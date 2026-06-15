import argparse
import logging
import os
import pandas as pd
from src.normalizer import TextNormalizer
from src.deduplicator import Deduplicator
from src.reporter import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Product Catalog Deduplicator")
    parser.add_argument("--catalog", required=True, help="Path to catalog CSV")
    parser.add_argument("--output-dir", default="output", help="Directory for reports")
    parser.add_argument("--fuzzy-threshold", type=int, default=85, help="0-100 threshold for fuzzy matches")
    
    args = parser.parse_args()

    if not os.path.exists(args.catalog):
        logger.error(f"Catalog file not found: {args.catalog}")
        return

    logger.info("1. Loading Catalog...")
    df = pd.read_csv(args.catalog)
    
    # Fill NAs
    df['upc'] = df['upc'].fillna('').astype(str)
    df['brand'] = df['brand'].fillna('UNKNOWN')

    logger.info("2. Normalizing Text...")
    normalizer = TextNormalizer()
    df = normalizer.normalize_dataframe(df, column='product_name')

    logger.info("3. Finding Duplicates...")
    deduper = Deduplicator(fuzzy_threshold=args.fuzzy_threshold)
    
    # Exact Matches (Same UPC)
    exact_clusters = deduper.find_exact_matches(df, identifier_col='upc')
    
    # Fuzzy Matches (Similar Names within the same Brand)
    fuzzy_clusters = deduper.find_fuzzy_matches(df, block_col='brand', text_col='product_name_clean')

    logger.info("4. Generating Reports...")
    reporter = ReportGenerator()
    reporter.generate(exact_clusters, fuzzy_clusters, args.output_dir)
    
    total = len(exact_clusters) + len(fuzzy_clusters)
    logger.info(f"✅ Deduplication complete. Found {total} suspected duplicate clusters.")

if __name__ == "__main__":
    main()
