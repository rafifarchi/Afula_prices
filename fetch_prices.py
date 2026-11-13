import os
import json
import israeli_prices as ilp

def main():
    print("Starting Afula comprehensive prices collection...")
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # חיפוש רחב וגמיש לכיסוי מלא של כל הסניפים והפארמים בעפולה
    target_keywords = ["עפול", "afula"]
    collected_count = 0
    
    chains = ilp.list_chains()
    print(f"Checking {len(chains)} chains...")
    
    for chain in chains:
        if not getattr(chain, 'implemented', True):
            continue
            
        chain_slug = chain.slug
        
        try:
            stores_file = ilp.get_stores(chain_slug)
            if not stores_file or not stores_file.stores:
                continue
            
            for store in stores_file.stores:
                city_str = str(getattr(store, 'city', '') or '')
                address_str = str(getattr(store, 'address', '') or '')
                store_name = str(getattr(store, 'store_name', '') or '')
                
                full_text = f"{city_str} {address_str} {store_name}".lower()
                
                if any(kw in full_text for kw in target_keywords):
                    print(f"-> Found Afula match in [{chain_slug}]: ID {store.store_id} | Name: {store_name} | City: {city_str}")
                    
                    try:
                        prices = ilp.get_prices(chain_slug, store_id=store.store_id)
                        
                        # חילוץ מקיף של כל השדות העשירים כולל נתוני יצרן, מידה ותמונה
                        items_data = [
                            {
                                "chain": chain_slug,
                                "store_id": store.store_id,
                                "store_name": store_name,
                                "item_code": getattr(item, 'item_code', ''),
                                "item_name": getattr(item, 'item_name', '') or getattr(item, 'name', ''),
                                "manufacturer_name": getattr(item, 'manufacturer_name', '') or getattr(item, 'manufacture_name', ''),
                                "manufacturer_country": getattr(item, 'manufacturer_country', ''),
                                "category": getattr(item, 'category', '') or getattr(item, 'item_category', ''),
                                "unit_of_measure": getattr(item, 'unit_of_measure', '') or getattr(item, 'unit_qty', ''),
                                "quantity": str(getattr(item, 'quantity', '') or ''),
                                "price": str(item.price),
                                "is_weighted": getattr(item, 'is_weighted', False),
                                "image_url": getattr(item, 'image_url', '') or getattr(item, 'picture', '') or getattr(item, 'img', None),
                                "gtin": getattr(item, 'gtin', None)
                            }
                            for item in prices.items
                        ]
                        
                        filename = f"{chain_slug}_{store.store_id}_prices.json"
                        filepath = os.path.join(output_dir, filename)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(items_data, f, ensure_ascii=False, indent=2)
                            
                        print(f"==> Saved {len(items_data)} items (with full metadata) to {filepath}")
                        collected_count += 1
                        
                    except Exception as price_err:
                        print(f"   Note: Could not fetch prices for store {store.store_id} in {chain_slug}: {price_err}")
                        
        except Exception as e:
            print(f"Note: Could not process stores for chain {chain_slug}: {e}")

    print(f"Collection completed. Total files saved: {collected_count}")

if __name__ == "__main__":
    main()
