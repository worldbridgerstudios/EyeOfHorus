# Eye of Horus - Egyptian Phonemic Analysis
# For reading ancient Egyptian through the 16-position wheel
#
# Engine: 16 wheel phonemes × 3 spine axes = 408 grammar (T(16) × 3)

__version__ = "0.3.0"

# Core mapping (Leiden → wheel phonemes)
from .mapping import (
    leiden_to_wheel,
    WHEEL_16,
    LEIDEN_TO_WHEEL,
    WHEEL_VERBS,
    phonemes_to_verbs,
)

# Hourglass engine (full semantic architecture)
from .engine import (
    # Enums
    Mode,
    Pole,
    Scale,
    SpinePhoneme,
    # Data structures
    Hourglass,
    Relation,
    TriangularRelation,
    # Phoneme data
    PHONEME_HOURGLASSES,
    PHONEME_ORDER,
    WHEEL_PHONEMES,
    SPINE_PRIMARY,
    SPINE_SECONDARY,
    SPINE_ALL,
    # Functions
    get_hourglass,
    get_core_verb,
    triangular,
    generate_relations,
    count_relations,
    get_all_relations,
    total_grammar,
    generate_all_triangular_relations,
    get_all_triangular_relations,
    count_triangular_relations,
    detect_mode,
    decode_with_mode,
    decode_trajectory,
    is_wheel_phoneme,
    is_spine_phoneme,
    classify_phoneme,
)

# Corpus access
from .corpus import (
    load_tla_corpus,
    search_corpus,
    Sentence,
)

# Validation tools
from .validation import (
    oldest_sentences,
    test_oldest_sentences,
    test_causal_coherence,
    DirectionTest,
    find_markers,
    show_sentence_detail,
)

# Pyramid Texts
from .pyramid import (
    get_pyramid_texts,
    decode,
    decode_range,
    decode_bidirectional,
    DecodedLine,
    BidirectionalLine,
)

# Fibonacci Rhythm & Breath
from .rhythm import (
    PHI,
    PHI_INV,
    FIBONACCI,
    BreathPhase,
    ScriptHealth,
    fibonacci,
    detect_phi_boundaries,
    detect_yuga_boundaries,
    detect_breath_phase,
    score_script_health,
    get_fibonacci_line_structure,
    is_at_phi_boundary,
    segment_by_fibonacci,
    analyze_line_rhythm,
    SCRIPT_RATIOS,
)
