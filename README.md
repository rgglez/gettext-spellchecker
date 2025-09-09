# gettext-spellchecker

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub all releases](https://img.shields.io/github/downloads/rgglez/gettext-spellchecker/total)
![GitHub issues](https://img.shields.io/github/issues/rgglez/gettext-spellchecker)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/rgglez/gettext-spellchecker)
![GitHub stars](https://img.shields.io/github/stars/rgglez/gettext-spellchecker?style=social)
![GitHub forks](https://img.shields.io/github/forks/rgglez/gettext-spellchecker?style=social)

**gettext-spellchecker** is a Python script which checks the spell of `msgid` or `msgstr` strings in a [gettext](https://www.gnu.org/software/gettext/) .po or .pot file. 

It uses [hunspell](https://github.com/hunspell/hunspell) dictionaries.

It outputs the results to a CSV file or to colored output in the terminal.

## Execution

```bash
python3 check.py --path /usr/share/hunspell --lang=de_DE -i ../examples/example_simple.po --check=msgstr
```

## Command line options

* `--version` prints the script version.
* `--path` the path to hunspell dictionaries. Default: "/usr/share/hunspell".
* `--lang` the code of the language the strings in the form xx_YY where xx is in [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) format and YY in [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements) format.
* `-i`, `--input` the path of the .po or .pot file.
* `-o`, `--output` optional path of the output file in CSV format.
* `--check` which string do you want the script to check: 'msgid' or 'msgstr'. Default="msgid".

## Dependencies

### hunspell

This script uses [hunspell](https://github.com/hunspell/hunspell) dictionaries.

In Debian and derivatives you install them with `apt`, for instance:

```bash
apt install hunspell-fr
```

Read your operating system's documentation to know how to install those packages from its repositories, or visit [hunspell](https://github.com/hunspell/hunspell) if you need to compile them by hand.

### Python modules

This script depends on the following Python modules:

* argparse
* spellchecker
* colorama
* csv
* polib
* hunspell
* pycountry
* string

You can install them using your operating system package manager or `pip` in a venv.

## Notes

* Sample .po and .pot files are included in the `examples` directory.
* Why gettext?
  * First and most relevant reason: it uses the full strings in the original language as key, so I don't have to be searching for weird keys such as "page.title.hello" or "item.specification". If one translation doesn't exist, the original key string is used.
  * It's a GNU standard, tried and trusted.

## License

Copyright 2025 Rodolfo González González.

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Please read the [LICENSE](LICENSE) file.
