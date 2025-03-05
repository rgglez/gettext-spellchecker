"""
   Copyright 2025 Rodolfo González González.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import polib
import hunspell
import pycountry
import string

###############################################################################

class SpellChecker:
    def __init__(self, path, lang, po, check):
        """
        Constructor.
        """

        # Path to the po file.
        self.po = po

        # "msgid" or "msgstr".
        self.check = check

        # Form the paths for the dic and aff files for hunspell.
        path = SpellChecker.strip_last_slash(path)
        code = SpellChecker.normalize_language_code(lang)        
        dic_file = path + "/" + code + ".dic"
        aff_file = path + "/" + code + ".aff"

        # Create the spell checker.
        self.spell_checker = hunspell.HunSpell(dic_file, aff_file)
    # __init__

    #--------------------------------------------------------------------------

    @staticmethod
    def strip_last_slash(s):
        """
        Strips trailing slashes from the path.
        """
        return s.rstrip('/')
    # strip_last_slash

    #--------------------------------------------------------------------------

    @staticmethod
    def normalize_language_code(code):
        """
        Validates and normalizes a language code in the form xx_YY.
        
        Args:
            code (str): The language code to validate and normalize.
            
        Returns:
            str: The normalized language code (xx_YY) if valid, otherwise None.
        """
        try:
            # Split the code into language and country parts
            lang_part, country_part = code.split('_')
            
            # Validate ISO 639-1 language code
            lang = pycountry.languages.get(alpha_2=lang_part.lower())
            if not lang:
                return None
            
            # Validate ISO 3166-1 alpha-2 country code
            country = pycountry.countries.get(alpha_2=country_part.upper())
            if not country:
                return None
            
            # Return the normalized code
            return f"{lang_part.lower()}_{country_part.upper()}"
        
        except (ValueError, AttributeError):
            # Handle invalid format or missing parts
            return None
    # normalize_language_code

    #--------------------------------------------------------------------------

    @staticmethod
    def strip_punctuation(text):
        """
        Strips punctuation marks from a string.
        """
        return text.translate(str.maketrans('', '', string.punctuation))
    # strip_punctuation

    #--------------------------------------------------------------------------

    def Check(self):
        """
        Checks the spell of each word of each string. 
        """

        # Load the po file.
        po_file = polib.pofile(self.po)

        # Load the strings to be checked, either the "msgid" or the "msgstr".
        strings = [
            entry.msgstr if self.check == "msgstr" else entry.msgid
            for entry in po_file
        ]

        # Be patient!!!!

        # Result. Phrases (strings) will be the key, and the value will be an 
        # array of mispelled words.
        result = {} 

        # Check every string.
        for string in strings:
            wrong_words = [] # each mispelled word will be kept here

            # Check every word.
            words = string.split()            
            for word in words:
                word = SpellChecker.strip_punctuation(word)
                if not self.spell_checker.spell(word):                    
                    wrong_words.append(word)

            if wrong_words:
                result[string] = wrong_words
                                    
        return result
    # check_strings
# SpellChecker