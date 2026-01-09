"""
Tests for Fibonacci rhythm and breath module.

Tests cover:
- Golden ratio calculations
- Phi boundary detection
- Yuga boundary detection
- Breath phase tracking
- Script health scoring
- Fibonacci segmentation
"""

import pytest
import math
from eye_of_horus.rhythm import (
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


class TestGoldenRatio:
    """Tests for golden ratio constants."""
    
    def test_phi_value(self):
        """PHI ≈ 1.618."""
        assert abs(PHI - 1.618033988749895) < 1e-10
    
    def test_phi_inverse(self):
        """PHI_INV ≈ 0.618."""
        assert abs(PHI_INV - 0.618033988749895) < 1e-10
    
    def test_phi_relationship(self):
        """PHI * PHI_INV = 1."""
        assert abs(PHI * PHI_INV - 1.0) < 1e-10
    
    def test_phi_property(self):
        """PHI = 1 + 1/PHI (defining property)."""
        assert abs(PHI - (1 + 1/PHI)) < 1e-10


class TestFibonacciSequence:
    """Tests for Fibonacci sequence."""
    
    def test_fibonacci_start(self):
        """First Fibonacci numbers correct."""
        assert FIBONACCI[:7] == [1, 1, 2, 3, 5, 8, 13]
    
    def test_fibonacci_function(self):
        """fibonacci() returns correct values."""
        assert fibonacci(0) == 1
        assert fibonacci(1) == 1
        assert fibonacci(2) == 2
        assert fibonacci(3) == 3
        assert fibonacci(4) == 5
        assert fibonacci(5) == 8
    
    def test_fibonacci_large(self):
        """fibonacci() works for larger indices."""
        assert fibonacci(10) == 89
        assert fibonacci(11) == 144
    
    def test_fibonacci_property(self):
        """F(n) = F(n-1) + F(n-2)."""
        for i in range(2, 10):
            assert fibonacci(i) == fibonacci(i-1) + fibonacci(i-2)


class TestPhiBoundaries:
    """Tests for phi boundary detection."""
    
    def test_empty_sequence(self):
        """Empty/single phoneme returns no boundaries."""
        assert detect_phi_boundaries(0) == []
        assert detect_phi_boundaries(1) == []
    
    def test_line1_boundaries(self):
        """Line 1 (23 phonemes) has phi boundaries."""
        bounds = detect_phi_boundaries(23)
        assert len(bounds) > 0
        # First boundary should be near 23 * 0.618 ≈ 14
        assert any(abs(b - 14) <= 2 for b in bounds)
    
    def test_boundaries_ascending(self):
        """Boundaries should be in ascending order."""
        for length in [10, 15, 20, 25, 30]:
            bounds = detect_phi_boundaries(length)
            assert bounds == sorted(bounds)
    
    def test_boundaries_within_range(self):
        """All boundaries within sequence length."""
        for length in [10, 15, 20, 25, 30]:
            bounds = detect_phi_boundaries(length)
            for b in bounds:
                assert 0 < b < length


class TestYugaBoundaries:
    """Tests for Yuga boundary detection (4:3:2:1)."""
    
    def test_line1_yugas(self):
        """Line 1 (23 phonemes) maps to Yuga ratios."""
        yugas = detect_yuga_boundaries(23)
        
        assert 'satya' in yugas
        assert 'treta' in yugas
        assert 'dvapara' in yugas
        assert 'kali' in yugas
    
    def test_yuga_ratios(self):
        """Yuga sizes follow 4:3:2:1 ratio."""
        yugas = detect_yuga_boundaries(100)
        
        satya_size = yugas['satya'][1] - yugas['satya'][0]
        treta_size = yugas['treta'][1] - yugas['treta'][0]
        dvapara_size = yugas['dvapara'][1] - yugas['dvapara'][0]
        kali_size = yugas['kali'][1] - yugas['kali'][0]
        
        # Should be approximately 40:30:20:10
        assert abs(satya_size - 40) <= 1
        assert abs(treta_size - 30) <= 1
        assert abs(dvapara_size - 20) <= 1
        assert abs(kali_size - 10) <= 1
    
    def test_yugas_cover_sequence(self):
        """Yugas should cover entire sequence without gaps."""
        length = 23
        yugas = detect_yuga_boundaries(length)
        
        assert yugas['satya'][0] == 0
        assert yugas['kali'][1] == length
        
        # No gaps
        assert yugas['satya'][1] == yugas['treta'][0]
        assert yugas['treta'][1] == yugas['dvapara'][0]
        assert yugas['dvapara'][1] == yugas['kali'][0]


class TestBreathPhase:
    """Tests for breath phase detection."""
    
    def test_nine_line_structure(self):
        """9-line block has correct breath phases."""
        assert detect_breath_phase(1, 9) == BreathPhase.SEED
        assert detect_breath_phase(2, 9) == BreathPhase.EXHALE
        assert detect_breath_phase(3, 9) == BreathPhase.EXHALE
        assert detect_breath_phase(4, 9) == BreathPhase.PIVOT
        assert detect_breath_phase(5, 9) == BreathPhase.PIVOT
        assert detect_breath_phase(6, 9) == BreathPhase.PIVOT
        assert detect_breath_phase(7, 9) == BreathPhase.INHALE
        assert detect_breath_phase(8, 9) == BreathPhase.INHALE
        assert detect_breath_phase(9, 9) == BreathPhase.RETURN
    
    def test_fibonacci_structure(self):
        """Line counts match Fibonacci: 1+2+3+2+1=9."""
        structure = get_fibonacci_line_structure()
        
        assert len(structure['seed']) == 1
        assert len(structure['exhale']) == 2
        assert len(structure['pivot']) == 3
        assert len(structure['inhale']) == 2
        assert len(structure['return']) == 1
        
        total = sum(len(v) for v in structure.values())
        assert total == 9
    
    def test_breath_phases_enum(self):
        """All breath phases have correct values."""
        assert BreathPhase.SEED.value == "seed"
        assert BreathPhase.EXHALE.value == "exhale"
        assert BreathPhase.PIVOT.value == "pivot"
        assert BreathPhase.INHALE.value == "inhale"
        assert BreathPhase.RETURN.value == "return"


class TestScriptHealth:
    """Tests for script health scoring."""
    
    def test_hieroglyph_highest(self):
        """Hieroglyph attestation = highest score."""
        health = score_script_health(hieroglyph_attested=True)
        assert health == ScriptHealth.HIEROGLYPH_ATTESTED
        assert health.value == 3
    
    def test_hieratic_medium(self):
        """Hieratic attestation = medium score."""
        health = score_script_health(hieratic_attested=True)
        assert health == ScriptHealth.HIERATIC_ATTESTED
        assert health.value == 2
    
    def test_coptic_low(self):
        """Coptic-only = low score."""
        health = score_script_health(coptic_attested=True)
        assert health == ScriptHealth.COPTIC_ONLY
        assert health.value == 1
    
    def test_unknown_zero(self):
        """No attestation = unknown."""
        health = score_script_health()
        assert health == ScriptHealth.UNKNOWN
        assert health.value == 0
    
    def test_hieroglyph_trumps_others(self):
        """Hieroglyph attestation trumps other levels."""
        health = score_script_health(
            hieroglyph_attested=True,
            hieratic_attested=True,
            coptic_attested=True
        )
        assert health == ScriptHealth.HIEROGLYPH_ATTESTED
    
    def test_health_ordering(self):
        """Health scores are properly ordered."""
        assert ScriptHealth.HIEROGLYPH_ATTESTED.value > ScriptHealth.HIERATIC_ATTESTED.value
        assert ScriptHealth.HIERATIC_ATTESTED.value > ScriptHealth.COPTIC_ONLY.value
        assert ScriptHealth.COPTIC_ONLY.value > ScriptHealth.UNKNOWN.value


class TestScriptRatios:
    """Tests for script breath ratios."""
    
    def test_hieroglyph_hieratic_unity(self):
        """Hieroglyph:Hieratic = 1:1 (unity)."""
        ratio = SCRIPT_RATIOS['hieroglyph_to_hieratic']
        assert ratio == (1, 1)
    
    def test_hieratic_coptic_division(self):
        """Hieratic:Coptic = 1:2 (division)."""
        ratio = SCRIPT_RATIOS['hieratic_to_coptic']
        assert ratio == (1, 2)
    
    def test_fibonacci_seed(self):
        """Sequence is Fibonacci seed: 1, 1, 2."""
        assert SCRIPT_RATIOS['sequence'] == [1, 1, 2]


class TestPhiBoundaryCheck:
    """Tests for is_at_phi_boundary."""
    
    def test_at_boundary(self):
        """Position at boundary returns True."""
        # For 23 phonemes, boundary near 14
        bounds = detect_phi_boundaries(23)
        for b in bounds:
            assert is_at_phi_boundary(b, 23)
    
    def test_not_at_boundary(self):
        """Position away from boundary returns False."""
        # Position 1 should not be at any boundary for length 23
        assert not is_at_phi_boundary(1, 23, tolerance=0.5)
    
    def test_tolerance(self):
        """Tolerance affects boundary detection."""
        bounds = detect_phi_boundaries(23)
        if bounds:
            b = bounds[0]
            assert is_at_phi_boundary(b + 1, 23, tolerance=1.5)
            assert not is_at_phi_boundary(b + 3, 23, tolerance=0.5)


class TestFibonacciSegmentation:
    """Tests for segment_by_fibonacci."""
    
    def test_empty_sequence(self):
        """Empty sequence returns empty."""
        assert segment_by_fibonacci([]) == []
    
    def test_segments_cover_all(self):
        """Segments should contain all original items."""
        items = list(range(23))
        segments = segment_by_fibonacci(items)
        
        # Flatten and check
        flat = [item for seg in segments for item in seg]
        assert flat == items
    
    def test_segments_non_empty(self):
        """All segments should be non-empty."""
        items = list(range(23))
        segments = segment_by_fibonacci(items)
        
        for seg in segments:
            assert len(seg) > 0
    
    def test_segment_count_limited(self):
        """Segment count respects max_segments."""
        items = list(range(50))
        segments = segment_by_fibonacci(items, max_segments=3)
        
        assert len(segments) <= 3


class TestLineRhythmAnalysis:
    """Tests for analyze_line_rhythm."""
    
    def test_analysis_keys(self):
        """Analysis returns expected keys."""
        phonemes = ['a', 'b', 'r', 'k', 'd']
        analysis = analyze_line_rhythm(phonemes)
        
        assert 'total_phonemes' in analysis
        assert 'phi_boundaries' in analysis
        assert 'yuga_boundaries' in analysis
        assert 'phi_segments' in analysis
        assert 'segment_sizes' in analysis
    
    def test_line1_analysis(self):
        """Line 1 (23 phonemes) analysis is coherent."""
        # Simulate Line 1 phonemes
        phonemes = ['s', 'a', 'r', 'w', 'n', 'a', 's', 'm', 'n', 'a', 
                    'r', 't', 'h', 'r', 'w', 'a', 'a', 'b', 'n', 's', 
                    'a', 'r', 'r']
        
        analysis = analyze_line_rhythm(phonemes)
        
        assert analysis['total_phonemes'] == 23
        assert len(analysis['phi_boundaries']) > 0
        assert 'satya' in analysis['yuga_boundaries']
        assert sum(analysis['segment_sizes']) == 23


class TestLine1YugaMapping:
    """Integration tests for Line 1 Yuga mapping."""
    
    def test_satya_boundary(self):
        """Satya ends near position 9 (23 * 0.4 = 9.2)."""
        yugas = detect_yuga_boundaries(23)
        satya_end = yugas['satya'][1]
        assert abs(satya_end - 9) <= 1
    
    def test_kali_ends_double_illumine(self):
        """Kali (positions 22-23) = ILLUMINE ILLUMINE."""
        yugas = detect_yuga_boundaries(23)
        kali_start = yugas['kali'][0]
        # Should be near position 21 (0-indexed)
        assert kali_start >= 20
