#!/usr/bin/env python
"""Download required NLTK data for TextBlob sentiment analysis"""

import nltk
import ssl

# Handle SSL certificate verification issues on Windows
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
print("Downloading NLTK data...")
nltk.download('punkt_tab')
nltk.download('brown')
nltk.download('punkt')

print("NLTK data download complete!")
