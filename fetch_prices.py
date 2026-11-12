import os
import json
import israeli_prices as ilp

def main():
    print("Starting Afula prices collection...")
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    target_city = "עפולה"
    collected_count = 0
    
    chains = ilp.list_chains()
    print(f"Checking {len(chains)} chains...")
    
    for chain_id in chains:
        try:
            stores_file = ilp.get_stores(chain_id)
            print(f"Chain [{chain_id}] has {len(stores_file.stores)} stores.")
            
            for store in stores_file.stores:
                city_str = str(getattr(store, 'city', '') or '')
                address_str = str(getattr(store, 'address', '') or '')
                store_name = str(getattr(store, 'store_name', '') or '')
                
                # בדיקה האם עפולה מופיעה באחד השדות של הסניף
                if target_city in city_str or target_city in address_str or target_city in store_name or "Afula" in city_str:
                    print(f"-> Found Afula match in [{chain_id}]: ID {store.store_id} | Name: {store_name} | City: {city_str}")
                    
                    prices = ilp.get_prices(chain_id, store_id=store.store_id)
                    items_data = [
                        {
                            "item_code": item.item_code,
                            "item_name": getattr(item, 'item_name', ''),
                            "price": str(item.price),
                            "gtin": getattr(item, 'gtin', None)
                        }
                        for item in prices.items
                    ]
                    
                    filename = f"{chain_id}_{store.store_id}_prices.json"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(items_data, f, ensure_ascii=False, indent=2)
                        
                    print(f"==> Saved {len(items_data)} items to {filepath}")
                    collected_count += 1
                    
        except Exception as e:
            print(f"Note: Could not process chain {chain_id}: {e}")

    print(f"Collection completed. Total files saved: {collected_count}")

if __name__ == "__main__":
    main()
