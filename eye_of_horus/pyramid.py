"""
Pyramid Texts decoder using the 16-position wheel.

The Pyramid Texts of Unas (~2375-2345 BCE) are the oldest substantial
religious texts in Egyptian. This module provides phonemic decoding
using the wheel verb system.
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
    # Decode first 10 lines
    decode(10)
