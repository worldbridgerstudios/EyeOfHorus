"""
Leiden transliteration → 16-position wheel mapping.

The wheel has 16 positions, each a fundamental phonemic verb.
This module handles transliteration conversion; see engine.py for
the complete hourglass semantics (5 positions per phoneme).

Wheel Order (for trajectory analysis):
| Pos | Phoneme | Deity   | Core Verb  |
|-----|---------|---------|------------|
|  1  | p       | Ptah    | FORM       |
|  2  | t       | Thoth   | MEASURE    |
|  3  | kh      | Khnum   | MOLD       |
|  4  | s       | Serpent | BIND       |
|  5  | n       | Neith   | WEAVE      |
|  6  | r       | Ra      | ILLUMINE   |
|  7  | a       | Atum    | SOURCE     |
|  8  | h       | Horus   | SEE        |
|  9  | m       | Ma'at   | WEIGH      |
| 10  | w       | Wadjet  | PROTECT    |
| 11  | b       | Ba      | BIRTH      |
| 12  | k       | Khonsu  | CYCLE      |
| 13  | g       | Geb     | GROUND     |
| 14  | d       | Duat    | DO         |
| 15  | f       | —       | BREATHE    |
| 16  | sh      | Shu     | LIFT       |
"""

import re
from typing import List

# The 16 wheel phonemes in order
WHEEL_16 = ['p', 't', 'kh', 's', 'n', 'r', 'a', 'h', 'm', 'w', 'b', 'k', 'g', 'd', 'f', 'sh']

# Phoneme to wheel position (0-indexed)
WHEEL_INDEX = {p: i for i, p in enumerate(WHEEL_16)}

# Core verbs (masculine equilibrium) - maintained for backward compatibility
# For full hourglass semantics, use engine.py
WHEEL_VERBS = {
    'p':  'FORM',       # Ptah - shaping from void
    't':  'MEASURE',    # Thoth - marking, counting
    'kh': 'MOLD',       # Khnum - shaping on wheel
    's':  'BIND',       # Serpent/Set - binding, containing
    'n':  'WEAVE',      # Neith - interlacing threads (= equilibrium itself)
    'r':  'ILLUMINE',   # Ra - making visible
    'a':  'SOURCE',     # Atum - origin point
    'h':  'SEE',        # Horus - perceiving
    'm':  'WEIGH',      # Ma'at - scales, equanimity
    'w':  'PROTECT',    # Wadjet - shielding
    'b':  'BIRTH',      # Ba - emerging
    'k':  'CYCLE',      # Khonsu - returning, revolving
    'g':  'GROUND',     # Geb - supporting, underlying
    'd':  'DO',         # Duat - acting, transforming
    'f':  'BREATHE',    # — - animating, vitalizing
    'sh': 'LIFT',       # Shu - raising, separating
}

# Leiden Unified Transliteration → Wheel mapping
LEIDEN_TO_WHEEL = {
    # Labials
    'p': 'p',
    'b': 'b', 
    'f': 'f',
    'm': 'm',
    'w': 'w',
    
    # Dentals/Alveolars  
    't': 't',
    'ṯ': 't',      # emphatic t → t
    'd': 'd',
    'ḏ': 'd',      # emphatic d → d
    'n': 'n',
    'r': 'r',
    's': 's',
    'z': 's',      # z → s (voice distinction collapses)
    
    # Palatals/Velars
    'š': 'sh',     # shin
    'k': 'k',
    'g': 'g',
    'q': 'k',      # emphatic k → k
    
    # Gutturals/Pharyngeals
    'h': 'h',
    'ḥ': 'h',      # pharyngeal h → h
    'ḫ': 'kh',     # voiceless velar fricative
    'ẖ': 'kh',     # voiced velar fricative → kh
    
    # Glottals/Semi-vowels
    'ꜣ': 'a',      # aleph → a (glottal stop)
    'ꜥ': 'a',      # ayin → a (pharyngeal)
    'ꞽ': 'a',      # yod/i → a (treating as vowel carrier)
    'i': 'a',      # i → a
    'y': 'a',      # y → a
    'l': 'r',      # l → r (late Egyptian loan)
    'u': 'w',      # u → w
}

# Vowel markers for mode detection (used by engine.py)
VOWEL_MARKERS = {
    'a': 'masc',   # "ah" → masculine
    'e': 'fem',    # "ey/ay" → feminine (aleph quality)
    'i': 'fem',    # → feminine
    'o': 'masc',   # stress → masculine intensity
    'u': 'masc',   # stress → masculine intensity
    'y': 'fem',    # → feminine
}


def leiden_to_wheel(translit: str, keep_words: bool = False) -> List[str]:
    """
    Convert Leiden transliteration to wheel phoneme sequence.
    
    Args:
        translit: Leiden transliteration string
        keep_words: If True, return list of word-phoneme pairs
                   If False, return flat phoneme list
    
    Returns:
        List of wheel phonemes (16-position)
    """
    # Clean: remove parentheses content, =suffixes, punctuation, numbers
    clean = re.sub(r'\([^)]*\)', '', translit)  # remove (...)
    clean = re.sub(r'=[a-zꞽꜣꜥ]+', '', clean)    # remove =sn, =f etc  
    clean = re.sub(r'[.:\-+~0-9/!]', '', clean)  # remove punctuation
    clean = re.sub(r'[𓍹𓍺]', '', clean)          # remove cartouche markers
    clean = clean.lower().strip()
    
    if keep_words:
        # Process word by word
        words = clean.split()
        result = []
        for word in words:
            phonemes = _convert_word(word)
            if phonemes:
                result.append((word, phonemes))
        return result
    else:
        # Flat phoneme list
        return _convert_word(clean.replace(' ', ''))


def _convert_word(word: str) -> List[str]:
    """Convert a single word to wheel phonemes."""
    result = []
    for char in word:
        # Skip combining marks
        if char in ' ̯̱':
            continue
        if char in LEIDEN_TO_WHEEL:
            result.append(LEIDEN_TO_WHEEL[char])
    return result


def phonemes_to_verbs(phonemes: List[str]) -> List[str]:
    """Convert phoneme sequence to verb sequence (core verbs)."""
    return [WHEEL_VERBS.get(p, f'?{p}') for p in phonemes]


def wheel_trajectory(translit: str) -> str:
    """
    Generate a semantic trajectory from transliteration.
    
    Returns a human-readable verb chain.
    """
    phonemes = leiden_to_wheel(translit)
    verbs = phonemes_to_verbs(phonemes)
    return ' → '.join(verbs)
