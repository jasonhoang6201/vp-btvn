from ast import Tuple
import unicodedata

# input chữ tiếng việt -> chữ ký âm
# step:
# 1. strip thanh điệu của chữ
TONE_MARKS = {
    "̀": (2, "huyền"),
    "̃": (3, "ngã"),
    "̉": (4, "hỏi"),
    "́": (5, "sắc"),
    "̣": (6, "nặng"),
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

# 2. phân tích thành âm đầu, âm phụ, âm chính, âm cuối
# 3. mapping từng phần thành ký âm
# âm đầu
ONSETS = [
    ("ngh", "ŋ"), ("ng", "ŋ"), ("gh", "ɣ"), ("ph", "f"), ("kh", "χ"),
    ("ch", "c"), ("tr", "ʈ"), ("nh", "ɲ"), ("gi", "z"), ("th", "tʼ"),
    ("b", "b"), ("m", "m"), ("v", "v"), ("t", "t"),
    ("đ", "d"), ("n", "n"), ("d", "z"), ("r", "ʐ"), ("x", "s"),
    ("s", "ʂ"), ("l", "l"), ("k", "k"), ("q", "k"), ("c", "k"),
    ("p", "p"), ("g", "ɣ"), ("h", "h")
]

# âm giữa
NUCLEI = [
    ("iê", "ie"), ("yê", "ie"), ("ia", "ie"), ("ya", "ie"),
    ("ươ", "ɯɤ"), ("ưa", "ɯɤ"), ("uô", "uo"), ("ua", "uo"),
    ("ôô", "o"), ("oo", "ɔ"), ("a", []), ("u", "u"), ("ô", "o"),
    ("i", "i"), ("y", "i"), ("ê", "e"), ("e", "ɛ"), ("ư", "ɯ"), ("ơ", "ɤ"),
    ("o", []), ("â", "ɤ̆"), ("ă", "ă"),
]

# âm cuối
CODAS = [
    ("ch", "k"), ("nh", "ŋ"), ("ng", "ŋ"),
    ("m", "m"), ("n", "n"), ("p", "p"), ("t", "t"), 
    ("c", "k"), ("o", "w"), ("u", "w"), ("y", "j"), ("i", "j"),
]

# âm giữa
MEDIAL = "w"

# xử lí special case
def mapping_special_case(char, conda):
    if char == "a":
        if conda in ("nh", "ch"):
            return "ɛ̆"
        if conda in ("u", "y"):
            return "ă"
        return "a"

    if char == "o":
        if conda in ("ng", "c"):
            return "ɔ̆"
        return "ɔ"

    for item in NUCLEI:
        if char == item[0]:
            return item[1]
    
    return ''

# tách chữ thành các thành phần: đầu, chính, cuối
def parse(word: str) -> str:
    onset, nuclei, condas = '', '', ''
    # mapping âm đầu
    for item, _ in ONSETS:
        if word.startswith(item):
            onset = item
            word = word[len(item):]
            break

    if word in ["o", "u", "i", "y"]:
        nuclei = word
    else:
        # mapping âm cuối
        for item, _ in CODAS:
            if word.endswith(item):
                condas = item
                word = word[:-len(item)]
                break

        # mapping âm chính
        for item, _ in NUCLEI:
            if word.endswith(item):
                nuclei = item
                word = word[:-len(item)]
                break

    print(onset, nuclei, condas)
    # todo: return ký âm

# word = input("Enter a word: ")

# tone, word = strip_tone(word)
# parse(word)
