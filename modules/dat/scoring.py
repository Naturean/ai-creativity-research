import dat

model = dat.Model()

def get_dat_score(words, minimum=7):
    """Compute DAT score with the shared model instance."""
    return model.dat(words, minimum)
