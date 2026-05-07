import re

from transliterate import translit


def client_name_to_username(name: str) -> str:
    transliterated = translit(name, "ru", reversed=True)
    cleaned = re.sub(r"[^\w]", "_", transliterated)
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned.strip("_").lower()
