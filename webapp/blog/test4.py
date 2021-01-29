
# f = open("static/dictionary.txt", "r")
# a = f.read()
# print(a) 

# a = [1,2,3,4]

# x = 1
# i = 0
# while i < x:
#     print(i)
#     a.pop()
#     i+=1
#     if a:
#         x+=

# from functools import reduce
# l1 = [1,2,3,4]
# l2 = [1,2]
# # result = list(reduce(lambda x,y : filter(lambda z: z not in y,x) ,l1,l2))
# # result = list(filter(lambda z: z not in l2, l1))
# result = [ x for x in l1 if x not in l2]
# # for i in result:
# #     print(i)
# print(result)
# print(l1)
# print(l2)

# def add_css_highlight_background(regex, item):
#     matches = re.finditer(regex, item, re.MULTILINE | re.IGNORECASE)
#     result = []
#     for matchNum, match in enumerate(matches, start=1):
#         result = item[0: match.start(
#         )] + fr"<span style=background-color:yellow>{item[match.start(): match.end()]}</span>" + item[match.end():]

#     return result

# import re

# url_regex = r"url=(\"|\')(.*)(\"|\')"
# video_id_regex = r"v=(.*)"
# figure_regex = r"<figure class=(\"|\')media(\"|\')><oembed url=(\"|\')(.*?)v=(\w*?)((\"|\')|&)(.*?)><\/oembed><\/figure>"

# txt = "qweqweqweqweq<figure class='media'><oembed url='https://www.youtube.com/watch?v=lfB5k5vokKU'></oembed></figure> qweqweqweqw <figure class='media'><oembed url='https://www.youtube.com/watch?v=lfB5k5vokKU111111'></oembed></figure> <figure class='media'><oembed url='https://www.youtube.com/watch?v=xI97sLMd1rM&amp;list=LL&amp;index=2&amp;t=1229s'></oembed></figure>"

# f = f"<figure class='media'><oembed url='https://www.youtube.com/watch?v={id}'></oembed></figure>"

# i = f"<div style='position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;'><iframe src='https://www.youtube.com/embed/{id}' style='position: absolute; width: 100%; height: 100%; top: 0; left: 0;' frameborder='0' allow='autoplay; encrypted-media' allowfullscreen=''></iframe></div>"

# x = re.findall(figure_regex, txt)
# print(x)
# ids = [ group[4] for group in x]
# print(ids)
# replace_regex = re.compile(r"<figure class=.*?><\/oembed><\/figure>")
# for id in ids:
#     txt = re.sub(replace_regex,f"<div style='position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;'><iframe src='https://www.youtube.com/embed/{id}' style='position: absolute; width: 100%; height: 100%; top: 0; left: 0;' frameborder='0' allow='autoplay; encrypted-media' allowfullscreen=''></iframe></div>",txt)
#     # txt = txt.replace(f"<figure class='media'><oembed url='https://www.youtube.com/watch?v={id}'></oembed></figure>", f"<div style='position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;'><iframe src='https://www.youtube.com/embed/{id}' style='position: absolute; width: 100%; height: 100%; top: 0; left: 0;' frameborder='0' allow='autoplay; encrypted-media' allowfullscreen=''></iframe></div>")

# print(txt)

# url = re.search(url_regex, txt).groups()[1]
# video_id = re.search(video_id_regex, url).groups()[0]
# result = f"<div style='position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;'><iframe src='https://www.youtube.com/embed/{video_id}' style='position: absolute; width: 100%; height: 100%; top: 0; left: 0;' frameborder='0' allow='autoplay; encrypted-media' allowfullscreen=''></iframe></div>"
# print(result)

from profanity_check import predict
from better_profanity import profanity

# txt = "fuck you"
# print(predict([txt]))
# print(profanity.)