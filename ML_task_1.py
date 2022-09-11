import random, pickle
import re
n=3 # длина элемента N-граммы
m=6 # длина генерируемого текста

# Открытие файла
def read_file(s):
    text=[] # массив строк
    with open(s, 'r', encoding='utf-8') as Fdocs:
        for line in Fdocs:
            doc=line  # считываем строку
            text.append(doc)
    return text

# Создание N-грамм
def generate_ngrams(text, n):
    docs=read_file(text)
    tokens=[]
    for doc in docs:
        doc=doc.lower()
        doc=re.sub(r'\W', ' ', doc) # замена всех символов, отличающихся от букв и цифр, на пробелы
        tokens.extend(re.split(r' +',doc))
    print(tokens)
    tokens = (n-1)*['FIRST']+tokens
    ngrams=[(tuple([tokens[i-p-1] for p in reversed(range(n))])) for i in range(n-1, len(tokens))]

    return ngrams

# Создание словаря, определение частоты слова (обучение)
def generate_dictionary(ngrams, n):
    dictionary={ngram: {} for ngram in ngrams}

    for i in range(len(ngrams)-1):
        next_word=ngrams[i+1][n-1]
        if next_word in dictionary[ngrams[i]]:
            dictionary[ngrams[i]][next_word]+=1
        else:
            dictionary[ngrams[i]][next_word]=1

    return dictionary

# Выбор токена в зависимости от частоты его встречи
def pick_token(tokens):
    rand_sequence=[]
    for token in tokens:
        p=tokens[token]
        rand_sequence+=[token]*p

    return random.choice(rand_sequence)

# Выбор наиболее похожего элемента (если заданного нет в списке)
def pick_close_elem(dictionary, elem):
    n=len(elem)
    best_elem, best_value=random.choice(list(dictionary.items()))
    max_count=0

    for dict_elem in dictionary:
        if dict_elem[n-1]==elem[n-1]:
            count=1
            for i in range(n-1):
                if dict_elem[i]==elem[i]:
                    count+=1
            if count>max_count:
                best_elem=dict_elem
                max_count=count
            if max_count==n-1:
                break

    return best_elem

# Выбор токена с опорой на заданный элемент (если такого элемента нет в словаре, то выбирается похлжий)
def get_token(dictionary, elem):
    if elem in dictionary:
        tokens=dictionary[elem]
        token=pick_token(tokens)
    else:
        close_elem=pick_close_elem(dictionary, elem)
        #print('closest elem = ', close_elem)
        tokens=dictionary[close_elem]
        token=pick_token(tokens)

    return token

# Генерация очередного предсказанного слова
def predict_token(dictionary, n, text):
    new_text=(n-1)*['FIRST']+text
    p=new_text.index('')
    elem=tuple(new_text[p-n:p])
    #print('elem = ', elem)
    return get_token(dictionary, elem)

# Функция генерации текста
def generate_text(dictionary, n, ngrams, m):
    generate_token=m*[''] # генерируется текст длиной в m токенов
    rand_ngram=random.choice(ngrams) # случайно выбирается слово на основе которого происходит генерация 
    generate_token[0]=rand_ngram[0]

    print("Given word: ", generate_token[0])

    for i in range(1, m):
        word = predict_token(dictionary, n, generate_token)
        generate_token[i]=word
        #print('predicted word is ', word)

    text=''
    for word in generate_token:
        text+=word+' '
    return text

# вводится путь к файлу с текстом, пример: 'C:\\Users\\ishen\\source\\repos\\ML_task_1\\ML_task_1\\text2.txt'
ngrams=generate_ngrams('C:\\Users\\ishen\\source\\repos\\ML_task_1\\ML_task_1\\text2.txt', n)
print(ngrams)
diction=generate_dictionary(ngrams, n)
with open('data.pickle', 'wb') as f:
    pickle.dump(diction, f)
with open('data.pickle', 'rb') as f:
    new_diction=pickle.load(f)
text=generate_text(new_diction, n, ngrams, m)
print('Text: ', text)