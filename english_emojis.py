EMOJI_MAP = {
    "emoji red heart": "❤️",
    "emoji orange heart": "🧡",
    "emoji fire": "🔥",
    "emoji star": "⭐",
    "emoji music": "🎵",
    "emoji smile": "😊"
}

def replace_emojis(texto: str) -> str:
    for clave, emoji in EMOJI_MAP.items():
        if clave in texto.lower():
            texto = texto.replace(clave, emoji)
    return texto.strip()
