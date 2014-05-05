import os
import re

d = os.path.dirname(__file__)
__all__ = []

for f in os.listdir(d):
    if f.endswith(".py") and not f.endswith("_test.py") and not f == os.path.basename(__file__):
        __all__.append(f.replace(".py", ""))


