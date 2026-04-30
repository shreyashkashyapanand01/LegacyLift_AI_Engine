from parsing.metrics.comparator.metrics_comparator import MetricsComparator

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

print(MetricsComparator.compare(before, after))