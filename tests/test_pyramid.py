"""
Tests for Pyramid Texts decoder.

Tests cover:
- get_pyramid_texts corpus loading
- decode function (unidirectional)
- decode_bidirectional (both directions)
- BidirectionalLine structure
"""

import pytest
from eye_of_horus.pyramid import (
    get_pyramid_texts,
    decode,
    decode_range,
    decode_bidirectional,
    DecodedLine,
    BidirectionalLine,
)


class TestPyramidTextsLoading:
    """Tests for corpus loading."""
    
    def test_get_pyramid_texts_returns_list(self):
        """get_pyramid_texts returns a list."""
        texts = get_pyramid_texts()
        assert isinstance(texts, list)
    
    def test_pyramid_texts_not_empty(self):
        """Corpus has content."""
        texts = get_pyramid_texts()
        assert len(texts) > 0
    
    def test_texts_have_phonemes(self):
        """Each text has phonemes extracted."""
        texts = get_pyramid_texts()
        for text in texts[:10]:  # Check first 10
            assert hasattr(text, 'phonemes')
            assert isinstance(text.phonemes, list)


class TestDecode:
    """Tests for unidirectional decode."""
    
    def test_decode_returns_list(self):
        """decode returns list of DecodedLine."""
        results = decode(3, 0, verbose=False)
        assert isinstance(results, list)
        assert len(results) == 3
    
    def test_decoded_line_structure(self):
        """DecodedLine has expected fields."""
        results = decode(1, 0, verbose=False)
        line = results[0]
        assert hasattr(line, 'index')
        assert hasattr(line, 'phonemes')
        assert hasattr(line, 'verbs')
        assert hasattr(line, 'trajectory')
    
    def test_decode_range(self):
        """decode_range works with 1-based indices."""
        results = decode_range(1, 3, verbose=False)
        assert len(results) == 3
        assert results[0].index == 0  # Internal index is 0-based


class TestBidirectionalDecode:
    """Tests for bidirectional decode."""
    
    def test_returns_tuple(self):
        """decode_bidirectional returns tuple of (lines, forward, reverse)."""
        result = decode_bidirectional(1, 3, verbose=False)
        assert isinstance(result, tuple)
        assert len(result) == 3
    
    def test_returns_lines(self):
        """First element is list of BidirectionalLine."""
        lines, _, _ = decode_bidirectional(1, 3, verbose=False)
        assert isinstance(lines, list)
        assert len(lines) == 3
        for line in lines:
            assert isinstance(line, BidirectionalLine)
    
    def test_returns_paragraphs(self):
        """Second and third elements are paragraph strings."""
        _, forward, reverse = decode_bidirectional(1, 3, verbose=False)
        assert isinstance(forward, str)
        assert isinstance(reverse, str)
        assert len(forward) > 0
        assert len(reverse) > 0
    
    def test_bidirectional_line_structure(self):
        """BidirectionalLine has forward and reverse verbs."""
        lines, _, _ = decode_bidirectional(1, 1, verbose=False)
        line = lines[0]
        
        assert hasattr(line, 'forward_verbs')
        assert hasattr(line, 'reverse_verbs')
        assert hasattr(line, 'forward_trajectory')
        assert hasattr(line, 'reverse_trajectory')
    
    def test_reverse_is_reversed(self):
        """Reverse verbs are the forward verbs reversed."""
        lines, _, _ = decode_bidirectional(1, 1, verbose=False)
        line = lines[0]
        
        assert line.reverse_verbs == list(reversed(line.forward_verbs))
    
    def test_nine_lines_fibonacci(self):
        """First 9 lines work (Fibonacci breath block)."""
        lines, forward, reverse = decode_bidirectional(1, 9, verbose=False)
        assert len(lines) == 9
        
        # Check phoneme counts match expected pattern
        counts = [len(line.phonemes) for line in lines]
        assert len(counts) == 9
        assert all(c > 0 for c in counts)


class TestLine1Specifics:
    """Tests for Line 1 (the seed line with 23 phonemes)."""
    
    def test_line1_phoneme_count(self):
        """Line 1 has 23 phonemes."""
        lines, _, _ = decode_bidirectional(1, 1, verbose=False)
        assert len(lines[0].phonemes) == 23
    
    def test_line1_ends_double_illumine(self):
        """Line 1 forward ends with ILLUMINE → ILLUMINE."""
        lines, _, _ = decode_bidirectional(1, 1, verbose=False)
        verbs = lines[0].forward_verbs
        assert verbs[-1] == 'ILLUMINE'
        assert verbs[-2] == 'ILLUMINE'
    
    def test_line1_reverse_starts_double_illumine(self):
        """Line 1 reverse starts with ILLUMINE → ILLUMINE."""
        lines, _, _ = decode_bidirectional(1, 1, verbose=False)
        verbs = lines[0].reverse_verbs
        assert verbs[0] == 'ILLUMINE'
        assert verbs[1] == 'ILLUMINE'


class TestLine8Specifics:
    """Tests for Line 8 (has spine phonemes d and k)."""
    
    def test_line8_has_spine_phonemes(self):
        """Line 8 contains d and k (spine phonemes)."""
        lines, _, _ = decode_bidirectional(8, 8, verbose=False)
        phonemes = lines[0].phonemes
        # Line 8: rḏ.t qbḥ(.w) → r, d, t, k, b, h
        # Based on output: ILLUMINE → DO → MEASURE → CYCLE → BIRTH → SEE
        verbs = lines[0].forward_verbs
        assert 'DO' in verbs  # d phoneme
        assert 'CYCLE' in verbs  # k phoneme


class TestParagraphBuilding:
    """Tests for paragraph construction."""
    
    def test_paragraphs_contain_verbs(self):
        """Paragraphs contain verb content."""
        _, forward, reverse = decode_bidirectional(1, 3, verbose=False)
        
        # Should contain lowercased verbs
        assert 'source' in forward.lower() or 'bind' in forward.lower()
        assert 'source' in reverse.lower() or 'illumine' in reverse.lower()
    
    def test_paragraphs_different(self):
        """Forward and reverse paragraphs are different."""
        _, forward, reverse = decode_bidirectional(1, 3, verbose=False)
        assert forward != reverse
