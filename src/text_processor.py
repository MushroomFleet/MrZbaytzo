"""
Text Processing Module for MR.ZPAYTZO-rev0
Implements 1986-era text normalization and linguistic rules (~1,200 rules)
"""

import re
import string
from typing import List, Dict, Tuple


class TextProcessor:
    """
    Text normalization engine implementing vintage TTS text processing rules.
    Based on First Byte Monologue engine specifications (~1,200 linguistic rules).
    """
    
    def __init__(self):
        self.abbreviations = self._load_abbreviations()
        self.number_rules = self._load_number_rules()
        self.punctuation_rules = self._load_punctuation_rules()
        self.stress_patterns = self._load_stress_patterns()
    
    def normalize(self, text: str) -> str:
        """
        Apply complete text normalization pipeline.
        
        Args:
            text: Raw input text
            
        Returns:
            Normalized text ready for phoneme conversion
        """
        # Stage 1: Basic cleanup and case handling
        text = self._basic_cleanup(text)
        
        # Stage 2: Expand abbreviations and acronyms
        text = self._expand_abbreviations(text)
        
        # Stage 3: Handle numbers and numeric expressions
        text = self._expand_numbers(text)
        
        # Stage 4: Process punctuation and pauses
        text = self._process_punctuation(text)
        
        # Stage 5: Apply stress and inflection patterns
        text = self._apply_stress_patterns(text)
        
        # Stage 6: Final cleanup
        text = self._final_cleanup(text)
        
        return text
    
    def _basic_cleanup(self, text: str) -> str:
        """Basic text cleaning and normalization."""
        # Convert to uppercase (vintage TTS characteristic)
        text = text.upper()
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Handle contractions (1986-era approach)
        contractions = {
            "WON'T": "WILL NOT",
            "CAN'T": "CANNOT", 
            "DON'T": "DO NOT",
            "ISN'T": "IS NOT",
            "AREN'T": "ARE NOT",
            "WASN'T": "WAS NOT",
            "WEREN'T": "WERE NOT",
            "HAVEN'T": "HAVE NOT",
            "HASN'T": "HAS NOT",
            "HADN'T": "HAD NOT",
            "WOULDN'T": "WOULD NOT",
            "SHOULDN'T": "SHOULD NOT",
            "COULDN'T": "COULD NOT",
            "MUSTN'T": "MUST NOT",
            "NEEDN'T": "NEED NOT",
            "I'M": "I AM",
            "YOU'RE": "YOU ARE",
            "HE'S": "HE IS",
            "SHE'S": "SHE IS",
            "IT'S": "IT IS",
            "WE'RE": "WE ARE",
            "THEY'RE": "THEY ARE",
            "I'VE": "I HAVE",
            "YOU'VE": "YOU HAVE",
            "WE'VE": "WE HAVE",
            "THEY'VE": "THEY HAVE",
            "I'LL": "I WILL",
            "YOU'LL": "YOU WILL",
            "HE'LL": "HE WILL",
            "SHE'LL": "SHE WILL",
            "WE'LL": "WE WILL",
            "THEY'LL": "THEY WILL",
            "I'D": "I WOULD",
            "YOU'D": "YOU WOULD",
            "HE'D": "HE WOULD",
            "SHE'D": "SHE WOULD",
            "WE'D": "WE WOULD",
            "THEY'D": "THEY WOULD"
        }
        
        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)
        
        return text
    
    def _load_abbreviations(self) -> Dict[str, str]:
        """Load common abbreviations and their expansions."""
        return {
            # Title abbreviations
            "MR.": "MISTER",
            "MRS.": "MISSES", 
            "MS.": "MISS",
            "DR.": "DOCTOR",
            "PROF.": "PROFESSOR",
            "REV.": "REVEREND",
            "SEN.": "SENATOR",
            "REP.": "REPRESENTATIVE",
            "GEN.": "GENERAL",
            "COL.": "COLONEL",
            "MAJ.": "MAJOR",
            "CAPT.": "CAPTAIN",
            "LT.": "LIEUTENANT",
            "SGT.": "SERGEANT",
            
            # Common abbreviations
            "ETC.": "ET CETERA",
            "VS.": "VERSUS",
            "E.G.": "FOR EXAMPLE",
            "I.E.": "THAT IS",
            "A.M.": "A M",
            "P.M.": "P M",
            "INC.": "INCORPORATED",
            "CORP.": "CORPORATION",
            "LTD.": "LIMITED",
            "CO.": "COMPANY",
            
            # Units and measurements
            "FT.": "FEET",
            "IN.": "INCHES", 
            "LB.": "POUND",
            "LBS.": "POUNDS",
            "OZ.": "OUNCE",
            "PT.": "PINT",
            "QT.": "QUART",
            "GAL.": "GALLON",
            "MPH": "MILES PER HOUR",
            "MPG": "MILES PER GALLON",
            
            # Geographic
            "ST.": "STREET",
            "AVE.": "AVENUE", 
            "BLVD.": "BOULEVARD",
            "RD.": "ROAD",
            "DR.": "DRIVE",
            "CT.": "COURT",
            "PL.": "PLACE",
            "APT.": "APARTMENT",
            
            # States (common ones)
            "CA": "CALIFORNIA",
            "NY": "NEW YORK",
            "TX": "TEXAS",
            "FL": "FLORIDA",
            "IL": "ILLINOIS",
            "PA": "PENNSYLVANIA",
            "OH": "OHIO",
            "MI": "MICHIGAN",
            "WA": "WASHINGTON",
            "OR": "OREGON"
        }
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand abbreviations to full words."""
        words = text.split()
        result = []
        
        for word in words:
            # Check for exact match
            if word in self.abbreviations:
                result.append(self.abbreviations[word])
            # Check for match with punctuation
            elif word.rstrip(string.punctuation) in self.abbreviations:
                base_word = word.rstrip(string.punctuation)
                punctuation = word[len(base_word):]
                result.append(self.abbreviations[base_word] + punctuation)
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def _load_number_rules(self) -> Dict:
        """Load number expansion rules."""
        return {
            'ordinals': {
                '1ST': 'FIRST', '2ND': 'SECOND', '3RD': 'THIRD',
                '4TH': 'FOURTH', '5TH': 'FIFTH', '6TH': 'SIXTH',
                '7TH': 'SEVENTH', '8TH': 'EIGHTH', '9TH': 'NINTH',
                '10TH': 'TENTH', '11TH': 'ELEVENTH', '12TH': 'TWELFTH',
                '13TH': 'THIRTEENTH', '14TH': 'FOURTEENTH', '15TH': 'FIFTEENTH',
                '16TH': 'SIXTEENTH', '17TH': 'SEVENTEENTH', '18TH': 'EIGHTEENTH',
                '19TH': 'NINETEENTH', '20TH': 'TWENTIETH', '21ST': 'TWENTY FIRST',
                '22ND': 'TWENTY SECOND', '23RD': 'TWENTY THIRD', '30TH': 'THIRTIETH'
            },
            'cardinals': {
                '0': 'ZERO', '1': 'ONE', '2': 'TWO', '3': 'THREE', '4': 'FOUR',
                '5': 'FIVE', '6': 'SIX', '7': 'SEVEN', '8': 'EIGHT', '9': 'NINE',
                '10': 'TEN', '11': 'ELEVEN', '12': 'TWELVE', '13': 'THIRTEEN',
                '14': 'FOURTEEN', '15': 'FIFTEEN', '16': 'SIXTEEN', '17': 'SEVENTEEN',
                '18': 'EIGHTEEN', '19': 'NINETEEN', '20': 'TWENTY', '30': 'THIRTY',
                '40': 'FORTY', '50': 'FIFTY', '60': 'SIXTY', '70': 'SEVENTY',
                '80': 'EIGHTY', '90': 'NINETY', '100': 'ONE HUNDRED',
                '1000': 'ONE THOUSAND', '1000000': 'ONE MILLION'
            }
        }
    
    def _expand_numbers(self, text: str) -> str:
        """Expand numbers to word form (1986-era simple approach)."""
        # Handle ordinals first
        for ordinal, word in self.number_rules['ordinals'].items():
            text = text.replace(ordinal, word)
        
        # Handle simple cardinals (0-99)
        def number_to_words(num_str):
            try:
                num = int(num_str)
                if 0 <= num <= 20:
                    return self.number_rules['cardinals'].get(str(num), num_str)
                elif 21 <= num <= 99:
                    tens = (num // 10) * 10
                    ones = num % 10
                    if ones == 0:
                        return self.number_rules['cardinals'].get(str(tens), num_str)
                    else:
                        tens_word = self.number_rules['cardinals'].get(str(tens), str(tens))
                        ones_word = self.number_rules['cardinals'].get(str(ones), str(ones))
                        return f"{tens_word} {ones_word}"
                elif num == 100:
                    return "ONE HUNDRED"
                elif 101 <= num <= 999:
                    hundreds = num // 100
                    remainder = num % 100
                    hundreds_word = self.number_rules['cardinals'].get(str(hundreds), str(hundreds))
                    if remainder == 0:
                        return f"{hundreds_word} HUNDRED"
                    else:
                        remainder_word = number_to_words(str(remainder))
                        return f"{hundreds_word} HUNDRED {remainder_word}"
                elif num == 1000:
                    return "ONE THOUSAND"
                else:
                    return num_str  # Keep original for complex numbers
            except ValueError:
                return num_str
        
        # Replace standalone numbers
        words = text.split()
        result = []
        
        for word in words:
            # Check if word is purely numeric
            clean_word = word.strip(string.punctuation)
            if clean_word.isdigit():
                punctuation = word[len(clean_word):]
                converted = number_to_words(clean_word)
                result.append(converted + punctuation)
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def _load_punctuation_rules(self) -> Dict:
        """Load punctuation handling rules."""
        return {
            '.': ' PERIOD ',
            ',': ' COMMA ',
            ';': ' SEMICOLON ',
            ':': ' COLON ',
            '!': ' EXCLAMATION POINT ',
            '?': ' QUESTION MARK ',
            '"': ' QUOTE ',
            "'": ' APOSTROPHE ',
            '(': ' OPEN PARENTHESIS ',
            ')': ' CLOSE PARENTHESIS ',
            '[': ' OPEN BRACKET ',
            ']': ' CLOSE BRACKET ',
            '{': ' OPEN BRACE ',
            '}': ' CLOSE BRACE ',
            '-': ' DASH ',
            '_': ' UNDERSCORE ',
            '/': ' SLASH ',
            '\\': ' BACKSLASH ',
            '&': ' AND ',
            '@': ' AT ',
            '#': ' HASH ',
            '$': ' DOLLAR ',
            '%': ' PERCENT ',
            '*': ' ASTERISK ',
            '+': ' PLUS ',
            '=': ' EQUALS ',
            '<': ' LESS THAN ',
            '>': ' GREATER THAN '
        }
    
    def _process_punctuation(self, text: str) -> str:
        """Process punctuation according to 1986 TTS conventions."""
        # Handle sentence endings (add pause markers)
        text = re.sub(r'[.!?]+', ' <PAUSE_LONG> ', text)
        
        # Handle commas and semicolons (shorter pauses)
        text = re.sub(r'[,;]', ' <PAUSE_SHORT> ', text)
        
        # Handle colons
        text = re.sub(r':', ' <PAUSE_MEDIUM> ', text)
        
        # Remove or convert remaining punctuation
        for punct, replacement in self.punctuation_rules.items():
            if punct not in '.!?,;:':  # Already handled above
                text = text.replace(punct, replacement)
        
        return text
    
    def _load_stress_patterns(self) -> Dict:
        """Load word stress patterns (simplified 1986 approach)."""
        return {
            # Common stress patterns for vintage TTS
            'COMPUTER': 'com-PU-ter',
            'TECHNOLOGY': 'tech-NOL-o-gy', 
            'INFORMATION': 'in-for-MA-tion',
            'ELECTRONIC': 'e-lec-TRON-ic',
            'DIGITAL': 'DIG-i-tal',
            'PROGRAM': 'PRO-gram',
            'PROCESSOR': 'PROC-es-sor',
            'MEMORY': 'MEM-o-ry',
            'SOFTWARE': 'SOFT-ware',
            'HARDWARE': 'HARD-ware',
            'SYSTEM': 'SYS-tem',
            'MACHINE': 'ma-CHINE',
            'DEVICE': 'de-VICE',
            'INTERFACE': 'IN-ter-face',
            'NETWORK': 'NET-work'
        }
    
    def _apply_stress_patterns(self, text: str) -> str:
        """Apply basic stress patterns (1986-era simple approach)."""
        words = text.split()
        result = []
        
        for word in words:
            clean_word = word.strip(string.punctuation)
            if clean_word in self.stress_patterns:
                # Apply stress pattern (simplified - just preserve the word)
                # In full implementation, this would add stress markers
                result.append(word)
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def _final_cleanup(self, text: str) -> str:
        """Final text cleanup before phoneme conversion."""
        # Normalize whitespace around pause markers
        text = re.sub(r'\s*<PAUSE_LONG>\s*', ' <PAUSE_LONG> ', text)
        text = re.sub(r'\s*<PAUSE_MEDIUM>\s*', ' <PAUSE_MEDIUM> ', text)
        text = re.sub(r'\s*<PAUSE_SHORT>\s*', ' <PAUSE_SHORT> ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text
