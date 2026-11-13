"""`python -m engine.impute` -- print the B11 hold-out validation report.

Equivalent to `python -m engine.impute.report`; arguments are documented in report.py.
"""
import sys

from .report import main

if __name__ == '__main__':
    sys.exit(main())
