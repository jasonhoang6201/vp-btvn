def parse_from_file(path: str):
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            res = line.split('\t')[0].strip()
            if res:
                print(res)

print("Đồ án giữa kì 2:")

parse_from_file("input/dictionary/VDic_uni.txt")
print("==========")
