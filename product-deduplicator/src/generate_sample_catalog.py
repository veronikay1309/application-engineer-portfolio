import os
import pandas as pd
import random

def generate_catalog(output_path: str):
    """Generates a sample product catalog with injected duplicates."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    base_products = [
        {"id": "P001", "name": "Apple iPhone 14 Pro 128GB Black", "brand": "Apple", "upc": "194253401140", "price": 999.00},
        {"id": "P002", "name": "Samsung Galaxy S23 Ultra 256GB", "brand": "Samsung", "upc": "887276729011", "price": 1199.99},
        {"id": "P003", "name": "Sony WH-1000XM5 Wireless Headphones", "brand": "Sony", "upc": "27242922811", "price": 348.00},
        {"id": "P004", "name": "Logitech MX Master 3S Wireless Mouse", "brand": "Logitech", "upc": "97855174542", "price": 99.99},
        {"id": "P005", "name": "Hydro Flask 32 oz Wide Mouth Bottle", "brand": "Hydro Flask", "upc": "810028840222", "price": 44.95},
    ]

    dirty_products = [
        # EXACT: Same UPC, different ID and slightly different name
        {"id": "P001-B", "name": "iPhone 14 Pro 128GB (Black)", "brand": "Apple", "upc": "194253401140", "price": 999.00},
        
        # FUZZY: Same Brand, missing UPC, very similar name
        {"id": "P003-B", "name": "Sony WH 1000XM5 Wireless Noise Cancelling Headphones", "brand": "Sony", "upc": "", "price": 345.00},
        
        # FUZZY: Typos and abbreviations
        {"id": "P004-B", "name": "logitech mx master 3 s mouse blk", "brand": "Logitech", "upc": "", "price": 99.00},
        
        # FUZZY: abbreviation to standard mapping
        {"id": "P005-B", "name": "Hydro Flask 32oz Wide Mouth", "brand": "Hydro Flask", "upc": "", "price": 44.95},
    ]

    # Generate some random unrelated products to fill the catalog
    random_products = []
    for i in range(1, 41):
        random_products.append({
            "id": f"RND-{i:03d}",
            "name": f"Generic Item {i} ({random.choice(['blk', 'wht', 'red'])})",
            "brand": random.choice(["Generic", "Unknown Brand", "Store Brand"]),
            "upc": f"1000000{i:04d}",
            "price": round(random.uniform(10.0, 50.0), 2)
        })

    all_data = base_products + dirty_products + random_products
    # Shuffle
    random.shuffle(all_data)

    df = pd.DataFrame(all_data)
    # Rename for expected columns
    df = df.rename(columns={"id": "product_id", "name": "product_name"})
    
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} products (including exact and fuzzy duplicates) at {output_path}")

if __name__ == "__main__":
    generate_catalog("data/catalog.csv")
