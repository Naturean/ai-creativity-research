"""
Extract unique DAT responses from participants.csv and write to words.txt

Usage:
    python modules/dat/get_words.py [input_csv] [output_txt]

Defaults:
    input_csv: data/preprocessed/participants.csv
    output_txt: modules/dat/words.txt
"""
import csv
import os
import sys


def find_dat_fields(fieldnames):
    return [name for name in fieldnames if name.lower().startswith('dat_')]


def extract_unique_dat_values(csv_path):
    uniques = set()
    with open(csv_path, newline='', encoding='utf8') as fh:
        reader = csv.DictReader(fh)
        dat_fields = find_dat_fields(reader.fieldnames or [])
        if not dat_fields:
            raise RuntimeError(f'No dat_ fields found in header of {csv_path}')
        for row in reader:
            for f in dat_fields:
                v = row.get(f)
                if v is None:
                    continue
                v = v.strip()
                if not v:
                    continue
                # normalize: lower ASCII, preserve Chinese
                try:
                    v = v.lower()
                except Exception:
                    pass
                uniques.add(v)
    return uniques


def write_words(words, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf8') as fh:
        for w in sorted(words):
            fh.write(w + '\n')


def main(argv):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    default_input = os.path.join(repo_root, 'data', 'preprocessed', 'participants.csv')
    default_output = os.path.join(repo_root, 'modules', 'dat', 'words.txt')

    input_csv = argv[1] if len(argv) > 1 else default_input
    output_txt = argv[2] if len(argv) > 2 else default_output

    if not os.path.exists(input_csv):
        print(f'Input CSV not found: {input_csv}', file=sys.stderr)
        return 2

    words = extract_unique_dat_values(input_csv)
    write_words(words, output_txt)
    print(f'Wrote {len(words)} unique words to {output_txt}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
