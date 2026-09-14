import numbers
import unicodedata

char = 'ề'
char_nfd = unicodedata.normalize('NFD',char)

TONE_MARKS = {
    "\u0300": (2, "huyền"),
    "\u0303": (3, "ngã"),
    "\u0309": (4, "hỏi"),
    "\u0301": (5, "sắc"),
    "\u0323": (6, "nặng"),
}
TONE_NGANG = (1, "ngang")

def strip_tone(char) -> tuple[tuple[int, str], str]:
    tone = TONE_NGANG
    char_nfd = unicodedata.normalize('NFD', char)
    result = []
    for item in char_nfd:
        if item in TONE_MARKS:
            tone = TONE_MARKS[item]
        else:
            result.append(item)

    return tone, unicodedata.normalize('NFC', "".join(result))
