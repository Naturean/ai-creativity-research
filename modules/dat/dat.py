"""Compute score for Divergent Association Task,
a quick and simple measure of creativity
(Copyright 2021 Jay Olson; see LICENSE)"""

import itertools
import os
import re

import gensim
import scipy.spatial.distance

DEFAULT_MODEL = r'D:\DevProjects\repo\Creativity-BasedOn-Semantic-Toolbox\cc.zh.300.bin'
DEFAULT_DICTIONARY = os.path.join(os.path.dirname(__file__), "words.txt")

class Model:
    """Create model to compute DAT"""

    def __init__(self, model=DEFAULT_MODEL, dictionary=DEFAULT_DICTIONARY, pattern="^[a-zA-Z\u4e00-\u9fff](?:[a-zA-Z\u4e00-\u9fff-]*[a-zA-Z\u4e00-\u9fff])?$"):
        """Load word vectors and optionally restrict them with a dictionary."""

        self.dictionary = None
        if dictionary is not None:
            self.dictionary = set()
            with open(dictionary, "r", encoding="utf8") as f:
                for line in f:
                    word = line.strip()
                    if re.match(pattern, word):
                        self.dictionary.add(word)

        print(f'Loading model from {model}...')
        if model.endswith(".bin"):
            self.model = gensim.models.fasttext.load_facebook_vectors(os.path.join(model))
        else:
            self.model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join(model), binary=False)


    def validate(self, word):
        """Clean up word and find best candidate to use"""

        # Strip unwanted characters
        clean = re.sub(r"[^a-zA-Z\u4e00-\u9fff- ]+", "", word).strip().lower()
        if len(clean) <= 0:
            return None

        if clean in self.model.key_to_index and (self.dictionary is None or clean in self.dictionary):
            return clean # Return the cleaned word if it is in model
        print(f'Word not found: {word}')
        return None # Could not find valid word


    def distance(self, word1, word2):
        """Compute cosine distance (0 to 2) between two words"""
        return scipy.spatial.distance.cosine(self.model.get_vector(word1), self.model.get_vector(word2))


    def dat(self, words, minimum=7):
        """Compute DAT score"""
        # Keep only valid unique words
        uniques = []
        for word in words:
            valid = self.validate(word)
            if valid and valid not in uniques:
                uniques.append(valid)

        # Keep subset of words
        if len(uniques) >= minimum:
            subset = uniques[:minimum]
        else:
            print(f'Not enough valid words (found {len(uniques)}, need {minimum}): {words}')
            return None # Not enough valid words

        # Compute distances between each pair of words
        distances = []
        for word1, word2 in itertools.combinations(subset, 2):
            dist = self.distance(word1, word2)
            distances.append(dist)

        # Compute the DAT score (average semantic distance multiplied by 100)
        return (sum(distances) / len(distances)) * 100
