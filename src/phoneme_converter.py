"""
Phoneme Conversion Module for MR.ZPAYTZO-rev0
Implements 1986-era grapheme-to-phoneme conversion using rule-based algorithms
"""

import re
from typing import List, Dict, Tuple


class PhonemeConverter:
    """
    Grapheme-to-phoneme converter implementing vintage TTS phonetic rules.
    Based on 1986 rule-based algorithms used in First Byte Monologue engine.
    
    Uses simplified ARPABET-style phonetic notation for compatibility
    with diphone concatenation synthesis.
    """
    
    def __init__(self):
        self.vowel_rules = self._load_vowel_rules()
        self.consonant_rules = self._load_consonant_rules()
        self.digraph_rules = self._load_digraph_rules()
        self.exception_words = self._load_exception_words()
        self.syllable_patterns = self._load_syllable_patterns()
    
    def convert(self, text: str) -> List[str]:
        """
        Convert normalized text to phoneme sequence.
        
        Args:
            text: Normalized text from TextProcessor
            
        Returns:
            List of phonemes in ARPABET-style notation
        """
        phonemes = []
        words = text.split()
        
        for word in words:
            word_phonemes = self._convert_word(word)
            phonemes.extend(word_phonemes)
            
        return phonemes
    
    def _convert_word(self, word: str) -> List[str]:
        """Convert a single word to phonemes."""
        # Handle pause markers
        if word.startswith('<PAUSE'):
            return [word]  # Preserve pause markers
        
        # Remove punctuation for phonetic processing
        clean_word = re.sub(r'[^\w]', '', word.upper())
        
        if not clean_word:
            return []
        
        # Check exception dictionary first
        if clean_word in self.exception_words:
            return self.exception_words[clean_word]
        
        # Apply rule-based conversion
        phonemes = self._apply_phoneme_rules(clean_word)
        
        return phonemes
    
    def _apply_phoneme_rules(self, word: str) -> List[str]:
        """Apply rule-based grapheme-to-phoneme conversion."""
        phonemes = []
        i = 0
        
        while i < len(word):
            # Try digraphs first (2-letter combinations)
            if i < len(word) - 1:
                digraph = word[i:i+2]
                if digraph in self.digraph_rules:
                    phonemes.extend(self.digraph_rules[digraph])
                    i += 2
                    continue
            
            # Single letter rules
            letter = word[i]
            
            # Apply contextual vowel rules
            if letter in 'AEIOU':
                phoneme = self._apply_vowel_rules(word, i)
                phonemes.append(phoneme)
            # Apply consonant rules
            elif letter in self.consonant_rules:
                phonemes.extend(self.consonant_rules[letter])
            else:
                # Fallback for unknown letters
                phonemes.append(letter)
            
            i += 1
        
        return phonemes
    
    def _apply_vowel_rules(self, word: str, pos: int) -> str:
        """Apply contextual vowel rules based on position and surrounding letters."""
        vowel = word[pos]
        
        # Get context
        prev_char = word[pos-1] if pos > 0 else ''
        next_char = word[pos+1] if pos < len(word)-1 else ''
        next2_char = word[pos+2] if pos < len(word)-2 else ''
        
        # Silent E rule
        if pos == len(word)-1 and vowel == 'E':
            if len(word) > 1 and word[pos-1] not in 'AEIOU':
                return 'SIL'  # Silent E
        
        # Magic E rule (CVCe pattern)
        if pos < len(word)-2 and next2_char == 'E' and next_char not in 'AEIOU':
            if vowel == 'A':
                return 'EY'
            elif vowel == 'I':
                return 'AY'
            elif vowel == 'O':
                return 'OW'
            elif vowel == 'U':
                return 'UW'
        
        # Default vowel mappings
        return self.vowel_rules.get(vowel, vowel)
    
    def _load_vowel_rules(self) -> Dict[str, str]:
        """Load basic vowel to phoneme mappings."""
        return {
            'A': 'AE',    # cat
            'E': 'EH',    # bed
            'I': 'IH',    # bit
            'O': 'AO',    # cot
            'U': 'AH',    # but
            'Y': 'IH'     # gym
        }
    
    def _load_consonant_rules(self) -> Dict[str, List[str]]:
        """Load consonant to phoneme mappings."""
        return {
            'B': ['B'],
            'C': ['K'],    # Default, context-dependent rules would be more complex
            'D': ['D'],
            'F': ['F'],
            'G': ['G'],    # Default, context-dependent rules would be more complex
            'H': ['HH'],
            'J': ['JH'],
            'K': ['K'],
            'L': ['L'],
            'M': ['M'],
            'N': ['N'],
            'P': ['P'],
            'Q': ['K', 'W'],  # QU sound
            'R': ['R'],
            'S': ['S'],
            'T': ['T'],
            'V': ['V'],
            'W': ['W'],
            'X': ['K', 'S'],  # ks sound
            'Z': ['Z']
        }
    
    def _load_digraph_rules(self) -> Dict[str, List[str]]:
        """Load two-letter combination rules."""
        return {
            # Consonant digraphs
            'CH': ['CH'],
            'SH': ['SH'],
            'TH': ['TH'],
            'WH': ['W'],
            'PH': ['F'],
            'GH': ['F'],   # laugh, rough
            'CK': ['K'],
            'NG': ['NG'],
            
            # Vowel combinations
            'AI': ['EY'],  # rain
            'AY': ['EY'],  # day
            'EA': ['IY'],  # eat
            'EE': ['IY'],  # see
            'EI': ['EY'],  # eight
            'EY': ['EY'],  # they
            'IE': ['IY'],  # piece
            'OA': ['OW'],  # boat
            'OO': ['UW'],  # moon
            'OU': ['AW'],  # out
            'OW': ['AW'],  # cow
            'OY': ['OY'],  # boy
            'UI': ['UW'],  # suit
            'UE': ['UW'],  # blue
            'AU': ['AO'],  # caught
            'AW': ['AO'],  # saw
            'EW': ['UW'],  # new
            'OI': ['OY'],  # oil
            
            # Common letter combinations
            'QU': ['K', 'W'],
            'SC': ['S'],   # science
            'KN': ['N'],   # knife
            'WR': ['R'],   # write
            'MB': ['M'],   # lamb (silent b)
            'BT': ['T'],   # debt (silent b)
        }
    
    def _load_exception_words(self) -> Dict[str, List[str]]:
        """Load words with irregular pronunciations."""
        return {
            # Common irregular words
            'THE': ['DH', 'AH'],
            'A': ['AH'],
            'AN': ['AE', 'N'],
            'AND': ['AE', 'N', 'D'],
            'OF': ['AH', 'V'],
            'TO': ['T', 'UW'],
            'IN': ['IH', 'N'],
            'IS': ['IH', 'Z'],
            'IT': ['IH', 'T'],
            'FOR': ['F', 'AO', 'R'],
            'AS': ['AE', 'Z'],
            'WITH': ['W', 'IH', 'TH'],
            'HIS': ['HH', 'IH', 'Z'],
            'HER': ['HH', 'ER'],
            'HIM': ['HH', 'IH', 'M'],
            'HAS': ['HH', 'AE', 'Z'],
            'HAD': ['HH', 'AE', 'D'],
            'HAVE': ['HH', 'AE', 'V'],
            'BE': ['B', 'IY'],
            'BEEN': ['B', 'IH', 'N'],
            'WAS': ['W', 'AH', 'Z'],
            'WERE': ['W', 'ER'],
            'ARE': ['AA', 'R'],
            'WHAT': ['W', 'AH', 'T'],
            'WHEN': ['W', 'EH', 'N'],
            'WHERE': ['W', 'EH', 'R'],
            'WHO': ['HH', 'UW'],
            'WHY': ['W', 'AY'],
            'HOW': ['HH', 'AW'],
            'WOULD': ['W', 'UH', 'D'],
            'COULD': ['K', 'UH', 'D'],
            'SHOULD': ['SH', 'UH', 'D'],
            'ONE': ['W', 'AH', 'N'],
            'TWO': ['T', 'UW'],
            'THREE': ['TH', 'R', 'IY'],
            'FOUR': ['F', 'AO', 'R'],
            'FIVE': ['F', 'AY', 'V'],
            'SIX': ['S', 'IH', 'K', 'S'],
            'SEVEN': ['S', 'EH', 'V', 'AH', 'N'],
            'EIGHT': ['EY', 'T'],
            'NINE': ['N', 'AY', 'N'],
            'TEN': ['T', 'EH', 'N'],
            'ELEVEN': ['IH', 'L', 'EH', 'V', 'AH', 'N'],
            'TWELVE': ['T', 'W', 'EH', 'L', 'V'],
            
            # Technology terms
            'COMPUTER': ['K', 'AH', 'M', 'P', 'Y', 'UW', 'T', 'ER'],
            'PROGRAM': ['P', 'R', 'OW', 'G', 'R', 'AE', 'M'],
            'SYSTEM': ['S', 'IH', 'S', 'T', 'AH', 'M'],
            'MACHINE': ['M', 'AH', 'SH', 'IY', 'N'],
            'DEVICE': ['D', 'IH', 'V', 'AY', 'S'],
            'NETWORK': ['N', 'EH', 'T', 'W', 'ER', 'K'],
            'SOFTWARE': ['S', 'AO', 'F', 'T', 'W', 'EH', 'R'],
            'HARDWARE': ['HH', 'AA', 'R', 'D', 'W', 'EH', 'R'],
            'MEMORY': ['M', 'EH', 'M', 'ER', 'IY'],
            'PROCESSOR': ['P', 'R', 'AA', 'S', 'EH', 'S', 'ER'],
            'TECHNOLOGY': ['T', 'EH', 'K', 'N', 'AA', 'L', 'AH', 'JH', 'IY'],
            'ELECTRONIC': ['IH', 'L', 'EH', 'K', 'T', 'R', 'AA', 'N', 'IH', 'K'],
            'DIGITAL': ['D', 'IH', 'JH', 'IH', 'T', 'AH', 'L'],
            'INTERFACE': ['IH', 'N', 'T', 'ER', 'F', 'EY', 'S'],
            'INFORMATION': ['IH', 'N', 'F', 'ER', 'M', 'EY', 'SH', 'AH', 'N'],
            
            # Numbers as words
            'ZERO': ['Z', 'IH', 'R', 'OW'],
            'HUNDRED': ['HH', 'AH', 'N', 'D', 'R', 'AH', 'D'],
            'THOUSAND': ['TH', 'AW', 'Z', 'AH', 'N', 'D'],
            'MILLION': ['M', 'IH', 'L', 'Y', 'AH', 'N'],
            'BILLION': ['B', 'IH', 'L', 'Y', 'AH', 'N'],
            
            # Common words with silent letters
            'KNIFE': ['N', 'AY', 'F'],
            'KNOW': ['N', 'OW'],
            'KNEE': ['N', 'IY'],
            'WRITE': ['R', 'AY', 'T'],
            'WRONG': ['R', 'AO', 'NG'],
            'LAMB': ['L', 'AE', 'M'],
            'THUMB': ['TH', 'AH', 'M'],
            'DEBT': ['D', 'EH', 'T'],
            'DOUBT': ['D', 'AW', 'T'],
            'ISLAND': ['AY', 'L', 'AH', 'N', 'D'],
            'LISTEN': ['L', 'IH', 'S', 'AH', 'N'],
            'CASTLE': ['K', 'AE', 'S', 'AH', 'L'],
            'CHRISTMAS': ['K', 'R', 'IH', 'S', 'M', 'AH', 'S'],
            'WEDNESDAY': ['W', 'EH', 'N', 'Z', 'D', 'EY'],
            'FEBRUARY': ['F', 'EH', 'B', 'R', 'UW', 'EH', 'R', 'IY']
        }
    
    def _load_syllable_patterns(self) -> Dict[str, str]:
        """Load syllable stress patterns (simplified for 1986 implementation)."""
        return {
            # Common syllable patterns
            'CV': 'unstressed',    # consonant-vowel
            'CVC': 'stressed',     # consonant-vowel-consonant
            'CVCV': 'stressed_unstressed',
            'VCVC': 'unstressed_stressed'
        }
