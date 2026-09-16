import unicodedata

# input chữ tiếng việt -> chữ ký âm
# step:
# 1. strip thanh điệu của chữ
TONE_MARKS = {
    "̀": ("2", "huyền"),
    "̃": ("3", "ngã"),
    "̉": ("4", "hỏi"),
    "́": ("5", "sắc"),
    "̣": ("6", "nặng"),
}
TONE_NGANG = ("1", "ngang")

def strip_tone(word) -> tuple[tuple[str, str], str]:
    tone = TONE_NGANG
    word_nfd = unicodedata.normalize('NFD', word)
    result = []
    for item in word_nfd:
        if item in TONE_MARKS:
            tone = TONE_MARKS[item]
        else:
            result.append(item)

    return tone, unicodedata.normalize('NFC', "".join(result))

# 2. phân tích thành âm đầu, âm phụ, âm chính, âm cuối
# 3. mapping từng phần thành ký âm
# âm đệm
MEDIAL = "w"

# âm đầu
ONSETS = [
    ("qu", "k" + MEDIAL),
    ("ngh", "ŋ"), ("ng", "ŋ"), ("gh", "ɣ"), ("ph", "f"), ("kh", "χ"),
    ("ch", "c"), ("tr", "ʈ"), ("nh", "ɲ"), ("gi", "z"), ("th", "tʼ"),
    ("b", "b"), ("m", "m"), ("v", "v"), ("t", "t"),
    ("đ", "d"), ("n", "n"), ("d", "z"), ("r", "ʐ"), ("x", "s"),
    ("s", "ʂ"), ("l", "l"), ("k", "k"), ("q", "k"), ("c", "k"),
    ("p", "p"), ("g", "ɣ"), ("h", "h"),
    ("", "ʔ")
]

# âm chính
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

# xử lí special case cho âm chính
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
def mapping(word: str) -> str:
    word = word.lower()
    onset, nuclei, conda = None, None, None
    # mapping âm đầu
    for item in ONSETS:
        if word.startswith(item[0]):
            onset = item
            word = word[len(item[0]):]

            if item[0] == "gi":
                if word == "":
                    word = "i"
                elif word[0] not in "aăâeêoôơuưy":
                    word = "i" + word
                elif word[0] == "ê":
                    word = "i" + word
            break

    # special case: 1 từ cuối là âm chính hoặc âm cuối là "y"
    if len(word) == 1 or (word[-1] == "y" and word[-2] not in ("a", "â")):
        nuclei = word[-1]
        word = word[:-1]
    else:
        # mapping âm cuối
        for item in CODAS:
            if word.endswith(item[0]):
                conda = item
                word = word[:-len(item[0])]
                break

        # mapping âm chính
        for item in NUCLEI:
            if word.endswith(item[0]):
                nuclei = item[0]
                word = word[:-len(item[0])]
                break
    
    result = ''
    if onset:
        result += onset[1]
    if len(word) >= 1:
        result += MEDIAL
    result += mapping_special_case(nuclei, conda[0] if conda else "")
    if conda:
        result += conda[1]
    
    return result

def parse(word: str) -> str: 
    word = word.lower()
    tone, word = strip_tone(word=word)
    return mapping(word) + tone[0]