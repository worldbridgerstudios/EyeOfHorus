"""
Tests for bitwise phonemic engine.

Validates:
- Phoneme encoding/decoding roundtrip
- Classification (wheel vs spine)
- Semantic address construction
- Layered decode consistency with string-based engine
- Relation and grammar indexing
"""

import pytest
import numpy as np
from eye_of_horus.bitwise import (
    # IDs
    PHONEME_TO_ID, ID_TO_PHONEME, NUM_PHONEMES, NUM_WHEEL, NUM_SPINE,
    ID_N, ID_W, ID_S, ID_SH, ID_A, ID_T, ID_H, ID_R,
    ID_M, ID_AA, ID_Y, ID_B, ID_P, ID_I, ID_KH, ID_DJ,
    ID_D, ID_K, ID_X, ID_G, ID_F, ID_HH,
    SPINE_BIT,
    # Position
    Pos, Layer, LAYER_POS,
    MODE_MASC, MODE_FEM, POLE_EQ, POLE_MIN, POLE_MAX,
    # Tables
    VERB_TABLE, CORE_VERB_TABLE,
    # Functions
    encode_phonemes, decode_ids, semantic_address, address_to_components,
    is_wheel, is_spine, is_wheel_array, is_spine_array,
    decode_layer, decode_all_layers, decode_layered, LayeredResult,
    decode_text, phonemes_to_verbs_fast,
    relation_index, relation_to_pair, NUM_WHEEL_RELATIONS,
    grammar_index, grammar_to_components, TOTAL_GRAMMAR,
    Scale,
)
from eye_of_horus.engine import (
    PHONEME_HOURGLASSES, SPINE_HOURGLASSES,
    Mode, Pole,
)


class TestPhonemeEncoding:
    """Test phoneme ID encoding/decoding."""
    
    def test_num_phonemes(self):
        assert NUM_PHONEMES == 22
        assert NUM_WHEEL == 16
        assert NUM_SPINE == 6
    
    def test_wheel_ids(self):
        """Wheel phonemes should have IDs 0-15."""
        wheel = ['n', 'w', 's', 'sh', 'A', 't', 'H', 'r', 'm', 'a', 'y', 'b', 'p', 'i', 'kh', 'dj']
        for i, p in enumerate(wheel):
            assert PHONEME_TO_ID[p] == i, f"{p} should have ID {i}"
    
    def test_spine_ids(self):
        """Spine phonemes should have IDs 16-21."""
        spine = ['d', 'k', 'x', 'g', 'f', 'h']
        for i, p in enumerate(spine):
            assert PHONEME_TO_ID[p] == 16 + i, f"{p} should have ID {16+i}"
    
    def test_encode_roundtrip(self):
        """Encoding then decoding should return original."""
        phonemes = ['n', 'w', 's', 'sh', 'A', 'd', 'k', 'x']
        ids = encode_phonemes(phonemes)
        recovered = decode_ids(ids)
        assert recovered == phonemes
    
    def test_id_to_phoneme_array(self):
        """ID_TO_PHONEME array should have correct length."""
        assert len(ID_TO_PHONEME) == NUM_PHONEMES


class TestClassification:
    """Test wheel/spine classification."""
    
    def test_wheel_classification(self):
        """Wheel phonemes should classify correctly."""
        for i in range(16):
            assert is_wheel(i), f"ID {i} should be wheel"
            assert not is_spine(i), f"ID {i} should not be spine"
    
    def test_spine_classification(self):
        """Spine phonemes should classify correctly."""
        for i in range(16, 22):
            assert is_spine(i), f"ID {i} should be spine"
            assert not is_wheel(i), f"ID {i} should not be wheel"
    
    def test_spine_bit(self):
        """SPINE_BIT should correctly identify spine."""
        assert SPINE_BIT == 0b10000
        for i in range(16):
            assert (i & SPINE_BIT) == 0
        for i in range(16, 22):
            assert (i & SPINE_BIT) != 0
    
    def test_vectorized_classification(self):
        """Array classification should match scalar."""
        ids = np.array([0, 5, 15, 16, 18, 21], dtype=np.uint8)
        wheel_mask = is_wheel_array(ids)
        spine_mask = is_spine_array(ids)
        
        expected_wheel = np.array([True, True, True, False, False, False])
        expected_spine = np.array([False, False, False, True, True, True])
        
        np.testing.assert_array_equal(wheel_mask, expected_wheel)
        np.testing.assert_array_equal(spine_mask, expected_spine)


class TestSemanticAddress:
    """Test 8-bit semantic address encoding."""
    
    def test_address_construction(self):
        """Address should combine phoneme, mode, pole correctly."""
        # n (0), masc, eq → 0b00000_0_00 = 0
        assert semantic_address(0, MODE_MASC, POLE_EQ) == 0
        
        # n (0), fem, min → 0b00000_1_01 = 5
        assert semantic_address(0, MODE_FEM, POLE_MIN) == 5
        
        # dj (15), fem, max → 0b01111_1_10 = 126
        assert semantic_address(15, MODE_FEM, POLE_MAX) == 126
    
    def test_address_decomposition(self):
        """Decomposition should recover components."""
        for p_id in [0, 7, 15, 18]:
            for mode in [0, 1]:
                for pole in [0, 1, 2]:
                    addr = semantic_address(p_id, mode, pole)
                    recovered = address_to_components(addr)
                    assert recovered == (p_id, mode, pole)
    
    def test_position_enum_values(self):
        """Position enum values should match bit patterns."""
        assert Pos.EQ_MASC == 0b000
        assert Pos.MIN_MASC == 0b001
        assert Pos.MAX_MASC == 0b010
        assert Pos.EQ_FEM == 0b100
        assert Pos.MIN_FEM == 0b101
        assert Pos.MAX_FEM == 0b110


class TestVerbTable:
    """Test verb lookup table."""
    
    def test_verb_table_size(self):
        """Table should have 256 entries."""
        assert len(VERB_TABLE) == 256
    
    def test_core_verb_table_size(self):
        """Core verb table should have 22 entries."""
        assert len(CORE_VERB_TABLE) == NUM_PHONEMES
    
    def test_verb_lookup_matches_hourglass(self):
        """Verb table should match hourglass data."""
        # Test n (INTEGRATE)
        hg = PHONEME_HOURGLASSES['n']
        addr = semantic_address(ID_N, MODE_MASC, POLE_EQ)
        assert VERB_TABLE[addr] == hg.equilibrium_masc == 'INTEGRATE'
        
        addr = semantic_address(ID_N, MODE_FEM, POLE_MAX)
        assert VERB_TABLE[addr] == hg.max_fem == 'INTERLOCK'
    
    def test_spine_verb_lookup(self):
        """Spine verbs should be accessible."""
        hg = SPINE_HOURGLASSES['d']
        addr = semantic_address(ID_D, MODE_MASC, POLE_EQ)
        assert VERB_TABLE[addr] == 'DO'
    
    def test_core_verbs_match(self):
        """Core verb table should match equilibrium verbs."""
        for p, hg in PHONEME_HOURGLASSES.items():
            p_id = PHONEME_TO_ID[p]
            assert CORE_VERB_TABLE[p_id] == hg.equilibrium_masc


class TestLayeredDecode:
    """Test layered decode functionality."""
    
    def test_layer_enum(self):
        """Layer enum should have 5 values."""
        assert len(Layer) == 5
        assert Layer.CORE == 0
        assert Layer.M2 == 4
    
    def test_layer_pos_values(self):
        """Layer position bits should be correct."""
        assert LAYER_POS[Layer.CORE] == Pos.EQ_MASC
        assert LAYER_POS[Layer.F1] == Pos.MIN_FEM
        assert LAYER_POS[Layer.F2] == Pos.MAX_FEM
        assert LAYER_POS[Layer.M1] == Pos.MIN_MASC
        assert LAYER_POS[Layer.M2] == Pos.MAX_MASC
    
    def test_core_layer_all_equilibrium(self):
        """Core layer should return equilibrium verbs."""
        ids = np.array([ID_N, ID_W, ID_S], dtype=np.uint8)
        verbs = decode_layer(ids, Layer.CORE)
        assert verbs[0] == 'INTEGRATE'
        assert verbs[1] == 'CHARGE'
        assert verbs[2] == 'EMERGE'
    
    def test_f1_layer_alternation(self):
        """F1 layer should alternate min_fem/eq_fem."""
        ids = np.array([ID_N, ID_N, ID_N, ID_N], dtype=np.uint8)
        verbs = decode_layer(ids, Layer.F1)
        # Even indices: min_fem, odd indices: eq_fem
        assert verbs[0] == 'UNRAVEL'    # min_fem
        assert verbs[1] == 'WEAVE'      # eq_fem
        assert verbs[2] == 'UNRAVEL'    # min_fem
        assert verbs[3] == 'WEAVE'      # eq_fem
    
    def test_m2_layer_alternation(self):
        """M2 layer should alternate max_masc/eq_masc."""
        ids = np.array([ID_N, ID_N], dtype=np.uint8)
        verbs = decode_layer(ids, Layer.M2)
        assert verbs[0] == 'FUSE'       # max_masc
        assert verbs[1] == 'INTEGRATE'  # eq_masc
    
    def test_all_layers_returns_five(self):
        """decode_all_layers should return 5 arrays."""
        ids = np.array([ID_N, ID_W, ID_S], dtype=np.uint8)
        layers = decode_all_layers(ids)
        assert len(layers) == 5
        for layer in layers:
            assert len(layer) == 3
    
    def test_layered_result_structure(self):
        """LayeredResult should have correct attributes."""
        ids = np.array([ID_N, ID_W], dtype=np.uint8)
        result = decode_layered(ids)
        
        assert isinstance(result, LayeredResult)
        assert len(result.core) == 2
        assert len(result.f1) == 2
        assert len(result.f2) == 2
        assert len(result.m1) == 2
        assert len(result.m2) == 2
        np.testing.assert_array_equal(result.phoneme_ids, ids)
    
    def test_decode_text_convenience(self):
        """decode_text should accept string phonemes."""
        result = decode_text(['n', 'w', 's'])
        assert result.core[0] == 'INTEGRATE'
        assert result.core[1] == 'CHARGE'
        assert result.core[2] == 'EMERGE'


class TestRelations:
    """Test relation encoding."""
    
    def test_num_relations(self):
        """Should have T(16) = 136 relations."""
        assert NUM_WHEEL_RELATIONS == 136
    
    def test_relation_index_self(self):
        """Self-relations should be on diagonal."""
        # (0,0) → 0, (1,1) → 2, (2,2) → 5, etc.
        assert relation_index(0, 0) == 0
        assert relation_index(1, 1) == 2
        assert relation_index(2, 2) == 5
    
    def test_relation_index_pairs(self):
        """Pair relations should be triangular."""
        # (0,1) → 1, (0,2) → 3, (1,2) → 4
        assert relation_index(0, 1) == 1
        assert relation_index(0, 2) == 3
        assert relation_index(1, 2) == 4
    
    def test_relation_canonical_ordering(self):
        """Order shouldn't matter for undirected relations."""
        assert relation_index(0, 5) == relation_index(5, 0)
        assert relation_index(3, 12) == relation_index(12, 3)
    
    def test_relation_roundtrip(self):
        """Index to pair and back should work."""
        for a in range(16):
            for b in range(a, 16):
                idx = relation_index(a, b)
                recovered = relation_to_pair(idx)
                assert recovered == (a, b), f"Failed for ({a},{b})"
    
    def test_all_relations_unique(self):
        """All 136 relations should have unique indices."""
        indices = set()
        for a in range(16):
            for b in range(a, 16):
                idx = relation_index(a, b)
                assert idx not in indices, f"Duplicate index {idx}"
                indices.add(idx)
        assert len(indices) == 136


class TestGrammar:
    """Test 408-grammar encoding."""
    
    def test_total_grammar(self):
        """Total grammar should be 408."""
        assert TOTAL_GRAMMAR == 408
    
    def test_grammar_index_range(self):
        """Grammar indices should span 0-407."""
        for scale in Scale:
            for rel in range(NUM_WHEEL_RELATIONS):
                idx = grammar_index(scale, rel)
                assert 0 <= idx < TOTAL_GRAMMAR
    
    def test_grammar_roundtrip(self):
        """Grammar index decomposition should roundtrip."""
        for scale in Scale:
            for rel in [0, 50, 135]:
                idx = grammar_index(scale, rel)
                s, r = grammar_to_components(idx)
                assert s == scale
                assert r == rel


class TestConvenience:
    """Test convenience functions."""
    
    def test_phonemes_to_verbs_fast(self):
        """Fast verb conversion should match slow path."""
        phonemes = ['n', 'w', 's', 'sh', 'A', 't']
        fast = phonemes_to_verbs_fast(phonemes)
        expected = ['INTEGRATE', 'CHARGE', 'EMERGE', 'DIRECT', 'LEAD', 'READ']
        assert fast == expected
    
    def test_spine_phonemes_in_text(self):
        """Should handle spine phonemes in text."""
        phonemes = ['n', 'd', 'k', 'x']
        fast = phonemes_to_verbs_fast(phonemes)
        assert fast == ['INTEGRATE', 'DO', 'CYCLE', 'FUNDAMENT']


class TestConsistencyWithEngine:
    """Verify bitwise results match string-based engine."""
    
    def test_all_wheel_verbs_match(self):
        """All wheel phoneme verbs should match."""
        from eye_of_horus.engine import get_hourglass, Mode, Pole
        
        for p, hg in PHONEME_HOURGLASSES.items():
            p_id = PHONEME_TO_ID[p]
            
            # Check all 6 positions
            for mode, pole, expected in [
                (Mode.MASCULINE, Pole.EQUILIBRIUM, hg.equilibrium_masc),
                (Mode.MASCULINE, Pole.MINIMA, hg.min_masc),
                (Mode.MASCULINE, Pole.MAXIMA, hg.max_masc),
                (Mode.FEMININE, Pole.EQUILIBRIUM, hg.equilibrium_fem),
                (Mode.FEMININE, Pole.MINIMA, hg.min_fem),
                (Mode.FEMININE, Pole.MAXIMA, hg.max_fem),
            ]:
                mode_bit = MODE_MASC if mode == Mode.MASCULINE else MODE_FEM
                pole_bit = {Pole.EQUILIBRIUM: POLE_EQ, Pole.MINIMA: POLE_MIN, Pole.MAXIMA: POLE_MAX}[pole]
                
                addr = semantic_address(p_id, mode_bit, pole_bit)
                assert VERB_TABLE[addr] == expected, f"Mismatch for {p} {mode} {pole}"
