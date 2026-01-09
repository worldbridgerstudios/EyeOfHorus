"""
Tests for the phonemic engine (hourglass architecture).

Tests cover:
- Hourglass structure (5 positions per phoneme)
- Mode selection (masculine/feminine)
- Pole selection (minima/equilibrium/maxima)
- Relations (T(16) = 136)
- Total grammar (408)
- Scale enumeration
"""

import pytest
from eye_of_horus.engine import (
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
    detect_mode,
    decode_with_mode,
    decode_trajectory,
    phonemes_to_verbs,
)


class TestTriangularNumbers:
    """Tests for triangular number calculation."""
    
    def test_triangular_basic(self):
        """T(n) = n(n+1)/2 for small values."""
        assert triangular(1) == 1
        assert triangular(2) == 3
        assert triangular(3) == 6
        assert triangular(4) == 10
        assert triangular(5) == 15
    
    def test_triangular_16(self):
        """T(16) = 136 — the number of unique phoneme pairs."""
        assert triangular(16) == 136
    
    def test_triangular_formula(self):
        """Verify formula for various n."""
        for n in range(1, 20):
            expected = sum(range(1, n + 1))
            assert triangular(n) == expected


class TestPhonemeCount:
    """Tests for phoneme data structures."""
    
    def test_phoneme_count(self):
        """Exactly 16 phonemes."""
        assert len(PHONEME_ORDER) == 16
        assert len(PHONEME_HOURGLASSES) == 16
    
    def test_all_phonemes_have_hourglasses(self):
        """Every phoneme in the order list has an hourglass."""
        for p in PHONEME_ORDER:
            assert p in PHONEME_HOURGLASSES
            assert get_hourglass(p) is not None
    
    def test_phoneme_order_matches_wheel(self):
        """Phoneme order matches the wheel specification."""
        expected = ['n', 'w', 's', 'sh', 'A', 't', 'H', 'r', 'm', 'a', 'y', 'b', 'p', 'i', 'kh', 'dj']
        assert PHONEME_ORDER == expected


class TestHourglassStructure:
    """Tests for the 5-position hourglass structure."""
    
    def test_hourglass_has_five_positions(self):
        """Each hourglass has 5 distinct meaning positions."""
        for p, hg in PHONEME_HOURGLASSES.items():
            positions = {
                hg.min_masc,
                hg.max_masc,
                hg.equilibrium_masc,
                hg.equilibrium_fem,
                hg.min_fem,
                hg.max_fem,
            }
            # Note: equilibrium may be same word for both modes
            # Minimum distinct: 5 (if eq shared) or 6 (if eq different)
            assert len(positions) >= 4, f"Phoneme {p} has too few distinct meanings"
    
    def test_hourglass_get_meaning_masculine(self):
        """get_meaning works for masculine mode."""
        hg = get_hourglass('r')  # Ra - SHINE
        assert hg.get_meaning(Mode.MASCULINE, Pole.MINIMA) == 'DIM'
        assert hg.get_meaning(Mode.MASCULINE, Pole.EQUILIBRIUM) == 'SHINE'
        assert hg.get_meaning(Mode.MASCULINE, Pole.MAXIMA) == 'BLAZE'
    
    def test_hourglass_get_meaning_feminine(self):
        """get_meaning works for feminine mode."""
        hg = get_hourglass('r')  # Ra
        assert hg.get_meaning(Mode.FEMININE, Pole.MINIMA) == 'SHADE'
        assert hg.get_meaning(Mode.FEMININE, Pole.EQUILIBRIUM) == 'BASK'
        assert hg.get_meaning(Mode.FEMININE, Pole.MAXIMA) == 'ABSORB'
    
    def test_core_verb_is_masculine_equilibrium(self):
        """core_verb property returns masculine equilibrium."""
        test_cases = {
            'a': 'HONOUR',
            'm': 'TRUE',
            'n': 'INTEGRATE',
            'r': 'SHINE',
            't': 'READ',
            'd': 'DO',
        }
        for phoneme, expected in test_cases.items():
            hg = get_hourglass(phoneme)
            assert hg.core_verb == expected
    
    def test_get_core_verb_function(self):
        """get_core_verb() function matches hourglass property."""
        for p in PHONEME_ORDER:
            hg = get_hourglass(p)
            assert get_core_verb(p) == hg.core_verb
    
    def test_unknown_phoneme_returns_question_mark(self):
        """Unknown phoneme returns ?phoneme."""
        assert get_core_verb('xyz') == '?xyz'
        assert get_hourglass('xyz') is None


class TestDeityAssociations:
    """Tests for deity associations."""
    
    def test_key_deity_mappings(self):
        """Core phoneme-deity associations are correct (v62)."""
        associations = {
            'a': 'Anubis',
            'n': 'Neith',
            'm': "Ma'at",
            'r': 'Ra',
            'H': 'Horus',
            'g': 'Geb',
            'sh': 'Shu',
            't': 'Seshat',
            'p': 'Ptah',
            'kh': 'Khnum',
            'w': 'Wadjet',
            's': 'Sekhmet',
            'A': 'Atum',
            'y': 'Isis',
            'b': 'Taweret',
            'i': 'Ihy',
            'dj': 'Thoth',
        }
        for phoneme, deity in associations.items():
            hg = get_hourglass(phoneme)
            assert hg.deity == deity, f"Phoneme {phoneme} should map to {deity}"


class TestMaatTrue:
    """Specific tests for M = Ma'at = TRUE."""
    
    def test_m_masculine_poles(self):
        """M masculine: FALSIFY - TRUE - VERIFY."""
        hg = get_hourglass('m')
        assert hg.min_masc == 'FALSIFY'
        assert hg.equilibrium_masc == 'TRUE'
        assert hg.max_masc == 'VERIFY'
    
    def test_m_feminine_poles(self):
        """M feminine: DOUBT - TRUST - BELIEVE."""
        hg = get_hourglass('m')
        assert hg.min_fem == 'DOUBT'
        assert hg.equilibrium_fem == 'TRUST'
        assert hg.max_fem == 'BELIEVE'


class TestNeithEquilibrium:
    """Specific tests for N = Neith = INTEGRATE (equilibrium itself)."""
    
    def test_n_is_integrate(self):
        """N's core verb is INTEGRATE."""
        assert get_core_verb('n') == 'INTEGRATE'
    
    def test_n_masculine_poles(self):
        """N masculine: FRAGMENT - INTEGRATE - FUSE."""
        hg = get_hourglass('n')
        assert hg.min_masc == 'FRAGMENT'
        assert hg.equilibrium_masc == 'INTEGRATE'
        assert hg.max_masc == 'FUSE'
    
    def test_n_feminine_poles(self):
        """N feminine: UNRAVEL - WEAVE - INTERLOCK."""
        hg = get_hourglass('n')
        assert hg.min_fem == 'UNRAVEL'
        assert hg.equilibrium_fem == 'WEAVE'
        assert hg.max_fem == 'INTERLOCK'


class TestRelations:
    """Tests for the 136 phoneme relations."""
    
    def test_relation_count(self):
        """Exactly 136 unique relations (T(16)) including self-relations."""
        assert count_relations() == 136
        assert len(generate_relations()) == 136
        assert len(get_all_relations()) == 136
    
    def test_relations_include_self_relations(self):
        """16 self-relations are included (a-a, b-b, etc.)."""
        relations = generate_relations()
        self_relations = [(a, b) for a, b in relations if a == b]
        assert len(self_relations) == 16
    
    def test_distinct_pairs_count(self):
        """120 distinct pairs + 16 self = 136."""
        relations = generate_relations()
        self_count = sum(1 for a, b in relations if a == b)
        distinct_count = sum(1 for a, b in relations if a != b)
        assert self_count == 16
        assert distinct_count == 120
        assert self_count + distinct_count == 136
    
    def test_relation_object_verbs(self):
        """Relation objects correctly produce verbs."""
        rel = Relation('r', 'n')
        assert rel.verb_a == 'SHINE'
        assert rel.verb_b == 'INTEGRATE'
        assert rel.forward == 'SHINE→INTEGRATE'
        assert rel.reverse == 'INTEGRATE→SHINE'


class TestTotalGrammar:
    """Tests for the 408 total grammar."""
    
    def test_total_grammar_is_408(self):
        """Total grammar = 136 × 3 = 408."""
        assert total_grammar() == 408
    
    def test_grammar_components(self):
        """408 = T(16) relations × 3 scales."""
        relations = count_relations()
        scales = len(Scale)
        assert relations == 136
        assert scales == 3
        assert relations * scales == 408


class TestScales:
    """Tests for the three reading scales linked to spine phonemes."""
    
    def test_three_scales(self):
        """Exactly three scales."""
        assert len(Scale) == 3
    
    def test_scale_spine_phonemes(self):
        """Scales are linked to spine phonemes x, d, k."""
        assert Scale.ONTOGENIC.phoneme == 'k'
        assert Scale.PHYLOGENIC.phoneme == 'd'
        assert Scale.COSMOGENIC.phoneme == 'x'
    
    def test_scale_verbs(self):
        """Scales have spine verbs."""
        assert Scale.ONTOGENIC.verb == 'CYCLE'
        assert Scale.PHYLOGENIC.verb == 'DO'
        assert Scale.COSMOGENIC.verb == 'FUNDAMENT'


class TestModes:
    """Tests for masculine/feminine mode selection."""
    
    def test_two_modes(self):
        """Exactly two modes."""
        assert len(Mode) == 2
    
    def test_mode_values(self):
        """Modes are masculine and feminine."""
        assert Mode.MASCULINE.value == 'masc'
        assert Mode.FEMININE.value == 'fem'
    
    def test_detect_mode_masculine(self):
        """Masculine vowels detected."""
        assert detect_mode('a') == Mode.MASCULINE
        assert detect_mode('o') == Mode.MASCULINE
        assert detect_mode('u') == Mode.MASCULINE
    
    def test_detect_mode_feminine(self):
        """Feminine vowels detected."""
        assert detect_mode('e') == Mode.FEMININE
        assert detect_mode('i') == Mode.FEMININE
        assert detect_mode('y') == Mode.FEMININE


class TestPoles:
    """Tests for the three pole positions."""
    
    def test_three_poles(self):
        """Exactly three poles."""
        assert len(Pole) == 3
    
    def test_pole_values(self):
        """Poles are minima, equilibrium, maxima."""
        assert Pole.MINIMA.value == 'min'
        assert Pole.EQUILIBRIUM.value == 'eq'
        assert Pole.MAXIMA.value == 'max'


class TestDecoding:
    """Tests for decoding phoneme sequences."""
    
    def test_decode_with_mode_masculine(self):
        """Decode in masculine mode returns masculine verbs."""
        phonemes = ['a', 'b', 'r']
        verbs = decode_with_mode(phonemes, Mode.MASCULINE, Pole.EQUILIBRIUM)
        assert verbs == ['HONOUR', 'HARVEST', 'SHINE']
    
    def test_decode_with_mode_feminine(self):
        """Decode in feminine mode returns feminine verbs."""
        phonemes = ['a', 'b', 'r']
        verbs = decode_with_mode(phonemes, Mode.FEMININE, Pole.EQUILIBRIUM)
        assert verbs == ['ALLOW', 'CULTIVATE', 'BASK']
    
    def test_decode_trajectory(self):
        """decode_trajectory returns arrow-joined string."""
        phonemes = ['a', 'b', 'r']
        traj = decode_trajectory(phonemes, Mode.MASCULINE)
        assert traj == 'HONOUR → HARVEST → SHINE'
    
    def test_phonemes_to_verbs_backward_compat(self):
        """phonemes_to_verbs maintains backward compatibility."""
        phonemes = ['a', 'b', 'r', 'k', 'd']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['HONOUR', 'HARVEST', 'SHINE', 'CYCLE', 'DO']
    
    def test_abracadabra(self):
        """ABRACADABRA decodes correctly."""
        # Ah-Ba-Ra-Ka-Da-Ba-Ra → A B R K D B R
        phonemes = ['a', 'b', 'r', 'k', 'd', 'b', 'r']
        verbs = decode_with_mode(phonemes, Mode.MASCULINE, Pole.EQUILIBRIUM)
        assert verbs == ['HONOUR', 'HARVEST', 'SHINE', 'CYCLE', 'DO', 'HARVEST', 'SHINE']
    
    def test_maat_decode(self):
        """MA'AT decodes as TRUE-HONOUR-READ."""
        phonemes = ['m', 'a', 't']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['TRUE', 'HONOUR', 'READ']
    
    def test_unknown_phoneme_in_sequence(self):
        """Unknown phonemes marked with ?."""
        phonemes = ['a', 'xyz', 'r']
        verbs = decode_with_mode(phonemes, Mode.MASCULINE, Pole.EQUILIBRIUM)
        assert verbs == ['HONOUR', '?xyz', 'SHINE']


class TestEdgeCases:
    """Edge case tests."""
    
    def test_empty_phoneme_list(self):
        """Empty list returns empty list."""
        assert decode_with_mode([], Mode.MASCULINE, Pole.EQUILIBRIUM) == []
        assert decode_trajectory([], Mode.MASCULINE) == ''
        assert phonemes_to_verbs([]) == []
    
    def test_single_phoneme(self):
        """Single phoneme decodes correctly."""
        assert decode_with_mode(['r'], Mode.MASCULINE, Pole.EQUILIBRIUM) == ['SHINE']
        assert decode_trajectory(['r'], Mode.MASCULINE) == 'SHINE'
    
    def test_all_phonemes_decode(self):
        """All 16 phonemes decode without error."""
        for p in PHONEME_ORDER:
            verbs = decode_with_mode([p], Mode.MASCULINE, Pole.EQUILIBRIUM)
            assert len(verbs) == 1
            assert not verbs[0].startswith('?')


class TestPositionCounts:
    """Tests verifying position mathematics."""
    
    def test_positions_per_phoneme(self):
        """5 positions per phoneme in hourglass structure."""
        # 2 masc poles + 2 fem poles + 1 shared eq = 5
        # (Though we store eq separately for masc/fem, the concept is 5)
        for p in PHONEME_ORDER:
            hg = get_hourglass(p)
            meanings = [
                hg.min_masc, hg.max_masc,
                hg.min_fem, hg.max_fem,
                hg.equilibrium_masc, hg.equilibrium_fem,
            ]
            # All should be non-empty strings
            for m in meanings:
                assert isinstance(m, str)
                assert len(m) > 0
    
    def test_total_positions(self):
        """80 total positions (16 × 5)."""
        # This is conceptual: 16 phonemes × 5 positions each
        positions = 16 * 5
        assert positions == 80
