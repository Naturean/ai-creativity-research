# Divergent Association Task code

Modified version of [Divergent Association Task](https://github.com/jayolson/divergent-association-task).

## How to run

1. Run `pip3 install --user numpy scipy` to install dependencies.
2. Run `python get_words.py` first to extract the DAT word dictionary from the raw questionnaire CSV. The script auto-detects the first CSV in `data/raw/questionnaire/` and writes `words.txt`.
3. Use `scoring.py` to compute scores for new responses. Example usage:

   ```python
   from dat.scoring import get_dat_score

   dat_score = get_dat_score(["apple", "banana", "car", "dog"])
   ```
