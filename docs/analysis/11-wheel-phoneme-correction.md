# 11. Wheel Phoneme Specification

**Date:** 2025-01-09  
**Status:** ✓ Implemented in v0.4.0

---

## The True Wheel (16 Positions)

```
Position:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16
Phoneme:   n - w - s - sh - A - t - H - r - m - a - y - b - p - i - kh - dj
```

### Phoneme Definitions

| Pos | Symbol | Leiden | IPA | Articulatory |
|-----|--------|--------|-----|--------------|
| 1 | n | n | /n/ | Alveolar nasal |
| 2 | w | w | /w/ | Labial-velar approximant |
| 3 | s | s, z | /s/ | Alveolar fricative |
| 4 | sh | š | /ʃ/ | Palato-alveolar fricative |
| 5 | A | ꜣ | /ʔ/ | Glottal stop (aleph) |
| 6 | t | t, ṯ | /t/ | Alveolar stop |
| 7 | H | ḥ | /ħ/ | Pharyngeal fricative |
| 8 | r | r | /r/ | Alveolar trill/tap |
| 9 | m | m | /m/ | Bilabial nasal |
| 10 | a | ꜥ | /ʕ/ | Pharyngeal approximant (ayin) |
| 11 | y | y | /j/ | Palatal approximant |
| 12 | b | b | /b/ | Bilabial stop |
| 13 | p | p | /p/ | Bilabial stop (voiceless) |
| 14 | i | ꞽ, i | /j/ | Palatal glide (yod) |
| 15 | kh | ḫ, ẖ | /x/ | Velar fricative |
| 16 | dj | ḏ | /dʒ/ | Palato-alveolar affricate |

---

## Leiden → Wheel Mapping

All Unicode variants now handled:

```python
LEIDEN_TO_WHEEL = {
    # Position 1: n
    'n': 'n',
    
    # Position 2: w
    'w': 'w',
    'u': 'w',
    
    # Position 3: s
    's': 's',
    'z': 's',
    'ś': 's',      # s with acute (variant)
    
    # Position 4: sh
    'š': 'sh',
    
    # Position 5: A (aleph) — all Unicode variants
    'ꜣ': 'A',      # U+A723 EGYPTOLOGICAL ALEF (primary)
    'Ꜣ': 'A',      # U+A722 CAPITAL
    'ʾ': 'A',      # U+02BE MODIFIER RIGHT HALF RING
    'ʼ': 'A',      # U+02BC MODIFIER APOSTROPHE
    'ˀ': 'A',      # U+02C0 MODIFIER GLOTTAL STOP
    
    # Position 6: t
    't': 't',
    'ṯ': 't',      # t with line below
    'ṭ': 't',      # t with dot below
    
    # Position 7: H (pharyngeal) — DISTINCT from glottal h
    'ḥ': 'H',
    
    # Position 8: r
    'r': 'r',
    'l': 'r',      # l → r (late Egyptian)
    
    # Position 9: m
    'm': 'm',
    
    # Position 10: a (ayin) — all Unicode variants
    'ꜥ': 'a',      # U+A725 EGYPTOLOGICAL AIN (primary)
    'Ꜥ': 'a',      # U+A724 CAPITAL
    'ʿ': 'a',      # U+02BF MODIFIER LEFT HALF RING
    
    # Position 11: y
    'y': 'y',
    
    # Position 12: b
    'b': 'b',
    
    # Position 13: p
    'p': 'p',
    
    # Position 14: i (yod) — all Unicode variants
    'ꞽ': 'i',      # U+A7BD GLOTTAL I (primary)
    'i': 'i',
    'j': 'i',      # j often used for yod
    'ı': 'i',      # U+0131 dotless i
    'ỉ': 'i',      # U+1EC9 i with hook above
    
    # Position 15: kh (velar fricative)
    'ḫ': 'kh',
    'ẖ': 'kh',
    'x': 'kh',     # x sometimes used for kh
    
    # Position 16: dj (palatalized) — on wheel
    'ḏ': 'dj',
    'ḍ': 'dj',     # d with dot below
}
```

Also handles:
- `.PL`, `.DU`, `.SG` grammatical markers (stripped)
- Combining diacritics U+032F, U+0331 (skipped)
- Parenthetical content `(...)` (removed)
- Suffix markers `=sn`, `=f` etc (removed)

---

## Spine Phonemes (Not on Wheel)

These phonemes are spine-only — they frame the wheel but don't rotate:

| Phoneme | Leiden | Scale | Verb |
|---------|--------|-------|------|
| x | — | Cosmogenic | FUNDAMENT |
| d | d | Phylogenic | DO |
| k | k | Ontogenic | CYCLE |
| g | g | (secondary) | GROUND |
| f | f | (secondary) | BREATHE |
| h | h | (secondary) | SEE |

**Key:** Plain **d** and **k** are spine. Wheel has **dj** (palatalized).

---

## Complete Verb Assignments

All 16 wheel positions now have verbs:

| Pos | Phoneme | Deity | Verb | Hourglass |
|-----|---------|-------|------|-----------|
| 1 | n | Neith | WEAVE | SEVER ↔ CONNECT ↔ FUSE |
| 2 | w | Wadjet | PROTECT | EXPOSE ↔ SHELTER ↔ ENCLOSE |
| 3 | s | Serpent | BIND | LOOSE ↔ COMMIT ↔ CONSTRICT |
| 4 | sh | Shu | LIFT | PRESS ↔ SUPPORT ↔ SOAR |
| 5 | A | — | OPEN | SEAL ↔ ADMIT ↔ GAPE |
| 6 | t | Thoth | MEASURE | CHAOS ↔ ATTEND ↔ RIGIDIFY |
| 7 | H | — | PIERCE | DEFLECT ↔ PERCEIVE ↔ IMPALE |
| 8 | r | Ra | ILLUMINE | OBSCURE ↔ REVEAL ↔ BLIND |
| 9 | m | Ma'at | WEIGH | DIMINISH ↔ COMPASSION ↔ AMPLIFY |
| 10 | a | Atum | SOURCE | VOID ↔ RECEPTIVE ↔ FULLNESS |
| 11 | y | — | YEARN | REPEL ↔ YIELD ↔ CRAVE |
| 12 | b | Ba | BIRTH | BLOCK ↔ BEAR ↔ BURST |
| 13 | p | Ptah | FORM | SCATTER ↔ TEND ↔ FIX |
| 14 | i | — | POINT | BLUR ↔ INDICATE ↔ TARGET |
| 15 | kh | Khnum | MOLD | SHATTER ↔ SURRENDER ↔ PETRIFY |
| 16 | dj | — | JUDGE | CONFUSE ↔ DISCERN ↔ CONDEMN |

---

## Implementation Checklist

1. ✓ Resolved verb assignments for positions 5, 7, 11, 14, 16
2. ✓ Updated `WHEEL_16` in mapping.py
3. ✓ Updated `LEIDEN_TO_WHEEL` with correct distinctions + Unicode variants
4. ✓ Updated `WHEEL_VERBS` with all 16 verbs
5. ✓ Updated hourglass definitions in engine.py (wheel + spine separate)
6. ✓ All 198 tests passing
7. ✓ Re-translated Lines 1-9 (see doc 12 for layered decode)

---

## Test Case: Line 1 `ꞽꜥb`

With correct mapping:
```
ꞽ → i (position 14) → POINT
ꜥ → a (position 10) → SOURCE
b → b (position 12) → BIRTH
```

Three distinct phonemes, three distinct verbs.

---

## Author

Nicholas David Brown  
Independent Researcher

---

*"The wheel is now whole. 16 positions, 16 verbs, no conflation."*
