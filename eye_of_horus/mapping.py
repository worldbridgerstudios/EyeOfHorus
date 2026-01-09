"""
Leiden transliteration → 16-position wheel mapping.

The wheel has 16 positions, each a fundamental phonemic verb.
This module handles transliteration conversion; see engine.py for
the complete hourglass semantics (5 positions per phoneme).

Wheel Order (from HoloCell paper):
| Pos | Phoneme | Leiden | Verb       |
|-----|---------|--------|------------|
|  1  | n       | n      | WEAVE      |
|  2  | w       | w      | PROTECT    |
|  3  | s       | s,z    | BIND       |
|  4  | sh      | š      | LIFT       |
|  5  | A       | ꜣ      | OPEN       |
|  6  | t       | t,ṯ    | MEASURE    |
|  7  | H       | ḥ      | PIERCE     |
|  8  | r       | r      | ILLUMINE   |
|  9  | m       | m      | WEIGH      |
| 10  | a       | ꜥ      | SOURCE     |
| 11  | y       | y      | YEARN      |
| 12  | b       | b      | BIRTH      |
| 13  | p       | p      | FORM       |
| 14  | i       | ꞽ,i    | POINT      |
| 15  | kh      | ḫ,ẖ    | MOLD       |
| 16  | dj      | ḏ      | JUDGE      |

Spine phonemes (NOT on wheel): x, d, k, q, g, f, h
"""

import re
from typing import List

# The 16 wheel phonemes in order
WHEEL_16 = ['n', 'w', 's', 'sh', 'A', 't', 'H', 'r', 'm', 'a', 'y', 'b', 'p', 'i', 'kh', 'dj']

# Phoneme to wheel position (0-indexed)
WHEEL_INDEX = {p: i for i, p in enumerate(WHEEL_16)}

# Core verbs for wheel phonemes
WHEEL_VERBS = {
    'n':  'WEAVE',      # Neith - interlacing
    'w':  'PROTECT',    # Wadjet - shielding
    's':  'BIND',       # Serpent - containing
    'sh': 'LIFT',       # Shu - raising
    'A':  'OPEN',       # Aleph - glottal opening
    't':  'MEASURE',    # Thoth - marking
    'H':  'PIERCE',     # Pharyngeal - penetrating
    'r':  'ILLUMINE',   # Ra - making visible
    'm':  'WEIGH',      # Ma'at - balancing
    'a':  'SOURCE',     # Ayin/Atum - origin
    'y':  'YEARN',      # Palatal glide - reaching
    'b':  'BIRTH',      # Ba - emerging
    'p':  'FORM',       # Ptah - shaping
    'i':  'POINT',      # Yod - indicating
    'kh': 'MOLD',       # Khnum - shaping
    'dj': 'JUDGE',      # Palatalized - decreeing
}

# Spine phonemes (not on wheel) - for reference
SPINE_VERBS = {
    'x':  'FUNDAMENT',  # Cosmogenic axis
    'd':  'DO',         # Phylogenic axis
    'k':  'CYCLE',      # Ontogenic axis
    'g':  'GROUND',     # Secondary spine
    'f':  'BREATHE',    # Secondary spine
    'h':  'SEE',        # Secondary spine (glottal, not pharyngeal H)
}

# Leiden Unified Transliteration → Wheel mapping
LEIDEN_TO_WHEEL = {
    # Position 1: n
    'n': 'n',
    
    # Position 2: w
    'w': 'w',
    'u': 'w',
    
    # Position 3: s
    's': 's',
    'z': 's',
    
    # Position 4: sh
    'š': 'sh',
    
    # Position 5: A (aleph) — DISTINCT from ayin
    'ꜣ': 'A',
    
    # Position 6: t
    't': 't',
    'ṯ': 't',
    
    # Position 7: H (pharyngeal) — DISTINCT from glottal h
    'ḥ': 'H',
    
    # Position 8: r
    'r': 'r',
    'l': 'r',
    
    # Position 9: m
    'm': 'm',
    
    # Position 10: a (ayin) — DISTINCT from aleph
    'ꜥ': 'a',
    
    # Position 11: y
    'y': 'y',
    
    # Position 12: b
    'b': 'b',
    
    # Position 13: p
    'p': 'p',
    
    # Position 14: i (yod) — DISTINCT from ayin
    'ꞽ': 'i',
    'i': 'i',
    
    # Position 15: kh
    'ḫ': 'kh',
    'ẖ': 'kh',
    
    # Position 16: dj (palatalized) — on wheel
    'ḏ': 'dj',
    
    # Spine phonemes (map but flag as spine)
    'd': 'd',   # Plain d is spine
    'k': 'k',   # Plain k is spine
    'q': 'k',   # Emphatic k → k (spine)
    'g': 'g',   # Spine
    'f': 'f',   # Spine
    'h': 'h',   # Glottal h is spine (distinct from pharyngeal H)
}

# All verbs (wheel + spine)
ALL_VERBS = {**WHEEL_VERBS, **SPINE_VERBS}

# Vowel markers for mode detection (used by engine.py)
VOWEL_MARKERS = {
    'a': 'masc',   # "ah" → masculine
    'e': 'fem',    # "ey/ay" → feminine
    'i': 'fem',    # → feminine
    'o': 'masc',   # → masculine
    'u': 'masc',   # → masculine
    'y': 'fem',    # → feminine
}


def leiden_to_wheel(translit: str, keep_words: bool = False) -> List[str]:
    """
    Convert Leiden transliteration to phoneme sequence.
    
    Returns both wheel AND spine phonemes (caller can distinguish).
    
    Args:
        translit: Leiden transliteration string
        keep_words: If True, return list of word-phoneme pairs
                   If False, return flat phoneme list
    
    Returns:
        List of phonemes (wheel + spine)
    """
    # Clean: remove parentheses content, =suffixes, punctuation, numbers
    clean = re.sub(r'\([^)]*\)', '', translit)  # remove (...)
    clean = re.sub(r'=[a-zꞽꜣꜥ]+', '', clean)    # remove =sn, =f etc  
    clean = re.sub(r'[.:\-+~0-9/!]', '', clean)  # remove punctuation
    clean = re.sub(r'[𓍹𓍺]', '', clean)          # remove cartouche markers
    clean = clean.lower().strip()
    
    if keep_words:
        words = clean.split()
        result = []
        for word in words:
            phonemes = _convert_word(word)
            if phonemes:
                result.append((word, phonemes))
        return result
    else:
        return _convert_word(clean.replace(' ', ''))


def _convert_word(word: str) -> List[str]:
    """Convert a single word to phonemes."""
    result = []
    for char in word:
        if char in ' ̯̱':
            continue
        if char in LEIDEN_TO_WHEEL:
            result.append(LEIDEN_TO_WHEEL[char])
    return result


def is_wheel_phoneme(p: str) -> bool:
    """Check if phoneme is on the wheel."""
    return p in WHEEL_VERBS


def is_spine_phoneme(p: str) -> bool:
    """Check if phoneme is spine."""
    return p in SPINE_VERBS


def phonemes_to_verbs(phonemes: List[str]) -> List[str]:
    """Convert phoneme sequence to verb sequence."""
    return [ALL_VERBS.get(p, f'?{p}') for p in phonemes]


def wheel_trajectory(translit: str) -> str:
    """
    Generate a semantic trajectory from transliteration.
    
    Returns a human-readable verb chain.
    """
    phonemes = leiden_to_wheel(translit)
    verbs = phonemes_to_verbs(phonemes)
    return ' → '.join(verbs)
