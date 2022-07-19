"""Simple regular expressions to fix tokenization issues for CoNLL.

Usage:
$ python3 retokenize.py [model_predictions_file] > [retokenized_predictions_file]
"""
import fileinput
import re

retokenization_rules = [
    # Remove extra space around single quotes, hyphens, and slashes.
    (" ' (.*?) ' ", " '\\1' "),
    (" - ", "-"),
    (" / ", "/"),
    # Ensure there are spaces around parentheses and brackets.
    (r"([\]\[\(\){}<>])", " \\1 "),
    (r"\s+", " "),
]

for line in fileinput.input():
  for rule in retokenization_rules:
    line = re.sub(rule[0], rule[1], line)
  print(line.strip())
