from parsing.metrics.extractors.maintainability import MaintainabilityAnalyzer

# sample inputs from your previous steps
volume = 62.91
complexity = 2
loc = 2

print(MaintainabilityAnalyzer.analyze(volume, complexity, loc))