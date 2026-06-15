import pandas as pd
from thefuzz import fuzz
import logging

logger = logging.getLogger(__name__)

class Deduplicator:
    """Identifies exact and fuzzy duplicates in a product catalog."""

    def __init__(self, fuzzy_threshold: int = 85):
        self.fuzzy_threshold = fuzzy_threshold

    def find_exact_matches(self, df: pd.DataFrame, identifier_col: str = 'upc') -> list:
        """Groups products that share the exact same unique identifier (UPC/ASIN)."""
        logger.info(f"Running Exact Matcher on '{identifier_col}'...")
        
        duplicates = []
        
        # Drop rows where identifier is missing
        valid_df = df.dropna(subset=[identifier_col])
        valid_df = valid_df[valid_df[identifier_col] != ""]
        
        # Group by the identifier
        grouped = valid_df.groupby(identifier_col)
        
        for upc, group in grouped:
            if len(group) > 1:
                duplicates.append({
                    "match_type": "EXACT",
                    "match_key": f"{identifier_col}:{upc}",
                    "confidence": 100,
                    "products": group.to_dict('records')
                })
                
        logger.info(f"Found {len(duplicates)} exact match clusters.")
        return duplicates

    def find_fuzzy_matches(self, df: pd.DataFrame, block_col: str = 'brand', text_col: str = 'product_name_clean') -> list:
        """Finds fuzzy matches by comparing text only within the same 'block' (e.g. brand) to optimize O(N^2)."""
        logger.info(f"Running Fuzzy Matcher on '{text_col}', blocking by '{block_col}'...")
        
        duplicates = []
        visited_ids = set()

        # Group by the blocking column to reduce comparison space
        grouped = df.groupby(block_col)

        for brand, group in grouped:
            records = group.to_dict('records')
            n = len(records)
            
            # O(N^2) comparison within the block
            for i in range(n):
                prod_a = records[i]
                if prod_a['product_id'] in visited_ids:
                    continue
                    
                cluster = [prod_a]
                
                for j in range(i + 1, n):
                    prod_b = records[j]
                    if prod_b['product_id'] in visited_ids:
                        continue
                        
                    # Calculate Levenshtein distance similarity ratio (0-100)
                    score = fuzz.token_sort_ratio(prod_a[text_col], prod_b[text_col])
                    
                    if score >= self.fuzzy_threshold:
                        prod_b['_fuzzy_score'] = score
                        cluster.append(prod_b)
                        visited_ids.add(prod_b['product_id'])
                
                if len(cluster) > 1:
                    visited_ids.add(prod_a['product_id'])
                    # Calculate average confidence of the cluster
                    avg_score = sum(p.get('_fuzzy_score', 100) for p in cluster[1:]) / (len(cluster) - 1)
                    
                    duplicates.append({
                        "match_type": "FUZZY",
                        "match_key": f"brand:{brand}",
                        "confidence": int(avg_score),
                        "products": cluster
                    })

        logger.info(f"Found {len(duplicates)} fuzzy match clusters.")
        return duplicates
