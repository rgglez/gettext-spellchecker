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

import argparse
from spellchecker import SpellChecker
from colorama import init, Style, Fore
import csv
from version import __version__

###############################################################################

def main():
    """
    Main function to parse arguments and initiate processing.
    """

    parser = argparse.ArgumentParser(description="Scan and process .po or .pot files")
    parser.add_argument("--version", action="version", version=f'%(prog)s {__version__}')
    parser.add_argument("--path", required=True, default="/usr/share/hunspell", help="The path to hunspell dictionaries.")
    parser.add_argument("--lang", required=True, default="", help="Input language code in the form xx_YY where xx is in ISO 639-1 format and YY in ISO 3166-1 alpha-2 format")
    parser.add_argument("-i", "--input", required=True, help="Input .po or .pot file path and name")
    parser.add_argument("-o", "--output", required=False, help="CSV output file.")
    parser.add_argument("--check", required=False, default="msgid", choices=["msgid", "msgstr"], help="Input which string do you want me to check: 'msgid' or 'msgstr'")

    args = parser.parse_args()

    # Spellcheck...

    sc = SpellChecker(path=args.path, lang=args.lang, po=args.input, check=args.check)
    result = sc.Check()

    # Show results...

    if args.output:
        # Store results in a CSV file.
        with open(args.output, mode="w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
                       
            # Write rows with string and misspelled words.
            for string, words in result.items():
                csv_writer.writerow([string, ", ".join(words)])
    else:
        # Print it colorfully. 
        # Initialize Colorama (required for Windows compatibility)
        init()        
        for string, words in result.items():
            print(f"Possible spelling error in " + Style.BRIGHT + string + Style.RESET_ALL + " > " + Fore.RED + ", ".join(words) + Style.RESET_ALL)
# main    

###############################################################################

if __name__ == "__main__":
    main()
# __main__