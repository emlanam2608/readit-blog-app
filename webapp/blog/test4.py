
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

from functools import reduce
l1 = [1,2,3,4]
l2 = [1,2]
# result = list(reduce(lambda x,y : filter(lambda z: z not in y,x) ,l1,l2))
# result = list(filter(lambda z: z not in l2, l1))
result = [ x for x in l1 if x not in l2]
# for i in result:
#     print(i)
print(result)
print(l1)
print(l2)