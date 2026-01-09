"""
Tests for Leiden transliteration → wheel mapping.

Tests cover:
- Leiden character conversion
- Word cleaning and normalization
- Phoneme sequence generation
- Verb trajectory generation
"""

import pytest
from eye_of_horus.mapping import (
    WHEEL_16,
    WHEEL_INDEX,
    WHEEL_VERBS,
    LEIDEN_TO_WHEEL,
    VOWEL_MARKERS,
    leiden_to_wheel,
    phonemes_to_verbs,
    wheel_trajectory,
)


class TestWheelConstants:
    """Tests for wheel constant definitions."""
    
    def test_wheel_has_16_phonemes(self):
        """Exactly 16 phonemes in the wheel."""
        assert len(WHEEL_16) == 16
    
    def test_wheel_index_complete(self):
        """All wheel phonemes have indices."""
        assert len(WHEEL_INDEX) == 16
        for p in WHEEL_16:
            assert p in WHEEL_INDEX
    
    def test_wheel_index_values(self):
        """Indices are 0-15."""
        indices = list(WHEEL_INDEX.values())
        assert sorted(indices) == list(range(16))
    
    def test_wheel_verbs_complete(self):
        """All wheel phonemes have verbs."""
        assert len(WHEEL_VERBS) == 16
        for p in WHEEL_16:
            assert p in WHEEL_VERBS


class TestCoreVerbs:
    """Tests for core verb definitions."""
    
    def test_key_verbs(self):
        """Key phoneme-verb associations are correct."""
        expected = {
            'a': 'SOURCE',
            'b': 'BIRTH',
            'd': 'DO',
            'f': 'BREATHE',
            'g': 'GROUND',
            'h': 'SEE',
            'k': 'CYCLE',
            'kh': 'MOLD',
            'm': 'WEIGH',
            'n': 'WEAVE',
            'p': 'FORM',
            'r': 'ILLUMINE',
            's': 'BIND',
            'sh': 'LIFT',
            't': 'MEASURE',
            'w': 'PROTECT',
        }
        for phoneme, verb in expected.items():
            assert WHEEL_VERBS[phoneme] == verb, f"{phoneme} should map to {verb}"


class TestLeidenMapping:
    """Tests for Leiden transliteration mapping."""
    
    def test_basic_consonants(self):
        """Basic consonants map correctly."""
        assert LEIDEN_TO_WHEEL['p'] == 'p'
        assert LEIDEN_TO_WHEEL['b'] == 'b'
        assert LEIDEN_TO_WHEEL['t'] == 't'
        assert LEIDEN_TO_WHEEL['m'] == 'm'
        assert LEIDEN_TO_WHEEL['n'] == 'n'
        assert LEIDEN_TO_WHEEL['r'] == 'r'
    
    def test_emphatic_collapse(self):
        """Emphatic consonants collapse to base forms."""
        assert LEIDEN_TO_WHEEL['ṯ'] == 't'
        assert LEIDEN_TO_WHEEL['ḏ'] == 'd'
        assert LEIDEN_TO_WHEEL['q'] == 'k'
    
    def test_pharyngeal_collapse(self):
        """Pharyngeals collapse to h/a."""
        assert LEIDEN_TO_WHEEL['ḥ'] == 'h'
        assert LEIDEN_TO_WHEEL['ḫ'] == 'kh'
        assert LEIDEN_TO_WHEEL['ẖ'] == 'kh'
    
    def test_glottal_to_a(self):
        """Glottal stops map to a."""
        assert LEIDEN_TO_WHEEL['ꜣ'] == 'a'
        assert LEIDEN_TO_WHEEL['ꜥ'] == 'a'
    
    def test_shin(self):
        """Š maps to sh."""
        assert LEIDEN_TO_WHEEL['š'] == 'sh'
    
    def test_voiced_distinctions_collapse(self):
        """Voiced/voiceless distinctions collapse."""
        assert LEIDEN_TO_WHEEL['z'] == 's'


class TestLeidenToWheel:
    """Tests for leiden_to_wheel function."""
    
    def test_simple_word(self):
        """Simple transliteration converts correctly."""
        result = leiden_to_wheel('ptr')
        assert result == ['p', 't', 'r']
    
    def test_with_aleph(self):
        """Aleph (ꜣ) converts to a."""
        result = leiden_to_wheel('ꜣnḫ')  # ankh
        assert 'a' in result
        assert 'n' in result
        assert 'kh' in result
    
    def test_parentheses_removal(self):
        """Parenthetical content removed."""
        result = leiden_to_wheel('ptr(n)')
        assert result == ['p', 't', 'r']  # (n) is removed
    
    def test_suffix_removal(self):
        """=suffixes removed."""
        result = leiden_to_wheel('ḥtp=f')
        # Should have h, t, p (suffix =f removed)
        assert 'h' in result
        assert 't' in result
        assert 'p' in result
    
    def test_punctuation_removal(self):
        """Punctuation removed."""
        result = leiden_to_wheel('ptr.ntr')
        assert result == ['p', 't', 'r', 'n', 't', 'r']
    
    def test_empty_string(self):
        """Empty string returns empty list."""
        assert leiden_to_wheel('') == []
    
    def test_keep_words_mode(self):
        """keep_words returns word-phoneme pairs."""
        result = leiden_to_wheel('ptr ntr', keep_words=True)
        assert len(result) == 2
        assert result[0][0] == 'ptr'
        assert result[0][1] == ['p', 't', 'r']
        assert result[1][0] == 'ntr'
        assert result[1][1] == ['n', 't', 'r']


class TestPhonemesToVerbs:
    """Tests for phonemes_to_verbs function."""
    
    def test_basic_conversion(self):
        """Phonemes convert to verbs correctly."""
        phonemes = ['p', 't', 'r']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['FORM', 'MEASURE', 'ILLUMINE']
    
    def test_unknown_phoneme(self):
        """Unknown phonemes marked with ?."""
        phonemes = ['p', 'xyz', 'r']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['FORM', '?xyz', 'ILLUMINE']
    
    def test_empty_list(self):
        """Empty list returns empty list."""
        assert phonemes_to_verbs([]) == []
    
    def test_all_phonemes(self):
        """All 16 phonemes convert without error."""
        verbs = phonemes_to_verbs(WHEEL_16)
        assert len(verbs) == 16
        for v in verbs:
            assert not v.startswith('?')


class TestWheelTrajectory:
    """Tests for wheel_trajectory function."""
    
    def test_basic_trajectory(self):
        """Trajectory produces arrow-joined string."""
        traj = wheel_trajectory('ptr')
        assert traj == 'FORM → MEASURE → ILLUMINE'
    
    def test_empty_trajectory(self):
        """Empty input produces empty string."""
        traj = wheel_trajectory('')
        assert traj == ''
    
    def test_single_phoneme_trajectory(self):
        """Single phoneme has no arrows."""
        traj = wheel_trajectory('r')
        assert traj == 'ILLUMINE'


class TestVowelMarkers:
    """Tests for vowel marker definitions."""
    
    def test_vowel_markers_defined(self):
        """Key vowel markers are defined."""
        assert 'a' in VOWEL_MARKERS
        assert 'e' in VOWEL_MARKERS
        assert 'i' in VOWEL_MARKERS
        assert 'o' in VOWEL_MARKERS
        assert 'u' in VOWEL_MARKERS
    
    def test_masculine_vowels(self):
        """Masculine vowels marked correctly."""
        assert VOWEL_MARKERS['a'] == 'masc'
        assert VOWEL_MARKERS['o'] == 'masc'
        assert VOWEL_MARKERS['u'] == 'masc'
    
    def test_feminine_vowels(self):
        """Feminine vowels marked correctly."""
        assert VOWEL_MARKERS['e'] == 'fem'
        assert VOWEL_MARKERS['i'] == 'fem'


class TestRealWords:
    """Tests using real Egyptian words."""
    
    def test_ankh(self):
        """ꜥnḫ (ankh - life) decodes correctly."""
        phonemes = leiden_to_wheel('ꜥnḫ')
        # ayin → a, n → n, kh → kh
        assert phonemes == ['a', 'n', 'kh']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['SOURCE', 'WEAVE', 'MOLD']
    
    def test_ntr(self):
        """nṯr (netjer - god) decodes correctly."""
        phonemes = leiden_to_wheel('nṯr')
        assert phonemes == ['n', 't', 'r']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['WEAVE', 'MEASURE', 'ILLUMINE']
    
    def test_maat(self):
        """mꜣꜥt (Ma'at) decodes correctly."""
        phonemes = leiden_to_wheel('mꜣꜥt')
        # m → m, aleph → a, ayin → a, t → t
        assert 'm' in phonemes
        assert 't' in phonemes
    
    def test_ra(self):
        """rꜥ (Ra) decodes correctly."""
        phonemes = leiden_to_wheel('rꜥ')
        assert phonemes == ['r', 'a']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['ILLUMINE', 'SOURCE']
    
    def test_ptah(self):
        """ptḥ (Ptah) decodes correctly."""
        phonemes = leiden_to_wheel('ptḥ')
        assert phonemes == ['p', 't', 'h']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['FORM', 'MEASURE', 'SEE']
