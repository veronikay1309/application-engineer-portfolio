from src.normalizer import TextNormalizer
import pandas as pd

def test_clean_text():
    normalizer = TextNormalizer()
    
    assert normalizer.clean_text("Apple iPhone 14 Pro!!") == "apple iphone 14 pro"
    assert normalizer.clean_text("Hydro Flask 32 oz blk") == "hydro flask 32 ounces black"
    assert normalizer.clean_text("LOGITECH MX MASTER   3S") == "logitech mx master 3s"

def test_normalize_dataframe():
    normalizer = TextNormalizer()
    df = pd.DataFrame({"name": ["Test Item blk", "Item 2 oz"]})
    
    result = normalizer.normalize_dataframe(df, column="name")
    assert "name_clean" in result.columns
    assert result.iloc[0]["name_clean"] == "test item black"
    assert result.iloc[1]["name_clean"] == "item 2 ounces"
