EMOJI_MAP = {
    "emoji corazón rojo": "❤️",
    "emoji corazón naranja": "🧡",
    "emoji fuego": "🔥",
    "emoji estrella": "⭐",
    "emoji musica": "🎵",
    "emoji sonrisa": "😊"
}

def replace_emojis(texto: str) -> str:
    for clave, emoji in EMOJI_MAP.items():
        if clave in texto.lower():
            texto = texto.replace(clave, emoji)
    return texto.strip()

