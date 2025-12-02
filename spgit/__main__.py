"""
Allow running spgit as a module: python -m spgit
"""

from .cli import main

if __name__ == '__main__':
    import sys
    sys.exit(main())
