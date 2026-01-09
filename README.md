# Eye of Horus 𓂀

Read ancient Egyptian through the 16-position phonemic wheel.

## Architecture

**The 408 Grammar:** T(16) = 136 wheel relations × 3 spine axes = 408

### The Wheel (16 Phonemes)

| Pos | Phoneme | Leiden | Verb     | Deity   |
|-----|---------|--------|----------|---------|
| 1   | n       | n      | WEAVE    | Neith   |
| 2   | w       | w      | PROTECT  | Wadjet  |
| 3   | s       | s,z    | BIND     | Serpent |
| 4   | sh      | š      | LIFT     | Shu     |
| 5   | A       | ꜣ      | OPEN     | —       |
| 6   | t       | t,ṯ    | MEASURE  | Thoth   |
| 7   | H       | ḥ      | PIERCE   | —       |
| 8   | r       | r      | ILLUMINE | Ra      |
| 9   | m       | m      | WEIGH    | Ma'at   |
| 10  | a       | ꜥ      | SOURCE   | Atum    |
| 11  | y       | y      | YEARN    | —       |
| 12  | b       | b      | BIRTH    | Ba      |
| 13  | p       | p      | FORM     | Ptah    |
| 14  | i       | ꞽ,i    | POINT    | —       |
| 15  | kh      | ḫ,ẖ    | MOLD     | Khnum   |
| 16  | dj      | ḏ      | JUDGE    | —       |

### The Spine (3 Scale Phonemes)

| Phoneme | Verb      | Scale      |
|---------|-----------|------------|
| k       | CYCLE     | Ontogenic  |
| d       | DO        | Phylogenic |
| x       | FUNDAMENT | Cosmogenic |

### The Hourglass (5 Positions per Phoneme)

```
        Masc Max
           △
          / \
         / EQ \   ← shared equilibrium
        /_____\
        Fem Max
           ▽
```

Each phoneme has 5 semantic positions:
- **equilibrium** (shared center)
- **min_masc** / **max_masc** (masculine poles)
- **min_fem** / **max_fem** (feminine poles)

## Installation

```bash
pip install eye-of-horus
```

For corpus access (12,773 Earlier Egyptian sentences):
```bash
pip install eye-of-horus[corpus]
```

## Usage

### Basic Decoding

```python
from eye_of_horus import leiden_to_wheel, phonemes_to_verbs
from eye_of_horus.mapping import wheel_trajectory

# Convert transliteration to phonemes
phonemes = leiden_to_wheel("ꜥnḫ")  # ankh - life
# ['a', 'n', 'kh']

# Get verbs
verbs = phonemes_to_verbs(phonemes)
# ['SOURCE', 'WEAVE', 'MOLD']

# Or get trajectory directly
trajectory = wheel_trajectory("ꜥnḫ")
# "SOURCE → WEAVE → MOLD"
```

### Bidirectional Reading

```python
from eye_of_horus import decode_bidirectional

# Decode Pyramid Text lines 1-9 (Fibonacci breath block)
lines, ascend, penetrate = decode_bidirectional(1, 9)

# ascend (L→R): cohering, unifying — becoming
# penetrate (R→L): decohering, dissolving — undoing
```

### Layered Decode (5 Simultaneous Readings)

```python
from eye_of_horus import decode_layered

# Five parallel layers with pole alternation
ascend, penetrate = decode_layered(1, 9)

# ASCEND order: core → f1 → f2 → m1 → m2
# PENETRATE order: core → m1 → m2 → f1 → f2

# Each layer alternates: (pole)(eq)(pole)(eq)...
# - core: all equilibrium
# - f1: min_fem alternating with eq
# - f2: max_fem alternating with eq
# - m1: min_masc alternating with eq
# - m2: max_masc alternating with eq
```

### Corpus Search

```python
from eye_of_horus import load_tla_corpus, search_corpus

# Load full corpus
corpus = load_tla_corpus()
print(f"Loaded {len(corpus)} sentences")

# Search by pattern
results = search_corpus("ankh", corpus)
```

### 408 Grammar Access

```python
from eye_of_horus import (
    triangular,
    count_relations,
    total_grammar,
    get_all_triangular_relations,
)

# T(16) = 136
assert triangular(16) == 136

# 136 wheel relations × 3 scales = 408
assert total_grammar() == 408

# Get all triangular relations
relations = get_all_triangular_relations()
for rel in relations[:5]:
    print(f"{rel.scale.name}: {rel.relation.forward}")
```

## Key Concepts

### Phoneme Classification

```python
from eye_of_horus import is_wheel_phoneme, is_spine_phoneme, classify_phoneme

is_wheel_phoneme('r')   # True - on the 16-position wheel
is_spine_phoneme('d')   # True - plain d is spine (DO)
is_wheel_phoneme('dj')  # True - palatalized dj is wheel (JUDGE)

classify_phoneme('k')   # 'spine-primary'
classify_phoneme('n')   # 'wheel'
```

### Hourglass Semantics

```python
from eye_of_horus import get_hourglass, Mode, Pole

hg = get_hourglass('r')  # Ra - ILLUMINE

# Get meaning at specific position
hg.get_meaning(Mode.MASCULINE, Pole.EQUILIBRIUM)  # 'ILLUMINE'
hg.get_meaning(Mode.FEMININE, Pole.EQUILIBRIUM)   # 'REVEAL'
hg.get_meaning(Mode.MASCULINE, Pole.MINIMA)       # 'OBSCURE'
hg.get_meaning(Mode.MASCULINE, Pole.MAXIMA)       # 'BLIND'
hg.get_meaning(Mode.FEMININE, Pole.MINIMA)        # 'CONCEAL'
hg.get_meaning(Mode.FEMININE, Pole.MAXIMA)        # 'EXPOSE'
```

## Data Source

The corpus comes from the [Thesaurus Linguae Aegyptiae](https://thesaurus-linguae-aegyptiae.de), 
containing 12,773 intact Earlier Egyptian sentences (Old Kingdom through Middle Kingdom).

Licensed CC BY-SA 4.0.

## Documentation

See `docs/analysis/` for detailed architectural documentation:
- `00-INDEX.md` - Document index
- `06-408-grammar-architecture.md` - The 408 grammar mathematics
- `10-spine-phonemes-as-scales.md` - Spine phonemes as reading scales
- `11-wheel-phoneme-correction.md` - True 16-phoneme wheel specification
- `12-layered-decode.md` - Five simultaneous readings

## Author

Nicholas David Brown  
Independent Researcher

## License

MIT
