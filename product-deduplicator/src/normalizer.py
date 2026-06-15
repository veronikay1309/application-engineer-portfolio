import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TextNormalizer:
    """Standardizes product titles for more accurate fuzzy matching."""

    def __init__(self):
        # Common e-commerce abbreviations to normalize
        self.replacements = {
            r'\boz\b': 'ounces',
            r'\bblk\b': 'black',
            r'\bwht\b': 'white',
            r'\bpkg\b': 'package',
            r'\bxl\b': 'extra large',
            r'\blg\b': 'large',
            r'\bmd\b': 'medium',
            r'\bsm\b': 'small',
        }

    def clean_text(self, text: str) -> str:
        """Applies lowercase, removes punctuation, and standardizes terms."""
        if not isinstance(text, str):
            return ""

        # 1. Lowercase
        text = text.lower()

        # 2. Remove special characters (keep alphanumeric and spaces)
        text = re.sub(r'[^a-z0-9\s]', ' ', text)

        # 3. Replace abbreviations
        for pattern, replacement in self.replacements.items():
            text = re.sub(pattern, replacement, text)

        # 4. Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def normalize_dataframe(self, df: pd.DataFrame, column: str = 'product_name') -> pd.DataFrame:
        """Normalizes a specific column in a Pandas DataFrame."""
        if column not in df.columns:
            logger.error(f"Column '{column}' not found in dataframe.")
            return df
            
        logger.info(f"Normalizing text in column: {column}")
        df[f'{column}_clean'] = df[column].apply(self.clean_text)
        return df
