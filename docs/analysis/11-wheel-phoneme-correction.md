# 11. Wheel Phoneme Specification

**Date:** 2025-01-09  
**Status:** Specification complete, implementation pending

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
    
    # Position 16: dj (palatalized) — DISTINCT from plain d
    'ḏ': 'dj',
}
```

---

## Spine Phonemes (Not on Wheel)

These phonemes are spine-only — they frame the wheel but don't rotate:

| Phoneme | Leiden | Scale | Verb |
|---------|--------|-------|------|
| x | — | Cosmogenic | FUNDAMENT |
| d | d | Phylogenic | DO |
| k | k | Ontogenic | CYCLE |
| q | q | (secondary) | — |
| tj | ṯ | (secondary) | — |
| g | g | (secondary) | GROUND |
| f | f | (secondary) | BREATHE |
| h | h | (secondary) | SEE |

**Key:** Plain **d** and **k** are spine. Wheel has **dj** (palatalized).

---

## Verb Assignments

### Confirmed (from existing work)

| Pos | Phoneme | Deity | Verb |
|-----|---------|-------|------|
| 1 | n | Neith | WEAVE |
| 2 | w | Wadjet | PROTECT |
| 3 | s | Serpent | BIND |
| 4 | sh | Shu | LIFT |
| 6 | t | Thoth | MEASURE |
| 8 | r | Ra | ILLUMINE |
| 9 | m | Ma'at | WEIGH |
| 10 | a | Atum | SOURCE |
| 12 | b | Ba | BIRTH |
| 13 | p | Ptah | FORM |
| 15 | kh | Khnum | MOLD |

### Pending Assignment

| Pos | Phoneme | Candidates | Notes |
|-----|---------|------------|-------|
| 5 | A (aleph) | INITIATE, MARK, HALT | Glottal stop — beginning/boundary |
| 7 | H (pharyngeal) | PERCEIVE, WITNESS | Deeper than r, seeing inward |
| 11 | y | GLIDE, YIELD | Transition, flow |
| 14 | i (yod) | CARRY, INTEND | Semi-vowel, carrier |
| 16 | dj | JUDGE, DECREE | Palatalized emphasis |

---

## Implementation Checklist

1. ☐ Resolve verb assignments for positions 5, 7, 11, 14, 16
2. ☐ Update `WHEEL_16` in mapping.py
3. ☐ Update `LEIDEN_TO_WHEEL` with correct distinctions
4. ☐ Update `WHEEL_VERBS` with all 16 verbs
5. ☐ Update hourglass definitions in engine.py
6. ☐ Re-run test suite
7. ☐ Re-translate Lines 1-9

---

## Test Case: Line 1 `ꞽꜥb`

With correct mapping:
```
ꞽ → i (position 14) → [VERB-14]
ꜥ → a (position 10) → SOURCE
b → b (position 12) → BIRTH
```

Three distinct phonemes, three distinct verbs.
