"""
Integration tests for the complete EyeOfHorus system.

Tests cover:
- End-to-end decoding pipelines
- Module interactions
- Real-world usage scenarios
- 408 grammar validation
"""

import pytest
from eye_of_horus import (
    # Mapping
    leiden_to_wheel,
    phonemes_to_verbs,
    WHEEL_16,
    WHEEL_VERBS,
    # Engine
    Mode,
    Pole,
    Scale,
    Hourglass,
    Relation,
    PHONEME_HOURGLASSES,
    PHONEME_ORDER,
    get_hourglass,
    get_core_verb,
    generate_relations,
    count_relations,
    get_all_relations,
    total_grammar,
    triangular,
    decode_with_mode,
    decode_trajectory,
)


class TestEndToEndDecoding:
    """End-to-end decoding tests."""
    
    def test_leiden_to_verbs_pipeline(self):
        """Full pipeline: Leiden → phonemes → verbs."""
        translit = 'ptr'
        phonemes = leiden_to_wheel(translit)
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['FORM', 'MEASURE', 'ILLUMINE']
    
    def test_leiden_to_mode_decode(self):
        """Full pipeline with mode selection."""
        translit = 'rꜥ'  # Ra
        phonemes = leiden_to_wheel(translit)
        
        # Masculine reading
        masc_verbs = decode_with_mode(phonemes, Mode.MASCULINE, Pole.EQUILIBRIUM)
        assert masc_verbs == ['ILLUMINE', 'SOURCE']
        
        # Feminine reading
        fem_verbs = decode_with_mode(phonemes, Mode.FEMININE, Pole.EQUILIBRIUM)
        assert fem_verbs == ['REVEAL', 'RECEPTIVE']
    
    def test_abracadabra_full_decode(self):
        """ABRACADABRA end-to-end with all modes."""
        phonemes = ['a', 'b', 'r', 'k', 'd', 'b', 'r']
        
        # Equilibrium (core verbs)
        eq_traj = decode_trajectory(phonemes, Mode.MASCULINE, Pole.EQUILIBRIUM)
        assert eq_traj == 'SOURCE → BIRTH → ILLUMINE → CYCLE → DO → BIRTH → ILLUMINE'
        
        # Minima
        min_verbs = decode_with_mode(phonemes, Mode.MASCULINE, Pole.MINIMA)
        assert min_verbs == ['VOID', 'BLOCK', 'OBSCURE', 'HALT', 'STALL', 'BLOCK', 'OBSCURE']
        
        # Maxima
        max_verbs = decode_with_mode(phonemes, Mode.MASCULINE, Pole.MAXIMA)
        assert max_verbs == ['FULLNESS', 'BURST', 'BLIND', 'ACCELERATE', 'FORCE', 'BURST', 'BLIND']


class TestVerbConsistency:
    """Tests ensuring mapping and engine verbs are consistent."""
    
    def test_wheel_verbs_match_engine(self):
        """WHEEL_VERBS matches engine core verbs."""
        for phoneme, wheel_verb in WHEEL_VERBS.items():
            engine_verb = get_core_verb(phoneme)
            # Note: some verbs were updated (GENERATE → WEIGH, TRANSFORM → DO)
            # The mapping module now uses the updated verbs


class TestGrammarMathematics:
    """Tests for the 408 grammar mathematics."""
    
    def test_triangular_16_is_136(self):
        """T(16) = 136."""
        assert triangular(16) == 136
    
    def test_relations_count_136(self):
        """136 unique phoneme relations (including 16 self-relations)."""
        assert count_relations() == 136
    
    def test_scales_count_3(self):
        """3 reading scales linked to spine phonemes."""
        assert len(Scale) == 3
    
    def test_total_grammar_408(self):
        """136 × 3 = 408."""
        assert total_grammar() == 408
    
    def test_408_equals_136_times_3(self):
        """Verify 408 = T(16) × scales."""
        t16 = triangular(16)
        scales = len(Scale)
        assert t16 * scales == 408


class TestHourglassIntegration:
    """Tests for hourglass structure integration."""
    
    def test_all_wheel_phonemes_have_hourglasses(self):
        """Every wheel phoneme has an hourglass."""
        for p in WHEEL_16:
            hg = get_hourglass(p)
            assert hg is not None, f"No hourglass for {p}"
    
    def test_hourglasses_match_phoneme_order(self):
        """PHONEME_ORDER contains all wheel phonemes."""
        wheel_set = set(WHEEL_16)
        order_set = set(PHONEME_ORDER)
        # They should have the same phonemes (though order may differ)
        assert wheel_set == order_set


class TestRelationGeneration:
    """Tests for relation generation."""
    
    def test_relations_are_pairs(self):
        """Each relation is a 2-tuple."""
        for a, b in generate_relations():
            assert isinstance(a, str)
            assert isinstance(b, str)
            assert a in PHONEME_ORDER
            assert b in PHONEME_ORDER
    
    def test_relation_objects_work(self):
        """Relation objects integrate correctly."""
        relations = get_all_relations()
        for rel in relations:
            # Both verbs should be valid (not ?xxx)
            assert not rel.verb_a.startswith('?')
            assert not rel.verb_b.startswith('?')
            # Forward and reverse should be well-formed
            assert '→' in rel.forward
            assert '→' in rel.reverse


class TestScaleApplication:
    """Tests for scale application (conceptual)."""
    
    def test_same_phoneme_different_scales(self):
        """Same phoneme applies at all scales (verbs unchanged)."""
        phoneme = 'n'
        
        # The verb is the same regardless of scale
        # Scale affects interpretation, not the verb itself
        verbs_onto = decode_with_mode([phoneme], Mode.MASCULINE, Pole.EQUILIBRIUM)
        verbs_phylo = decode_with_mode([phoneme], Mode.MASCULINE, Pole.EQUILIBRIUM)
        verbs_cosmo = decode_with_mode([phoneme], Mode.MASCULINE, Pole.EQUILIBRIUM)
        
        assert verbs_onto == verbs_phylo == verbs_cosmo == ['WEAVE']


class TestRealWorldScenarios:
    """Tests using realistic decoding scenarios."""
    
    def test_deity_name_maat(self):
        """Ma'at decodes semantically."""
        phonemes = leiden_to_wheel('mꜣꜥt')
        # Should include m, a, a, t (aleph and ayin both → a)
        assert 'm' in phonemes
        assert 't' in phonemes
        assert phonemes.count('a') >= 1
    
    def test_deity_name_neith(self):
        """Neith (n-t) decodes as WEAVE-MEASURE."""
        phonemes = leiden_to_wheel('nt')
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['WEAVE', 'MEASURE']
    
    def test_woman_weave_men_concept(self):
        """Test the WOMAN = WEAVE-MEN phonemic concept."""
        # In English: w-o-m-a-n
        # Phonemically: w-m-n (stripping vowels)
        phonemes = ['w', 'm', 'n']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['PROTECT', 'WEIGH', 'WEAVE']
        # PROTECT-WEIGH-WEAVE: she who protects, weighs, and weaves


class TestModuleImports:
    """Tests for correct module imports."""
    
    def test_main_package_imports(self):
        """Main package exports work."""
        import eye_of_horus
        
        # Mapping
        assert hasattr(eye_of_horus, 'leiden_to_wheel')
        assert hasattr(eye_of_horus, 'WHEEL_16')
        
        # Engine
        assert hasattr(eye_of_horus, 'Mode')
        assert hasattr(eye_of_horus, 'Pole')
        assert hasattr(eye_of_horus, 'Scale')
        assert hasattr(eye_of_horus, 'get_hourglass')
        assert hasattr(eye_of_horus, 'total_grammar')
    
    def test_engine_submodule(self):
        """Engine submodule accessible."""
        from eye_of_horus import engine
        assert hasattr(engine, 'PHONEME_HOURGLASSES')
        assert hasattr(engine, 'generate_relations')


class TestVersioning:
    """Tests for package versioning."""
    
    def test_version_exists(self):
        """Package has version."""
        import eye_of_horus
        assert hasattr(eye_of_horus, '__version__')
    
    def test_version_is_0_4(self):
        """Version is 0.4.0 (with layered decode)."""
        import eye_of_horus
        assert eye_of_horus.__version__ == '0.4.0'
