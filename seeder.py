import random
import uuid
import html

def generate_catalog():
    """Generates a rich catalog with SHORT emoji labels and interesting content."""
    
    compat_str = "📱 iPhone X и новее"

    # GAMES (Must be paid games)
    games = [
        {"name": "Minecraft", "desc": "🧱 **Лучшая песочница:** Строй, исследуй и играй с друзьями в полную версию."},
        {"name": "GTA: San Andreas", "desc": "🚗 **Тот самый Си-Джей:** Весь штат Сан-Андреас в твоём кармане."},
        {"name": "GTA: Vice City", "desc": "🌃 **Неоновые 80-е:** Крутые тачки и лучшая музыка того времени."},
        {"name": "Terraria", "desc": "⚔️ **Огромный мир:** Копай, сражайся и строй в лучшем 2D приключении."},
        {"name": "Stardew Valley", "desc": "🐥 **Твоя ферма:** Самый добрый и захватывающий симулятор жизни."},
        {"name": "Dead Cells", "desc": "🔥 **Крутой экшен:** Сражайся в меняющемся замке. Очень хардкорно!"},
        {"name": "Five Nights at Freddy's", "desc": "🐻 **Хоррор-хит:** Попробуй пережить ночь с аниматрониками."},
        {"name": "Geometry Dash Full", "desc": "⬛️ **Ритм-игра:** Все уровни и скины открыты. Прыгай под бит!"},
        {"name": "Monopoly", "desc": "🎲 **Настолка:** Классическая монополия без рекламы и доната."},
        {"name": "Hitman Sniper", "desc": "🎯 **Снайпер:** Работай максимально тихо и точно."},
        {"name": "The Room", "desc": "🗝 **Мистика:** Лучшая головоломка с невероятной атмосферой."},
        {"name": "Limbo", "desc": "🌑 **Мрачный квест:** Очень красивое и загадочное приключение."},
        {"name": "NBA 2K24 Arcade", "desc": "🏀 **Лучший баскетбол:** Графика как на приставке."}
    ]

    # MODS & SOCIAL (Very interesting apps)
    mods_categories = [
        {"game": "Telegram Plus", "types": ["💎 Premium: Всё открыто", "🚀 Функции: Скрытый режим", "🕵️ Шпион: Чат без следов"]},
        {"game": "TikTok Mod", "types": ["🎬 Фишка: Смена региона", "📥 Скачка: Без водяных знаков", "🚫 Без рекламы"]},
        {"game": "Instagram Mod", "types": ["📸 Фишка: Анонимные сторис", "⬇️ Скачка: Фото и видео", "💎 Premium функции"]},
        {"game": "Spotify Premium", "types": ["🎵 Музыка: Без рекламы", "⏭ Пропуски: Без границ", "🎧 Качество: Ultra HD"]},
        {"game": "YouTube Premium", "types": ["📺 Видео: В фоне", "🚫 Реклама: Удалена", "⬇️ Скачивание офлайн"]},
        {"game": "Minecraft Mods", "types": ["🦖 Мод: Динозавры", "🏡 Карта: Город будущего", "🌈 Шейдеры: Реалистичность"]},
        {"game": "Brawl Stars Mod", "types": ["🔥 Всё открыто: Скины и бойцы", "💎 Гемы: Много монет"]},
        {"game": "Roblox Hacks", "types": ["🎈 Чит: Полёт и скорость", "👻 Скин: Прозрачный"]}
    ]

    # PRO APPS
    apps = [
        {"name": "Capcut Pro", "desc": "🎬 **Топ монтаж:** Все платные эффекты, переходы и шрифты открыты."},
        {"name": "Procreate", "desc": "🎨 **Для рисования:** Инструмент номер один для всех художников."},
        {"name": "LumaFusion", "desc": "🎥 **Pro монтаж:** Если хочешь делать видео как в кино."},
        {"name": "Facetune Video", "desc": "✨ **Ретушь видео:** Идеальное лицо на видео в один клик."},
        {"name": "Alight Motion", "desc": "🎞 **Анимация:** Делай крутые мультики и спецэффекты."},
        {"name": "PicsArt Gold", "desc": "📸 **Фото-редактор:** Все VIP инструменты для твоих фото."},
        {"name": "Canva Pro", "desc": "🏮 **Дизайнер:** Тысячи готовых шаблонов для твоих сторис."},
        {"name": "GoodNotes 6", "desc": "📝 **Заметки:** Идеально для учёбы и планирования."},
        {"name": "Video Star++", "desc": "🌟 **Видео-эффекты:** Невероятные фильтры для твоих роликов."},
        {"name": "Shadowrocket", "desc": "🚀 **Proxy:** Утилита для стабильной работы сети."}
    ]

    # SHORTER CATEGORY NAMES with Emojis
    categories = {
        "games": {"title": "🎮 Игры", "items": []},
        "mods": {"title": "🧩 Моды", "items": []},
        "apps": {"title": "🛠 Софт", "items": []},
        "creative": {"title": "🎨 Дизайн", "items": []},
        "social": {"title": "📱 Соцсети ++", "items": []},
        "emulators": {"title": "🕹 Ретро", "items": []}
    }

    # Populate Games
    for g in games:
        item = {
            "id": str(uuid.uuid4()),
            "title": html.escape(g["name"]),
            "type": "ИГРА (PAID)",
            "category": "games",
            "desc": html.escape(g["desc"]),
            "compat": compat_str,
            "is_paid_version": True
        }
        categories["games"]["items"].append(item)

    # Populate Mods & Social
    for m in mods_categories:
        cat_key = "social" if any(x in m["game"] for x in ["Telegram", "TikTok", "Instagram", "YouTube", "Spotify"]) else "mods"
        for t in m["types"]:
            # Robust split
            parts = t.split(': ', 1)
            suffix = parts[1] if len(parts) > 1 else t
            
            item = {
                "id": str(uuid.uuid4()),
                "title": html.escape(f"{m['game']}: {suffix}"),
                "type": "МОД / ВЗЛОМ",
                "category": cat_key,
                "desc": html.escape(f"✨ Это особая версия приложения {m['game']}.\n{t}"),
                "compat": compat_str,
                "is_paid_version": False
            }
            categories[cat_key]["items"].append(item)

    # Populate Apps
    for a in apps:
        cat_key = "apps"
        if any(x in a["name"] for x in ["Procreate", "LumaFusion", "Facetune", "PicsArt", "Video Star", "Alight", "Canva", "Capcut"]):
            cat_key = "creative"
        
        item = {
            "id": str(uuid.uuid4()),
            "title": html.escape(a["name"]),
            "type": "PRO ВЕРСИЯ",
            "category": cat_key,
            "desc": html.escape(a["desc"]),
            "compat": compat_str,
            "is_paid_version": True
        }
        categories[cat_key]["items"].append(item)

    # Extra fillers for Emulators
    emulators = [
        {"name": "Delta Emulator", "desc": "🕹 **Nintendo на iOS:** Играй в Марио и Покемонов без проблем."},
        {"name": "PPSSPP Gold", "desc": "🎮 **PSP на iPhone:** Любимые игры в высоком качестве."}
    ]
    for e in emulators:
        item = {
            "id": str(uuid.uuid4()),
            "title": e["name"],
            "type": "ЭМУЛЯТОР",
            "category": "emulators",
            "desc": e["desc"],
            "compat": compat_str,
            "is_paid_version": True
        }
        categories["emulators"]["items"].append(item)

    # Final Shuffle
    for cat in categories.values():
        random.shuffle(cat["items"])

    return categories

if __name__ == "__main__":
    import json
    data = generate_catalog()
    print(json.dumps(data, indent=2, ensure_ascii=False))
