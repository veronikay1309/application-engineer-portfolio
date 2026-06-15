import pandas as pd
from src.deduplicator import Deduplicator

def test_find_exact_matches():
    df = pd.DataFrame([
        {"product_id": "1", "upc": "123"},
        {"product_id": "2", "upc": "123"},
        {"product_id": "3", "upc": "456"},
        {"product_id": "4", "upc": ""} # Missing UPC should be ignored
    ])
    
    deduper = Deduplicator()
    clusters = deduper.find_exact_matches(df, identifier_col="upc")
    
    assert len(clusters) == 1
    assert clusters[0]["match_type"] == "EXACT"
    assert len(clusters[0]["products"]) == 2

def test_find_fuzzy_matches():
    df = pd.DataFrame([
        {"product_id": "1", "brand": "Apple", "name_clean": "apple iphone 14 pro 128gb black"},
        {"product_id": "2", "brand": "Apple", "name_clean": "iphone 14 pro 128gb black apple"}, # Same tokens, different order
        {"product_id": "3", "brand": "Samsung", "name_clean": "galaxy s23 ultra"}
    ])
    
    deduper = Deduplicator(fuzzy_threshold=90) # High threshold, token_sort_ratio handles out of order
    clusters = deduper.find_fuzzy_matches(df, block_col="brand", text_col="name_clean")
    
    assert len(clusters) == 1
    assert clusters[0]["match_type"] == "FUZZY"
    assert clusters[0]["match_key"] == "brand:Apple"
    assert len(clusters[0]["products"]) == 2
