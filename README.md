# Eye of Horus 𓂀

Read ancient Egyptian through the 16-position phonemic wheel.

## The Wheel

Each Egyptian phoneme maps to a fundamental verb:

| Phoneme | Deity   | Verb      |
|---------|---------|-----------|
| p       | Ptah    | FORM      |
| t       | Thoth   | MEASURE   |
| kh      | Khnum   | MOLD      |
| s       | Sokar   | BIND      |
| n       | Neith   | WEAVE     |
| r       | Ra      | ILLUMINE  |
| a       | Atum    | SOURCE    |
| h       | Horus   | SIGHT     |
| m       | Min     | GENERATE  |
| w       | Wadjet  | PROTECT   |
| b       | Bast    | REFINE    |
| k       | Khonsu  | CYCLE     |
| g       | Geb     | GROUND    |
| d       | Duat    | TRANSFORM |
| f       | -       | BREATHE   |
| sh      | Shu     | LIFT      |

## Installation

```bash
pip install eye-of-horus
```

For corpus access (12,773 Earlier Egyptian sentences):
```bash
pip install eye-of-horus[corpus]
```

## Usage

```python
from eye_of_horus import leiden_to_wheel, load_tla_corpus
from eye_of_horus.mapping import wheel_trajectory, WHEEL_VERBS

# Convert transliteration to phoneme sequence
phonemes = leiden_to_wheel("ꜥḥꜥ")  # "Stand up!"
# ['a', 'h', 'a']

# Get semantic trajectory
trajectory = wheel_trajectory("ꜥḥꜥ")
# "SOURCE → SIGHT → SOURCE"

# Search the corpus
corpus = load_tla_corpus()
for sent in corpus[:5]:
    print(f"{sent.transliteration}: {sent.trajectory}")
```

## Data Source

The corpus comes from the [Thesaurus Linguae Aegyptiae](https://thesaurus-linguae-aegyptiae.de), 
containing 12,773 intact Earlier Egyptian sentences (Old Kingdom through Middle Kingdom).

Licensed CC BY-SA 4.0.

## Author

Nicholas David Brown  
Independent Researcher

## License

MIT
