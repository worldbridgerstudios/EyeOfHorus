"""
Pyramid Texts decoder using the 16-position wheel.

The Pyramid Texts of Unas (~2375-2345 BCE) are the oldest substantial
religious texts in Egyptian. This module provides phonemic decoding
using the wheel verb system.

Bidirectional reading:
- Forward (L→R): Ascending, cohering, unifying — becoming
- Reverse (R→L): Descending, decohering, dissolving — undoing
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from .corpus import Sentence, load_tla_corpus
from .mapping import WHEEL_VERBS, leiden_to_wheel, phonemes_to_verbs


# Cache for pyramid texts
_pyramid_texts: List[Sentence] = None


def get_pyramid_texts() -> List[Sentence]:
    """
    Get all Unas Pyramid Text sentences.
    
    These are dated -2375 to -2345 BCE, the reign of Unas,
    whose pyramid contains the oldest Pyramid Texts.
    
    Returns:
        List of Sentence objects in corpus order
    """
    global _pyramid_texts
    
    if _pyramid_texts is not None:
        return _pyramid_texts
    
    corpus = load_tla_corpus()
    
    # Filter for Unas reign specifically
    _pyramid_texts = [
        s for s in corpus
        if s.date_not_before == -2375 and s.date_not_after == -2345
    ]
    
    return _pyramid_texts


@dataclass
class DecodedLine:
    """A decoded line from the Pyramid Texts."""
    index: int
    hieroglyphs: str
    transliteration: str
    translation: str
    phonemes: List[str]
    verbs: List[str]
    trajectory: str


@dataclass
class BidirectionalLine:
    """A line decoded in both directions."""
    index: int
    hieroglyphs: str
    transliteration: str
    phonemes: List[str]
    
    # Forward (L→R): ascending, cohering
    forward_verbs: List[str]
    forward_trajectory: str
    
    # Reverse (R→L): descending, decohering  
    reverse_verbs: List[str]
    reverse_trajectory: str


def decode_bidirectional(
    start: int = 1,
    end: int = 9,
    verbose: bool = True
) -> Tuple[List[BidirectionalLine], str, str]:
    """
    Decode lines bidirectionally: forward (ascending) and reverse (descending).
    
    Args:
        start: First line (1-based)
        end: Last line (1-based, inclusive)
        verbose: Print results
        
    Returns:
        Tuple of:
        - List of BidirectionalLine objects
        - Forward paragraph (ascending/cohering)
        - Reverse paragraph (descending/decohering)
    """
    texts = get_pyramid_texts()
    
    # Convert to 0-based
    start_idx = start - 1
    end_idx = end  # end is inclusive, so end_idx = end for range()
    
    if start_idx >= len(texts):
        raise ValueError(f"Start line {start} exceeds corpus size {len(texts)}")
    
    end_idx = min(end_idx, len(texts))
    
    results = []
    all_forward_verbs = []
    all_reverse_verbs = []
    
    for i in range(start_idx, end_idx):
        s = texts[i]
        
        # Forward (L→R)
        forward_verbs = s.verbs
        forward_trajectory = ' → '.join(forward_verbs)
        
        # Reverse (R→L)
        reverse_verbs = list(reversed(s.verbs))
        reverse_trajectory = ' → '.join(reverse_verbs)
        
        decoded = BidirectionalLine(
            index=i,
            hieroglyphs=s.hieroglyphs,
            transliteration=s.transliteration,
            phonemes=s.phonemes,
            forward_verbs=forward_verbs,
            forward_trajectory=forward_trajectory,
            reverse_verbs=reverse_verbs,
            reverse_trajectory=reverse_trajectory,
        )
        results.append(decoded)
        all_forward_verbs.extend(forward_verbs)
        all_reverse_verbs.extend(reverse_verbs)
    
    # Build paragraphs
    forward_paragraph = build_paragraph(all_forward_verbs, "ascending")
    reverse_paragraph = build_paragraph(all_reverse_verbs, "descending")
    
    if verbose:
        print_bidirectional(results, forward_paragraph, reverse_paragraph, start, end_idx)
    
    return results, forward_paragraph, reverse_paragraph


def build_paragraph(verbs: List[str], mode: str) -> str:
    """
    Build a flowing paragraph from verb sequence.
    
    Joins verbs into natural-ish prose. Mode affects framing.
    """
    if not verbs:
        return ""
    
    # Group into clauses (chunks of ~5-7 verbs)
    clause_size = 6
    clauses = []
    
    for i in range(0, len(verbs), clause_size):
        chunk = verbs[i:i+clause_size]
        clause = '-'.join(v.lower() for v in chunk)
        clauses.append(clause)
    
    # Join clauses with punctuation
    if len(clauses) == 1:
        return clauses[0].capitalize() + "."
    
    # First clause capitalized, rest joined with commas, last with period
    result = clauses[0].capitalize()
    for clause in clauses[1:-1]:
        result += ", " + clause
    if len(clauses) > 1:
        result += "; " + clauses[-1] + "."
    
    return result


def print_bidirectional(
    results: List[BidirectionalLine],
    forward_para: str,
    reverse_para: str,
    start: int,
    end: int
):
    """Pretty-print bidirectional decode results."""
    
    print(f"\n{'='*70}")
    print(f"BIDIRECTIONAL DECODE: Lines {start}-{end}")
    print(f"{'='*70}")
    
    # Line-by-line
    for line in results:
        print(f"\n--- Line {line.index + 1} ({len(line.phonemes)} phonemes) ---")
        print(f"𓀀 {line.hieroglyphs[:60]}{'...' if len(line.hieroglyphs) > 60 else ''}")
        print(f"◯ {line.transliteration[:60]}{'...' if len(line.transliteration) > 60 else ''}")
        print(f"\n↗ ASCEND:  {line.forward_trajectory}")
        print(f"↙ DESCEND: {line.reverse_trajectory}")
    
    # Aggregate paragraphs
    print(f"\n{'='*70}")
    print("ASCENDING (Forward L→R)")
    print("Cohere • Unify • Become • Build")
    print(f"{'='*70}")
    print(f"\n{forward_para}")
    
    print(f"\n{'='*70}")
    print("DESCENDING (Reverse R→L)")
    print("Decohere • Dissolve • Undo • Return")
    print(f"{'='*70}")
    print(f"\n{reverse_para}")
    
    # Summary statistics
    total_phonemes = sum(len(line.phonemes) for line in results)
    print(f"\n{'='*70}")
    print(f"STATISTICS")
    print(f"{'='*70}")
    print(f"Lines: {len(results)}")
    print(f"Total phonemes: {total_phonemes}")
    print(f"Phonemes per line: {[len(line.phonemes) for line in results]}")
    
    # Check for Fibonacci 1+2+3+2+1=9 structure
    if len(results) == 9:
        fib_struct = [1, 2, 3, 2, 1]
        print(f"\n9-line Fibonacci breath: {' + '.join(map(str, fib_struct))} = 9")


def decode(n: int, start: int = 0, verbose: bool = True) -> List[DecodedLine]:
    """
    Decode N lines from the Pyramid Texts starting at index `start`.
    
    Args:
        n: Number of lines to decode
        start: Starting index (0-based). Default 0 = first lines.
        verbose: If True, print results as we go
        
    Returns:
        List of DecodedLine objects
    """
    texts = get_pyramid_texts()
    
    if start >= len(texts):
        raise ValueError(f"Start index {start} exceeds corpus size {len(texts)}")
    
    end = min(start + n, len(texts))
    
    results = []
    all_phonemes = []
    all_verbs = []
    
    for i in range(start, end):
        s = texts[i]
        
        decoded = DecodedLine(
            index=i,
            hieroglyphs=s.hieroglyphs,
            transliteration=s.transliteration,
            translation=s.translation,
            phonemes=s.phonemes,
            verbs=s.verbs,
            trajectory=s.trajectory,
        )
        results.append(decoded)
        all_phonemes.extend(s.phonemes)
        all_verbs.extend(s.verbs)
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"LINE {i+1}")
            print(f"{'='*60}")
            print(f"𓀀 {s.hieroglyphs}")
            print(f"◯ {s.transliteration}")
            print(f"→ {s.translation}")
            print(f"\nPHONEMES: {' '.join(s.phonemes)}")
            print(f"VERBS: {s.trajectory}")
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"AGGREGATE: Lines {start+1}-{end}")
        print(f"{'='*60}")
        print(f"Total phonemes: {len(all_phonemes)}")
        print(f"\nCOMBINED STREAM:")
        # Show in chunks of 20
        for i in range(0, len(all_verbs), 10):
            chunk = all_verbs[i:i+10]
            print(f"  {i+1:3}-{i+len(chunk):3}: {' → '.join(chunk)}")
        
        # Frequency analysis
        from collections import Counter
        freq = Counter(all_phonemes)
        print(f"\nFREQUENCY (n={len(all_phonemes)}):")
        for p, count in freq.most_common():
            pct = 100 * count / len(all_phonemes)
            verb = WHEEL_VERBS.get(p, '?')
            print(f"  {p:3} ({verb:10}): {count:3} ({pct:5.1f}%)")
    
    return results


def decode_range(start: int, end: int, verbose: bool = True) -> List[DecodedLine]:
    """
    Decode lines from start to end (inclusive).
    
    Args:
        start: First line (1-based for human readability)
        end: Last line (1-based, inclusive)
        verbose: Print results
        
    Returns:
        List of DecodedLine objects
    """
    # Convert to 0-based
    return decode(end - start + 1, start - 1, verbose)


if __name__ == '__main__':
    # Decode first 9 lines bidirectionally (Fibonacci breath block)
    decode_bidirectional(1, 9)
