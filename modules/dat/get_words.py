"""
Extract unique DAT responses from raw questionnaire CSV and write to words.txt

Usage:
    python modules/dat/get_words.py [input_csv] [output_txt]

Defaults:
    input_csv: auto-detected from data/raw/questionnaire/
    output_txt: modules/dat/words.txt

This script reads the RAW questionnaire CSV (GBK-encoded), so it can run
BEFORE preprocess. This breaks the circular dependency where preprocess
imports dat (which needs words.txt) but get_words.py used to read from
preprocess output (participants.csv).
"""
import csv
import os
import re
import sys
import glob


def find_dat_fields(fieldnames):
    """Match raw DAT columns by the (N-词语) suffix pattern."""
    return [name for name in fieldnames if re.search(r'\(\d+-词语\)', name)]


def extract_first_chinese_word(value):
    """Extract the first continuous Chinese segment from a string."""
    words = re.findall(r'[一-鿿]+', str(value))
    return words[0] if words else str(value).strip()


def extract_unique_dat_values(csv_path):
    uniques = set()
    with open(csv_path, newline='', encoding='gbk') as fh:
        reader = csv.DictReader(fh)
        dat_fields = find_dat_fields(reader.fieldnames or [])
        if not dat_fields:
            raise RuntimeError(f'No DAT fields (matching (N-词语)) found in header of {csv_path}')
        print(f'Found {len(dat_fields)} DAT fields')
        for row in reader:
            for f in dat_fields:
                v = row.get(f)
                if v is None:
                    continue
                v = v.strip()
                if not v:
                    continue
                v = extract_first_chinese_word(v)
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

    # Default input: first CSV in data/raw/questionnaire/
    questionnaire_dir = os.path.join(repo_root, 'data', 'raw', 'questionnaire')
    default_input = None
    if os.path.isdir(questionnaire_dir):
        csv_files = glob.glob(os.path.join(questionnaire_dir, '*.csv'))
        if csv_files:
            default_input = csv_files[0]

    default_output = os.path.join(repo_root, 'modules', 'dat', 'words.txt')

    input_csv = argv[1] if len(argv) > 1 else default_input
    output_txt = argv[2] if len(argv) > 2 else default_output

    if not input_csv:
        print('No raw questionnaire CSV found. Provide path as argument.', file=sys.stderr)
        return 2
    if not os.path.exists(input_csv):
        print(f'Input CSV not found: {input_csv}', file=sys.stderr)
        return 2

    words = extract_unique_dat_values(input_csv)
    write_words(words, output_txt)
    print(f'Wrote {len(words)} unique words to {output_txt}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
