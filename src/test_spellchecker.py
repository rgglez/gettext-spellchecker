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

# Self-check. Run with: python3 test_spellchecker.py
# Needs the de_DE and en_US hunspell dictionaries in /usr/share/hunspell.

import os
import sys
from spellchecker import SpellChecker

DICTS = "/usr/share/hunspell"
HERE = os.path.dirname(os.path.abspath(__file__))

# -----------------------------------------------------------------------------


def main():
    if not all(os.path.isfile(f"{DICTS}/{lang}.dic") for lang in ("de_DE", "en_US")):
        print("SKIP: de_DE or en_US hunspell dictionaries not found")
        return

    # Only the misspelled words are found: inner apostrophes (don't),
    # placeholders, typographic punctuation and obsolete entries are fine,
    # plural forms are checked.
    po = os.path.join(HERE, "..", "examples", "example_simple.po")
    result = SpellChecker(DICTS, "de_DE", po, "msgstr").Check()
    assert result == {
        "Ich verstehe nict": ["nict"],
        "%d Dateien wurden gelöshct": ["gelöshct"],
    }, result

    result = SpellChecker(DICTS, "en_US", po, "msgid").Check()
    assert result == {
        "Good mornin": ["mornin"],
        "%d files were deletd": ["deletd"],
    }, result

    # Missing dictionary raises a clear error listing the available ones.
    try:
        SpellChecker(DICTS, "xx_YY", po, "msgid")
        assert False, "expected FileNotFoundError"
    except FileNotFoundError as e:
        assert "de_DE" in str(e), e

    print("OK")
# main

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    sys.exit(main())
# __main__
