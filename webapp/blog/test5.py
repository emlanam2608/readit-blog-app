# query_comments = [
#     {
#         "id":1,
#         "level":0,
#         "pr":0
#     },
#     {
#         "id":2,
#         "level":1,
#         "pr":1
#     },
#     {
#         "id":3,
#         "level":2,
#         "pr":2
#     },
#     {
#         "id":4,
#         "level":3,
#         "pr":3
#     },
#     {
#         "id":5,
#         "level":0,
#         "pr":0
#     },
#     {
#         "id":6,
#         "level":1,
#         "pr":5
#     },
#     {
#         "id":7,
#         "level":2,
#         "pr":6
#     },
#     {
#         "id":8,
#         "level":3,
#         "pr":7
#     },
# ]

query_comments = [{'id': 11, 'post_id': 34, 'parent_id': None, 'reply_to': '', 'author_username': 'emlanam26082', 'author_id': 3, 'content': '1', 'created_at': {'day': '24', 'month': 'Jan', 'year': '2021', 'hour': '10', 'minute': '49', 'second': '25', 'AM-PM': 'p.m.'}, 'hidden': False, 'flag': False, 'level': '0'}, {'id': 12, 'post_id': 34, 'parent_id': 11, 'reply_to': '', 'author_username': 'emlanam26082', 'author_id': 3, 'content': '2', 'created_at': {'day': '24', 'month': 'Jan', 'year': '2021', 'hour': '10', 'minute': '53', 'second': '37', 'AM-PM': 'p.m.'}, 'hidden': False, 'flag': False, 'level': '1'}, {'id': 13, 'post_id': 34, 'parent_id': 12, 'reply_to': '', 'author_username': 'emlanam26082', 'author_id': 3, 'content': '3', 'created_at': {'day': '24', 'month': 'Jan', 'year': '2021', 'hour': '10', 'minute': '54', 'second': '09', 'AM-PM': 'p.m.'}, 'hidden': False, 'flag': False, 'level': '2'}]

level_array = []
# for c in query_comments:
# print([comment for comment in query_comments if comment["level"]=="0"])
# level_array.append([comment for comment in query_comments if comment["level"]=="0"])
# print(level_array)


x = 0
y = 1
while x < y:
    level_array.append([comment for comment in query_comments if comment["level"]==str(x)])
    query_comments = [ comment for comment in query_comments if comment not in level_array[x]]
    x += 1
    if query_comments:
        y += 1

for i in range(len(level_array)-1):
    temp = {}
    for c in level_array[-1]:
        if str(c["parent_id"]) in temp:
            temp[str(c["parent_id"])].append(c)
        else:
            temp[str(c["parent_id"])] = [c]
    
    for c in level_array[-2]:
        c['child'] = [ item for item in temp[str(c["id"])]]

    level_array.pop()

level_array = [ i for j in level_array for i in j]
print(level_array)