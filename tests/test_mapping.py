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
    SPINE_VERBS,
    ALL_VERBS,
    LEIDEN_TO_WHEEL,
    VOWEL_MARKERS,
    leiden_to_wheel,
    phonemes_to_verbs,
    wheel_trajectory,
    is_wheel_phoneme,
    is_spine_phoneme,
)


class TestWheelConstants:
    """Tests for wheel constant definitions."""
    
    def test_wheel_has_16_phonemes(self):
        """Exactly 16 phonemes in the wheel."""
        assert len(WHEEL_16) == 16
    
    def test_wheel_order(self):
        """Wheel order matches specification."""
        expected = ['n', 'w', 's', 'sh', 'A', 't', 'H', 'r', 'm', 'a', 'y', 'b', 'p', 'i', 'kh', 'dj']
        assert WHEEL_16 == expected
    
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


class TestWheelVerbs:
    """Tests for wheel verb definitions."""
    
    def test_wheel_verbs(self):
        """Wheel phoneme-verb associations are correct."""
        expected = {
            'n': 'WEAVE',
            'w': 'PROTECT',
            's': 'BIND',
            'sh': 'LIFT',
            'A': 'OPEN',
            't': 'MEASURE',
            'H': 'PIERCE',
            'r': 'ILLUMINE',
            'm': 'WEIGH',
            'a': 'SOURCE',
            'y': 'YEARN',
            'b': 'BIRTH',
            'p': 'FORM',
            'i': 'POINT',
            'kh': 'MOLD',
            'dj': 'JUDGE',
        }
        for phoneme, verb in expected.items():
            assert WHEEL_VERBS[phoneme] == verb, f"{phoneme} should map to {verb}"


class TestSpineVerbs:
    """Tests for spine verb definitions."""
    
    def test_spine_verbs(self):
        """Spine phoneme-verb associations are correct."""
        expected = {
            'x': 'FUNDAMENT',
            'd': 'DO',
            'k': 'CYCLE',
            'g': 'GROUND',
            'f': 'BREATHE',
            'h': 'SEE',
        }
        for phoneme, verb in expected.items():
            assert SPINE_VERBS[phoneme] == verb, f"{phoneme} should map to {verb}"


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
    
    def test_emphatic_distinctions(self):
        """Emphatic consonants map correctly."""
        assert LEIDEN_TO_WHEEL['ṯ'] == 't'   # Emphatic t → t
        assert LEIDEN_TO_WHEEL['ḏ'] == 'dj'  # Emphatic d → dj (wheel)
        assert LEIDEN_TO_WHEEL['d'] == 'd'   # Plain d → d (spine)
        assert LEIDEN_TO_WHEEL['q'] == 'k'   # Emphatic k → k (spine)
    
    def test_pharyngeal_distinctions(self):
        """Pharyngeals are distinct."""
        assert LEIDEN_TO_WHEEL['ḥ'] == 'H'   # Pharyngeal → H (wheel)
        assert LEIDEN_TO_WHEEL['h'] == 'h'   # Glottal → h (spine)
        assert LEIDEN_TO_WHEEL['ḫ'] == 'kh'
        assert LEIDEN_TO_WHEEL['ẖ'] == 'kh'
    
    def test_aleph_ayin_distinct(self):
        """Aleph and ayin are distinct."""
        assert LEIDEN_TO_WHEEL['ꜣ'] == 'A'   # Aleph → A
        assert LEIDEN_TO_WHEEL['ꜥ'] == 'a'   # Ayin → a
    
    def test_yod_distinct(self):
        """Yod is distinct from ayin."""
        assert LEIDEN_TO_WHEEL['ꞽ'] == 'i'   # Yod → i
        assert LEIDEN_TO_WHEEL['i'] == 'i'   # i → i
    
    def test_shin(self):
        """Š maps to sh."""
        assert LEIDEN_TO_WHEEL['š'] == 'sh'
    
    def test_voiced_distinctions_collapse(self):
        """Voiced/voiceless s collapse."""
        assert LEIDEN_TO_WHEEL['z'] == 's'


class TestLeidenToWheel:
    """Tests for leiden_to_wheel function."""
    
    def test_simple_word(self):
        """Simple transliteration converts correctly."""
        result = leiden_to_wheel('ptr')
        assert result == ['p', 't', 'r']
    
    def test_with_aleph(self):
        """Aleph (ꜣ) converts to A."""
        result = leiden_to_wheel('ꜣnḫ')
        assert 'A' in result
        assert 'n' in result
        assert 'kh' in result
    
    def test_parentheses_removal(self):
        """Parenthetical content removed."""
        result = leiden_to_wheel('ptr(n)')
        assert result == ['p', 't', 'r']
    
    def test_suffix_removal(self):
        """=suffixes removed."""
        result = leiden_to_wheel('ḥtp=f')
        assert 'H' in result  # Pharyngeal H
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


class TestPhonemesToVerbs:
    """Tests for phonemes_to_verbs function."""
    
    def test_wheel_phonemes(self):
        """Wheel phonemes convert to verbs correctly."""
        phonemes = ['p', 't', 'r']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['FORM', 'MEASURE', 'ILLUMINE']
    
    def test_spine_phonemes(self):
        """Spine phonemes convert to verbs correctly."""
        phonemes = ['d', 'k', 'h']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['DO', 'CYCLE', 'SEE']
    
    def test_mixed_phonemes(self):
        """Mixed wheel+spine phonemes convert correctly."""
        phonemes = ['r', 'd', 't', 'k']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['ILLUMINE', 'DO', 'MEASURE', 'CYCLE']
    
    def test_unknown_phoneme(self):
        """Unknown phonemes marked with ?."""
        phonemes = ['p', 'xyz', 'r']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['FORM', '?xyz', 'ILLUMINE']
    
    def test_empty_list(self):
        """Empty list returns empty list."""
        assert phonemes_to_verbs([]) == []
    
    def test_all_wheel_phonemes(self):
        """All 16 wheel phonemes convert without error."""
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
    
    def test_masculine_vowels(self):
        """Masculine vowels marked correctly."""
        assert VOWEL_MARKERS['a'] == 'masc'
        assert VOWEL_MARKERS['o'] == 'masc'
    
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
        # m → m, aleph → A, ayin → a, t → t
        assert phonemes == ['m', 'A', 'a', 't']
    
    def test_ra(self):
        """rꜥ (Ra) decodes correctly."""
        phonemes = leiden_to_wheel('rꜥ')
        assert phonemes == ['r', 'a']
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['ILLUMINE', 'SOURCE']
    
    def test_ptah(self):
        """ptḥ (Ptah) decodes correctly."""
        phonemes = leiden_to_wheel('ptḥ')
        assert phonemes == ['p', 't', 'H']  # Pharyngeal H
        verbs = phonemes_to_verbs(phonemes)
        assert verbs == ['FORM', 'MEASURE', 'PIERCE']


class TestPhonemeClassification:
    """Tests for phoneme classification functions."""
    
    def test_wheel_phonemes(self):
        """Wheel phonemes identified correctly."""
        for p in WHEEL_16:
            assert is_wheel_phoneme(p), f"{p} should be wheel"
    
    def test_spine_phonemes(self):
        """Spine phonemes identified correctly."""
        spine = ['x', 'd', 'k', 'g', 'f', 'h']
        for p in spine:
            assert is_spine_phoneme(p), f"{p} should be spine"
    
    def test_d_is_spine_not_wheel(self):
        """Plain d is spine, not wheel."""
        assert is_spine_phoneme('d')
        assert not is_wheel_phoneme('d')
    
    def test_dj_is_wheel_not_spine(self):
        """Palatalized dj is wheel, not spine."""
        assert is_wheel_phoneme('dj')
        assert not is_spine_phoneme('dj')
