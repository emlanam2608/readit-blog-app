import json
from bson  import json_util
import pymongo

client = pymongo.MongoClient()
db = client['blog_data']
collection = db["blog_post"]
collection.create_index([('title', 'text'), ('content.section_title', 'text'), ('content.section_content', 'text')])
raw_keys = "coding coder"
raw_keywords = raw_keys.split(" ")
data = []
keywords = []
for raw_keyword in raw_keywords:
    # x = collection.find({"$text": {"$search": f'"{keyword}"'}})
    x = collection.find({"$text": {"$search": raw_keyword}})
    print(x.count())
    keyword = collection.find({"$text": {"$search": raw_keyword}}).explain()["queryPlanner"]["winningPlan"]["parsedTextQuery"]["terms"]
    if keyword:
        keywords.append(keyword[0])
    print(keywords)
    for y in x:
        if y not in data:
            data.append(y)

# for d in data:
#     print(d)

result = []
for d in data:
    raw_d = json.dumps(d, default=json_util.default)

    f = open("static/dictionary.txt", "r")
    temp = f.read()
    temp = temp.replace("'", '"')
    temp = temp[temp.find("{"):-1]
    dictionary = json.loads(temp)
    f.close()

    for keyword in keywords:
        if keyword in dictionary:
            for value in dictionary[keyword]:
                raw_d = raw_d.replace(value, fr'<span style=\"background-color=yellow;\">{value}</span>')
        else:
            raw_d = raw_d.replace(keyword, fr'<span style=\"background-color=yellow;\">{keyword}</span>')

    result.append(json.loads(raw_d))

for r in result:
    print(r)