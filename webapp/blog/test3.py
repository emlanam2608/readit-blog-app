import json

from nltk.stem.porter import *
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import words, brown
import nltk

stemmer = EnglishStemmer()
# x = stemmer.stem('jack-of-all-trad')
# print(x)
# nltk.download('brown')
# print(True if "code" in brown.words() else False)


# vocab = set(w.lower().replace("'","") for w in brown.words())
# print(vocab)
# dictionary = nltk.defaultdict(list)
# for v in vocab:
#     dictionary[f'{stemmer.stem(v)}'].append(v)
#
# print(True if dictionary['code'] else False)
# f = open("static/dictionary.txt", "w+")
# f.write(str(dictionary))
# f.close()

key = "code"
f = open("static/dictionary.txt", "r")
a = f.read()
a = a.replace("'", '"')
a = a[a.find("{"):-1]
print(a)
b = json.loads(a)
print(type(b))
print(b)
f.close()
print(True if b[key] else False)

