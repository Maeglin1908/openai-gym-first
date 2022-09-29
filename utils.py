TRAINED_DIR_NAME = "trained_model"

def map(x, start1, end1, start2, end2):
    # https://forum.processing.org/one/topic/recreate-map-function.html
    return x + (end2 - start2) * ((x - start1) / (end1 - start1))