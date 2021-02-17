#!/usr/bin/env python

import io
import sys
from babel.messages import pofile


def main():

    filename = sys.argv[1]

    with io.open(filename, 'rb') as f:
        cat = pofile.read_po(f)
    charset = cat.charset or 'utf-8'

    with io.open(filename, 'rb') as f:
        my_catalog = pofile.read_po(f, charset=charset)
        fuzzy_entries = len([m for m in my_catalog if m.id and m.fuzzy])
        untranslated_entries = len([m for m in my_catalog if m.id and not m.string])

        if fuzzy_entries or untranslated_entries:
            print(filename)


if __name__ == "__main__":
    main()
