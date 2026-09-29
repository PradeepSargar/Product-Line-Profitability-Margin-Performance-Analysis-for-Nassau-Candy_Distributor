"""
Root entrypoint delegating directly to the modular dashboard application.

Usage:
    streamlit run app.py
    streamlit run dashboard/app.py
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dashboard.app import main

if __name__ == "__main__":
    main()
