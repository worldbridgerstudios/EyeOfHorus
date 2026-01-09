"""
Tests for spine phoneme integration.

Tests cover:
- SpinePhoneme enum
- Scale ↔ spine linkage
- TriangularRelation structure
- 408 triangular relation generation
- Phoneme classification (wheel vs spine)
"""

import pytest
from eye_of_horus.engine import (
    SpinePhoneme,
    Scale,
    TriangularRelation,
    Relation,
    WHEEL_PHONEMES,
    SPINE_PRIMARY,
    SPINE_SECONDARY,
    SPINE_ALL,
    generate_relations,
    generate_all_triangular_relations,
    get_all_triangular_relations,
    count_triangular_relations,
    is_wheel_phoneme,
    is_spine_phoneme,
    classify_phoneme,
    triangular,
    count_relations,
    total_grammar,
)


class TestSpinePhonemes:
    """Tests for spine phoneme constants."""
    
    def test_spine_primary_count(self):
        """3 primary spine phonemes: x, d, k."""
        assert len(SPINE_PRIMARY) == 3
        assert SPINE_PRIMARY == ['x', 'd', 'k']
    
    def test_spine_secondary(self):
        """Secondary spine phonemes include q, tj, g, f."""
        assert 'q' in SPINE_SECONDARY
        assert 'tj' in SPINE_SECONDARY
        assert 'g' in SPINE_SECONDARY
        assert 'f' in SPINE_SECONDARY
    
    def test_spine_all(self):
        """SPINE_ALL = primary + secondary."""
        assert set(SPINE_ALL) == set(SPINE_PRIMARY + SPINE_SECONDARY)
    
    def test_spine_not_in_wheel(self):
        """Primary spine phonemes (x) not in wheel."""
        for spine in SPINE_PRIMARY:
            if spine not in ['d', 'k']:  # d and k are in BOTH
                assert spine not in WHEEL_PHONEMES


class TestSpinePhonemeEnum:
    """Tests for SpinePhoneme enum."""
    
    def test_three_spine_phonemes(self):
        """Three spine phoneme enums: K, D, X."""
        assert len(SpinePhoneme) == 3
    
    def test_spine_phoneme_values(self):
        """Each spine phoneme has phoneme, verb, and decan_count."""
        assert SpinePhoneme.K.phoneme == 'k'
        assert SpinePhoneme.D.phoneme == 'd'
        assert SpinePhoneme.X.phoneme == 'x'
    
    def test_spine_phoneme_verbs(self):
        """Spine phonemes have correct verbs."""
        assert SpinePhoneme.K.verb == 'CYCLE'
        assert SpinePhoneme.D.verb == 'DO'
        assert SpinePhoneme.X.verb == 'FUNDAMENT'
    
    def test_spine_decan_counts(self):
        """Spine phoneme decan counts from paper."""
        assert SpinePhoneme.K.decan_count == 5
        assert SpinePhoneme.D.decan_count == 10
        assert SpinePhoneme.X.decan_count == 17


class TestScaleSpineLinkage:
    """Tests for Scale ↔ spine phoneme linkage."""
    
    def test_scale_links_to_spine(self):
        """Each scale is linked to a spine phoneme."""
        assert Scale.ONTOGENIC.spine == SpinePhoneme.K
        assert Scale.PHYLOGENIC.spine == SpinePhoneme.D
        assert Scale.COSMOGENIC.spine == SpinePhoneme.X
    
    def test_scale_phoneme_shortcut(self):
        """Scale.phoneme returns spine phoneme string."""
        assert Scale.ONTOGENIC.phoneme == 'k'
        assert Scale.PHYLOGENIC.phoneme == 'd'
        assert Scale.COSMOGENIC.phoneme == 'x'
    
    def test_scale_verb_shortcut(self):
        """Scale.verb returns spine verb."""
        assert Scale.ONTOGENIC.verb == 'CYCLE'
        assert Scale.PHYLOGENIC.verb == 'DO'
        assert Scale.COSMOGENIC.verb == 'FUNDAMENT'


class TestTriangularRelation:
    """Tests for TriangularRelation structure."""
    
    def test_triangular_relation_creation(self):
        """TriangularRelation stores wheel phonemes and scale."""
        rel = TriangularRelation('r', 'n', Scale.ONTOGENIC)
        assert rel.phoneme_a == 'r'
        assert rel.phoneme_b == 'n'
        assert rel.scale == Scale.ONTOGENIC
    
    def test_triangular_relation_spine(self):
        """TriangularRelation exposes spine phoneme."""
        rel = TriangularRelation('r', 'n', Scale.ONTOGENIC)
        assert rel.spine_phoneme == 'k'
        assert rel.spine_verb == 'CYCLE'
    
    def test_triangular_relation_verbs(self):
        """TriangularRelation verbs from wheel phonemes."""
        rel = TriangularRelation('r', 'n', Scale.ONTOGENIC)
        assert rel.verb_a == 'ILLUMINE'
        assert rel.verb_b == 'WEAVE'
    
    def test_self_relation(self):
        """Self-relations detected correctly."""
        self_rel = TriangularRelation('r', 'r', Scale.COSMOGENIC)
        assert self_rel.is_self_relation
        
        other_rel = TriangularRelation('r', 'n', Scale.COSMOGENIC)
        assert not other_rel.is_self_relation
    
    def test_description(self):
        """Description is human-readable."""
        rel = TriangularRelation('r', 'n', Scale.ONTOGENIC)
        assert 'ILLUMINE' in rel.description
        assert 'WEAVE' in rel.description
        assert 'ontogenic' in rel.description
        
        self_rel = TriangularRelation('r', 'r', Scale.COSMOGENIC)
        assert 'ILLUMINE' in self_rel.description
        assert 'cosmogenic' in self_rel.description


class TestTriangularRelationGeneration:
    """Tests for 408 triangular relation generation."""
    
    def test_count_triangular_relations(self):
        """408 total triangular relations."""
        assert count_triangular_relations() == 408
    
    def test_generate_all_triangular_relations(self):
        """Generator produces 408 relations."""
        count = sum(1 for _ in generate_all_triangular_relations())
        assert count == 408
    
    def test_get_all_triangular_relations(self):
        """List has 408 relations."""
        relations = get_all_triangular_relations()
        assert len(relations) == 408
    
    def test_all_scales_represented(self):
        """Each scale appears in triangular relations."""
        relations = get_all_triangular_relations()
        scales_found = set(rel.scale for rel in relations)
        assert scales_found == set(Scale)
    
    def test_scale_distribution(self):
        """Each scale has 136 relations."""
        relations = get_all_triangular_relations()
        for scale in Scale:
            scale_count = sum(1 for rel in relations if rel.scale == scale)
            assert scale_count == 136
    
    def test_408_equals_136_times_3(self):
        """408 = 136 wheel relations × 3 spine scales."""
        assert count_relations() == 136
        assert len(Scale) == 3
        assert count_triangular_relations() == 136 * 3


class TestPhonemeClassification:
    """Tests for phoneme classification functions."""
    
    def test_is_wheel_phoneme(self):
        """Wheel phonemes correctly identified."""
        assert is_wheel_phoneme('a')
        assert is_wheel_phoneme('r')
        assert is_wheel_phoneme('n')
        assert not is_wheel_phoneme('x')  # Primary spine
        assert not is_wheel_phoneme('q')  # Secondary spine
    
    def test_is_spine_phoneme(self):
        """Spine phonemes correctly identified."""
        assert is_spine_phoneme('x')
        assert is_spine_phoneme('d')
        assert is_spine_phoneme('k')
        assert is_spine_phoneme('q')
        assert is_spine_phoneme('tj')
        assert not is_spine_phoneme('a')  # Wheel only
    
    def test_classify_phoneme(self):
        """Phoneme classification works."""
        assert classify_phoneme('a') == 'wheel'
        assert classify_phoneme('r') == 'wheel'
        assert classify_phoneme('x') == 'spine-primary'
        assert classify_phoneme('q') == 'spine-secondary'
        assert classify_phoneme('tj') == 'spine-secondary'
        assert classify_phoneme('xyz') == 'unknown'
    
    def test_d_and_k_classification(self):
        """d and k are spine phonemes, dj is on wheel."""
        # Plain d and k are spine phonemes (scales)
        assert is_spine_phoneme('d')
        assert is_spine_phoneme('k')
        assert not is_wheel_phoneme('d')
        assert not is_wheel_phoneme('k')
        # Palatalized dj is on wheel
        assert is_wheel_phoneme('dj')
        assert not is_spine_phoneme('dj')
        # Classification
        assert classify_phoneme('d') == 'spine-primary'
        assert classify_phoneme('k') == 'spine-primary'
        assert classify_phoneme('dj') == 'wheel'


class TestRelationSelfRelations:
    """Tests for self-relations in the 136 count."""
    
    def test_basic_relation_self_check(self):
        """Basic Relation detects self-relations."""
        self_rel = Relation('r', 'r')
        assert self_rel.is_self_relation
        assert self_rel.verb_a == self_rel.verb_b
        
        other_rel = Relation('r', 'n')
        assert not other_rel.is_self_relation
    
    def test_self_relations_count_16(self):
        """16 self-relations in the 136."""
        relations = generate_relations()
        self_count = sum(1 for a, b in relations if a == b)
        assert self_count == 16
    
    def test_distinct_pairs_count_120(self):
        """120 distinct pairs in the 136."""
        relations = generate_relations()
        distinct_count = sum(1 for a, b in relations if a != b)
        assert distinct_count == 120
    
    def test_136_equals_16_plus_120(self):
        """136 = 16 self + 120 distinct."""
        assert 16 + 120 == 136
        assert triangular(16) == 136


class TestIntegrationMathematics:
    """Integration tests for the complete grammar mathematics."""
    
    def test_wheel_count(self):
        """16 wheel phonemes."""
        assert len(WHEEL_PHONEMES) == 16
    
    def test_spine_count(self):
        """3 primary spine phonemes."""
        assert len(SPINE_PRIMARY) == 3
    
    def test_relations_formula(self):
        """T(16) = 136 from formula."""
        n = 16
        expected = n * (n + 1) // 2
        assert expected == 136
        assert triangular(16) == 136
    
    def test_total_grammar_formula(self):
        """408 = 136 × 3."""
        assert total_grammar() == 408
        assert count_relations() * len(Scale) == 408
        assert 136 * 3 == 408
