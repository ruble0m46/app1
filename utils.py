from data import sample_data, sample_choices
import numpy as np
from scipy.stats import pearsonr
from numpy.linalg import norm

def calculate_similarity(user_data):
    out = []
    for i, sample in enumerate(sample_data):
        diffs = [abs(a - b) for a, b in zip(user_data, sample)]
        sq = [(a - b)**2 for a, b in zip(user_data, sample)]
        mean_diff = sum(diffs) / len(sample)
        variance = sum(sq) / len(sample)
        distance = mean_diff * 0.75 + variance * 0.25
        out.append((i, {"choice": sample_choices[i], "distance": distance}))
    return sorted(out, key=lambda x: x[1]["distance"])[:3]

def calculate_pearson(user_data):
    out = []
    for i, sample in enumerate(sample_data):
        corr = pearsonr(user_data, sample)[0]
        out.append((i, {"choice": sample_choices[i], "score": corr}))
    return sorted(out, key=lambda x: -x[1]["score"])[:3]

def calculate_cosine(user_data):
    out = []
    for i, sample in enumerate(sample_data):
        sim = np.dot(user_data, sample) / (norm(user_data) * norm(sample))
        out.append((i, {"choice": sample_choices[i], "score": sim}))
    return sorted(out, key=lambda x: -x[1]["score"])[:3]
