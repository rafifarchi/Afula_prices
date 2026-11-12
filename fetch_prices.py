import os
from israeli_prices import PriceRetriever

def main():
    print("Starting Afula prices collection workflow...")
    
    # יצירת תיקיית פלט לשמירת הקבצים המקומיים
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # כאן נשלב בהמשך את הגדרת הרשתות והסניפים בעפולה
    print(f"Output directory ready at: {output_dir}")
    
    # דוגמה לשלב הבא: אתחול והורדה
    # retriever = PriceRetriever()
    # כאן נוסיף את הלוגיקה שמורידה את המחירים לסניפים הנבחרים

    print("Workflow step completed successfully.")

if __name__ == "__main__":
    main()
