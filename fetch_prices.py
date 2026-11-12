import os
import json
import israeli_prices as ilp

def main():
    print("Starting Afula prices collection...")
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    target_city = "עפולה"
    collected_count = 0
    
    # מקבלים את רשימת כל הרשתות הנתמכות בספרייה
    chains = ilp.list_chains()
    print(f"Checking {len(chains)} chains for stores in Afula...")
    
    for chain_id in chains:
        try:
            # שליפת רשימת הסניפים של הרשת
            stores_file = ilp.get_stores(chain_id)
            
            for store in stores_file.stores:
                # בדיקה האם הסניף נמצא בעפולה (לפי העיר או כתובת)
                city_str = getattr(store, 'city', '') or ''
                address_str = getattr(store, 'address', '') or ''
                
                if target_city in city_str or target_city in address_str:
                    print(f"Found Afula store in [{chain_id}]: ID {store.store_id} - {getattr(store, 'store_name', '')}")
                    
                    # הורדת מחירון מלא לסניף הספציפי
                    prices = ilp.get_prices(chain_id, store_id=store.store_id)
                    
                    # המרת המוצרים למבנה נתונים לשמירה בקובץ JSON
                    items_data = [
                        {
                            "item_code": item.item_code,
                            "item_name": getattr(item, 'item_name', ''),
                            "price": str(item.price),
                            "gtin": getattr(item, 'gtin', None)
                        }
                        for item in prices.items
                    ]
                    
                    # שמירת הקובץ בתיקיית הפלט
                    filename = f"{chain_id}_{store.store_id}_prices.json"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(items_data, f, ensure_ascii=False, indent=2)
                        
                    print(f"-> Saved {len(items_data)} items to {filepath}")
                    collected_count += 1
                    
        except Exception as e:
            # במקרה שפורטל של רשת מסוימת לא זמין זמנית, ממשיכים הלאה ברשתות האחרות
            print(f"Note: Could not fetch stores for chain {chain_id}: {e}")

    print(f"Collection completed successfully. Total Afula files saved: {collected_count}")

if __name__ == "__main__":
    main()
