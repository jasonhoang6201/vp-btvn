word = input("Enter a word: ")

# tách chữ theo âm đầu, âm đệm, âm chính, âm cuối
# âm đầu
ONSET = [
    ['ngh'],
    ['ch','tr','th','ph','kh','nh','gh','ng','gi','qu'],
    ['b','m','v','t','đ','n','d','r','x','s','l','k','c','g','h','q']
]

# 
NUCLEUS = ['iê', 'yê', 'ia', 'ya', 'ươ', 'ưa', 'uô', 'ua', 'oo', 'ôô']

ENDINGS = [
    ['ng', 'nh', 'ch'],
    ['m', 'n', 'p', 't', 'c', 'o', 'u', 'i', 'y']
]

onset = ''
medial = ''
nucleus = ''
coda = ''

for i in ONSET:
    for j in i:
        if word.startswith(j):
            onset = j
            word = word[len(j):]
            break
    if onset != '':
        break

for i in ENDINGS:
    for j in i:
        if word.endswith(j):
            coda = j
            word = word[:-len(j)]
            break
    if coda != '':
        break

if len(word) == 1:
    nucleus = word
else:
    for i in NUCLEUS:
        if word.endswith(i):
            nucleus = i
            word = word[:-len(i)]
            break
        if nucleus != '':
            break
    

    # if nucleus is not found, then it is a single character
    if nucleus == '':
        nucleus = word[-1]
        word = word[:-1]
    
    if word != '':
        medial = word

print('onset:', onset)
print('medial:', medial)
print('nucleus:', nucleus)
print('coda:', coda)

# 1. fix âm cuối có thể không có
# 2. fix tách dấu