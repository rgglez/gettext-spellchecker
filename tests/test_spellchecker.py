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

# Tests for the spell checker, using the example .po file.
# Needs the de_DE and en_US hunspell dictionaries in /usr/share/hunspell.

import os

import pytest

from gettext_spellchecker import SpellChecker

DICTS = "/usr/share/hunspell"
PO = os.path.join(os.path.dirname(__file__), "..", "examples", "example_simple.po")

pytestmark = pytest.mark.skipif(
    not all(os.path.isfile(f"{DICTS}/{lang}.dic") for lang in ("de_DE", "en_US")),
    reason="de_DE or en_US hunspell dictionaries not found",
)

# -----------------------------------------------------------------------------


def test_msgstr():
    # Only the misspelled words are found: placeholders, typographic
    # punctuation and obsolete entries are fine, plural forms are checked.
    result = SpellChecker(DICTS, "de_DE", PO, "msgstr").Check()
    assert result == {
        "Ich verstehe nict": ["nict"],
        "%d Dateien wurden gelöshct": ["gelöshct"],
    }


def test_msgid():
    # Inner apostrophes (don't) are fine, msgid_plural is checked.
    result = SpellChecker(DICTS, "en_US", PO, "msgid").Check()
    assert result == {
        "Good mornin": ["mornin"],
        "%d files were deletd": ["deletd"],
    }


def test_missing_dictionary():
    # Missing dictionary raises a clear error listing the available ones.
    with pytest.raises(FileNotFoundError, match="de_DE"):
        SpellChecker(DICTS, "xx_YY", PO, "msgid")
