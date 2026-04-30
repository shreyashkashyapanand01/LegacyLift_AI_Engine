from parsing.metrics.scorer.quality_scorer import QualityScorer

before = {
    "complexity": 3,
    "loc": 5,
    "maintainability": 70,
    "halstead": {"effort": 500}
}

after = {
    "complexity": 1,
    "loc": 3,
    "maintainability": 90,
    "halstead": {"effort": 300}
}

print(QualityScorer.compare(before, after))