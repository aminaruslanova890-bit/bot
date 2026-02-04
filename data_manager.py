import json
import os
from seeder import generate_catalog

DATA_FILE = "catalog.json"

def load_data():
    """Loads catalog data from JSON. Generates if missing."""
    if not os.path.exists(DATA_FILE):
        print("⚡️ Каталог не найден. Генерируем новый контент...")
        data = generate_catalog()
        save_data(data)
        return data
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("⚠️ Ошибка чтения каталога. Пересоздаем...")
        data = generate_catalog()
        save_data(data)
        return data

def save_data(data):
    """Saves catalog data to JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_category(category_key):
    """Returns items for a specific category."""
    data = load_data()
    return data.get(category_key, {})

def get_item(item_id):
    """Searches for an item by ID across all categories."""
    data = load_data()
    for cat in data.values():
        for item in cat["items"]:
            if item["id"] == item_id:
                return item
    return None
