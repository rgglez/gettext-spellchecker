"""
   Copyright 2026 Rodolfo González González.

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

import os
import polib
import hunspell
import string

# ASCII punctuation plus common typographic marks used in es/de/fr.
PUNCTUATION = string.punctuation + "¿¡«»„“”‘’‚…–—"

# -----------------------------------------------------------------------------


class SpellChecker:
    def __init__(self, path, lang, po, check):
        """
        Constructor.

        Raises FileNotFoundError if the hunspell dictionary for lang does not
        exist in path.
        """

        # Path to the po file.
        self.po = po

        # "msgid" or "msgstr".
        self.check = check

        # Form the paths for the dic and aff files for hunspell. The language
        # is used as is, since dictionary names vary (de_DE, de_DE_frami,
        # ca_ES-valencia, ...).
        dic_file = os.path.join(path, lang + ".dic")
        aff_file = os.path.join(path, lang + ".aff")
        for f in (dic_file, aff_file):
            if not os.path.isfile(f):
                available = sorted(
                    n[:-4] for n in os.listdir(path) if n.endswith(".dic")
                ) if os.path.isdir(path) else []
                raise FileNotFoundError(
                    f"hunspell dictionary file not found: {f}. "
                    f"Available in {path}: {', '.join(available) or 'none'}"
                )

        # Create the spell checker.
        self.spell_checker = hunspell.HunSpell(dic_file, aff_file)
    # __init__

    # -------------------------------------------------------------------------

    @staticmethod
    def strip_punctuation(word):
        """
        Strips leading and trailing punctuation marks from a word, keeping
        inner ones such as apostrophes and hyphens (don't, e-mail).
        """
        return word.strip(PUNCTUATION)
    # strip_punctuation

    # -------------------------------------------------------------------------

    def strings(self, entry):
        """
        Returns the strings of an entry to be checked, including plural forms.
        """
        if self.check == "msgstr":
            if entry.msgstr_plural:
                return list(entry.msgstr_plural.values())
            return [entry.msgstr]
        return [entry.msgid, entry.msgid_plural]
    # strings

    # -------------------------------------------------------------------------

    def Check(self):
        """
        Checks the spell of each word of each string.
        """

        # Load the po file.
        po_file = polib.pofile(self.po)

        # Load the strings to be checked, either the "msgid" or the "msgstr".
        # Obsolete (#~) entries are skipped.
        strings = [
            s
            for entry in po_file if not entry.obsolete
            for s in self.strings(entry) if s
        ]

        # Be patient!!!!

        # Result. Phrases (strings) will be the key, and the value will be an
        # array of mispelled words.
        result = {}

        # Check every string.
        for text in strings:
            wrong_words = []  # each mispelled word will be kept here

            # Check every word.
            for word in text.split():
                # ponytail: skips anything with digits or format chars
                # (%(count)d, {0}); a real placeholder regex if this misses some.
                if any(c.isdigit() or c in "%{}" for c in word):
                    continue
                word = SpellChecker.strip_punctuation(word)
                if not word:
                    continue
                if not self.spell_checker.spell(word):
                    wrong_words.append(word)

            if wrong_words:
                result[text] = wrong_words

        return result
    # Check
# SpellChecker
