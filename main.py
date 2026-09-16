import parse
import re
import unicodedata

SYLLABLE = re.compile(r"[^\W\d_]+")

# Đồ án giữa kì 1
text = unicodedata.normalize("NFC", "Nếu biết rằng em đã có chồng, trời ơi người ấy có buồn không")
print(SYLLABLE.sub(lambda m: parse.parse(m.group()), text))

def parse_from_file(path: str):
    with open(path) as f:
        raw, result = '', ''
        for line in f:
            raw += line
            line = line.rstrip("\n")
            result += SYLLABLE.sub(lambda m: parse.parse(m.group()), line) + "\n"
        print(raw)
        print("--------------")
        print(result)

print("Bài tập phiên âm #1:")
parse_from_file("input/bai_1.txt")
print("==========")
print("Bài tập phiên âm #2:")
parse_from_file("input/bai_2.txt")
print("==========")
print("Bài tập phiên âm #3:")
parse_from_file("input/bai_3.txt")
print("==========")
print("Bài tập phiên âm #4:")
parse_from_file("input/bai_4.txt")