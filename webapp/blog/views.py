import json
from urllib.parse import unquote
from random import sample
import pymongo
from bson import ObjectId, json_util
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
import re
from django.contrib.auth import login, authenticate, logout, get_user, get_user_model, validators
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from blog.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from blog.models import Post, Comment, Category
from django.utils.translation import gettext as _
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)

MAX_POST_HOME_PAGE = 4
MAX_POST_CATEGORY_PAGE = 4
MAX_PAGE = 3
MAX_SEARCH_RESULT = 10


# Create your views here.


@login_required
def admin(request):
    user = get_user(request)
    if user.is_superuser:
        return render(request, "admin.html")
    else:
        return HttpResponseNotAllowed("Not allowed")


@login_required
def create_post(request):
    user = get_user(request)
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        category = received_json_data["category"]
        title = received_json_data["title"]
        content = received_json_data["content"]
        thumbnail = received_json_data["thumbnail"]
        author = user
        author_username = user.username
        post = Post(
            category=Category.objects.get(name=category),
            title=title,
            content=content,
            thumbnail=thumbnail,
            author=author,
            author_username=author_username
        )
        post.save()
        if post:
            data = {
                "id": post.id,
                "title": post.title
            }
            print(data)
            # return render(request, "create_post.html", {"post":data})
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, "create_post.html")

    


@login_required
def update_post(request, id):
    user = get_user(request)
    User = get_user_model()
    if id == "all":
        posts = User.objects.get(id = user.id).posts.all()
        data = []
        for post in posts:
            data.append({"id": post.id, "title": post.title})
        return render(request, "posts_management.html", {"posts": data})
    else:
        if request.method == "POST":
            received_json_data = json.loads(request.body)
            category = received_json_data["category"]
            title = received_json_data["title"]
            content = received_json_data["content"]
            thumbnail = received_json_data["thumbnail"]
            post = get_object_or_404(Post, id=int(id))
            post.category = Category.objects.get(name=category)
            post.title = title
            post.content = content
            post.thumbnail = thumbnail
            post.save()
            return redirect(f"/blog/admin/post/update/{int(id)}")
        else:
            post = get_object_or_404(Post, id=int(id))
            if post.author.id == user.id:
                data = {
                    "id": post.id,
                    "category": post.category,
                    "title": post.title,
                    "content": post.content,
                    "thumbnail": f"<figure class='image'><img src='{post.thumbnail}'></figure>" if post.thumbnail else ""
                }
                return render(request, "update_post.html", {"post": data})
            else:
                return HttpResponseNotAllowed("Not allowed")

def validate_uname(username):
    User = get_user_model()
    try:
        if User.objects.get(username=username):
            return 0
    except ObjectDoesNotExist:
        return 1
    except MultipleObjectsReturned:
        return 0
    return 1

def validate_email_custom(email):
    User = get_user_model()
    try:
        validate_email(email)
        if User.objects.get(email=email):
            return 2
        return 1
    except ValidationError as e:
        return 0
    except ObjectDoesNotExist:
        return 1
    except MultipleObjectsReturned:
        return 2

@login_required
def profile(request):
    if request.method == "POST":
        print(request.body)
        received_json_data = json.loads(request.body)
        
        username = received_json_data['username']
        last_name = received_json_data['last_name']
        first_name = received_json_data['first_name']
        email = received_json_data['email']
        user = get_user(request)
        error = ""
        # if not validate_uname(username):
        #     error += "Username has been used! "
        if email != user.email:
            temp = validate_email_custom(email)
            if temp == 0:
                error += "Email is invalid! "
            elif temp == 2:
                error += "Email has been used! "
        
        if error != "":
            print(error)
            # return render(request, "profile.html", {"error": {'message': error}})
            return HttpResponse(json.dumps({'message': error}), content_type="application/json")
            

        
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return render(request, "profile.html", {"user": user})
    else:
        user = get_user(request)
        return render(request, "profile.html", {"user": user})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            redirect_to = (
                request.POST.get("next", "")
                .replace("/accounts/login/?next=", "")
                .replace("/en", "")
            )
            if "accounts/login/" in redirect_to or redirect_to == "" or "accounts/signup/" in redirect_to:
                return redirect("home")
            return HttpResponseRedirect(redirect_to)
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        raw_password = request.POST["password"]
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            redirect_to = str(request)[str(request).find("next") + 8: -2]
            print(redirect_to)
            # redirect_to = (
            #     request.POST.get("next", "")
            #     .replace("/accounts/login/?next=", "")
            #     .replace("/en", "")
            #     .replace("/vi","")
            # )
            if "accounts/login/" in redirect_to or redirect_to == "" or "accounts/signup/" in redirect_to:
                return redirect("home")
            return HttpResponseRedirect(redirect_to)
        else:
            form = AuthenticationForm()
            error = "Username or password is not correct"
            return render(request, "login.html", {"form": form, "error": error})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    redirect_to = request.GET.get("next", "")
    print(redirect_to)
    return HttpResponseRedirect(redirect_to)


def format_datetime(datetime):
    date = {}
    date["day"] = datetime.strftime("%d")
    date["month"] = datetime.strftime("%b")
    date["year"] = datetime.strftime("%Y")
    date["hour"] = datetime.strftime("%I")
    date["minute"] = datetime.strftime("%M")
    date["second"] = datetime.strftime("%S")
    date["AM-PM"] = "a.m." if datetime.strftime("%p") == "AM" else "p.m."
    return date


def load_comments(request, id):
    post = get_object_or_404(Post, id=int(id))
    parents = []
    children = {}
    comments = []
    query_comments = post.comments.all().order_by("created_at").values()

    for comment in query_comments:
        if comment["hidden"]:
            continue
        comment["created_at"] = format_datetime(comment["created_at"])
        comments.append(comment)

    for comment in comments:
        if comment["group"] == "0":
            parents.append(comment)
        else:
            if comment["group"] in children.keys():
                children[comment["group"]].append(comment)
            else:
                children[comment["group"]] = [comment]

    for parent in parents:
        group = str(parent["id"])
        if group in children.keys():
            parent["children"] = children[group]

    return HttpResponse(json.dumps(parents), content_type="application/json")


@login_required
@csrf_exempt
def post_comment(request):
    try:
        if request.method == "POST":
            print(request.body)
            received_json_data = json.loads(request.body)
            # category = received_json_data['category']
            author = received_json_data["author"]
            content = received_json_data["content"]
            post_id = received_json_data["post_id"]

            if "parent_id" in received_json_data:
                print("yes")
                parent_id = received_json_data["parent_id"]
                comment = Comment(
                    post_id=post_id, author=author, content=content, parent_id=parent_id
                )
            else:
                comment = Comment(
                    post_id=post_id, author=author, content=content)

            comment.save()

            post = get_object_or_404(Post, id=int(post_id))
            latest_comment = post.comments.all().order_by("created_at").values().last()
            latest_comment["created_at"] = format_datetime(
                latest_comment["created_at"])

            return HttpResponse(
                json.dumps(latest_comment), content_type="application/json"
            )
        return HttpResponseBadRequest("Bad Request", content_type="application/json")
    except TypeError:
        return HttpResponseBadRequest("Bad Request", content_type="application/json")
    except json.decoder.JSONDecodeError:
        return HttpResponseBadRequest("Bad Request", content_type="application/json")


def truncate(string, length):
    splitted_string = remove_html_tags(string).split()
    if len(splitted_string) > length:
        return " ".join(map(str, splitted_string[:length])) + "..."
    else:
        return string

def truncate_wo_html_rm(string, length):
    splitted_string = string.split()
    if len(splitted_string) > length:
        return " ".join(map(str, splitted_string[:length])) + "..."
    else:
        return string


def get_recent_posts(request, page=1):
    post = Post.objects.all().order_by("created_at").reverse()
    max_length = len(post)
    data = []
    for i in range(MAX_POST_HOME_PAGE):
        index = i + (page - 1) * MAX_POST_HOME_PAGE
        if index < max_length:
            data.append(
                {
                    # "id": json.loads(json.dumps(post[index]._id, default=json_util.default))["$oid"],
                    "id": post[index].id,
                    "category": post[index].category.name,
                    "title": truncate(post[index].title, 10),
                    "content": truncate(post[index].content, 30),
                    "date": post[index].created_at,
                    "number_comments": post[index].comments.count(),
                    "thumbnail": post[index].thumbnail,
                }
            )
        else:
            break

    if request.method == "POST":
        received_json_data = json.loads(request.body)
        ran = int(received_json_data["random"])
        except_id = int(received_json_data["except"])
        for i in range(len(data)):
            if data[i]["id"] == except_id:
                data.pop(i)
                break
        idx = sample(range(0, len(data)), ran)
        response = [data[i] for i in idx]
        for d in response:
            d["date"] = format_datetime(d["date"])
        return HttpResponse(json.dumps(response), content_type="application/json")

    else:
        return data, max_length


def get_post(request, id):
    # post = Post.objects.get(_id=ObjectId(id))
    post = get_object_or_404(Post, id=int(id))
    parents = []
    children = {}
    comments = post.comments.all().order_by("created_at").values()
    comments_count = len(comments)
    for comment in comments:
        if comment["group"] == "0":
            parents.append(comment)
        else:
            if comment["group"] in children.keys():
                children[comment["group"]].append(comment)
            else:
                children[comment["group"]] = [comment]

    for parent in parents:
        group = str(parent["id"])
        if group in children.keys():
            parent["children"] = children[group]

    data = {
        "id": post.id,
        "category": post.category,
        "title": post.title,
        "content": post.content,
        "comments": parents,
        "comments_count": comments_count,
        "date": post.created_at,
        "thumbnail": post.thumbnail,
    }
    return data


def modify_bottom_nav_bar(max_length, page, MAX):
    div = int(max_length / MAX) + 1
    mod = int(max_length % MAX)
    page_nav = 0

    if mod == 0:
        div -= 1

    if page < MAX_PAGE:
        if div > MAX_PAGE:
            page_nav = range(1, MAX_PAGE + 1)
        else:
            page_nav = range(1, div + 1)

    elif page >= MAX_PAGE:
        if page + 2 > div:
            page_nav = range(div - (MAX_PAGE - 1), div + 1)
        else:
            page_nav = range(page - int(MAX_PAGE / 2),
                             page + int(MAX_PAGE / 2) + 1)

    if div > MAX_PAGE:
        if page < 3:
            first = 0
        else:
            first = 1

        if page < div - 1:
            last = div
        else:
            last = 0  
    else:
        last = 0
        first = 0


    nav_bar = [first, page_nav, last]
    return nav_bar


def home(request, page=1):
    data, max_length = get_recent_posts(request, page=page)
    nav_bar = modify_bottom_nav_bar(max_length, page, MAX_POST_HOME_PAGE)
    context = {
        "data": data,
        "nav_bar": nav_bar,
        "page": page,
    }
    return render(request, "home.html", context)


def contact(request):
    return render(request, "contact.html")


def post(request, id):
    post_data = get_post(request, id)
    context = {"post": post_data}
    return render(request, "post.html", context)


def find_category(regex):
    categories = ["Technology", "Coding", "Inspiration"]
    for category in categories:
        if re.search(regex, category, re.IGNORECASE):
            return category


def category(request, cat, page=1):
    cat = find_category(cat)
    post = Category.objects.get(name=cat).posts.all()
    max_length = len(post)
    data = []
    for i in range(MAX_POST_CATEGORY_PAGE):
        index = i + (page - 1) * MAX_POST_CATEGORY_PAGE
        if index < max_length:
            if len(post[index].title) > 40:
                post[index].title = post[index].title[:27] + "..."
            data.append(
                {
                    # "id": json.loads(json.dumps(post[index]._id, default=json_util.default))["$oid"],
                    "id": post[index].id,
                    "category": post[index].category,
                    "title": truncate(post[index].title, 10),
                    "content": truncate(post[index].content, 30),
                    "date": format_datetime(post[index].created_at),
                    "thumbnail": post[index].thumbnail,
                }
            )
        else:
            break

    nav_bar = modify_bottom_nav_bar(max_length, page, MAX_POST_CATEGORY_PAGE)

    context = {"data": data, "nav_bar": nav_bar, "page": page, "nav_tab": cat}
    return render(request, "category.html", context)


def search_in_mongo(request, raw_keywords):
    client = pymongo.MongoClient(
        'mongodb+srv://admin:admindb123@cluster0.ospfa.mongodb.net/blog_data?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["blog_data"]
    collection = db["blog_post"]
    collection.create_index([("title", "text"), ("content", "text")])
    keywords = []
    result_id = []
    result = []

    # for raw_keyword in list_keywords:
    #     search_result = collection.find({"$text": {"$search": raw_keyword}})
    #     keyword = collection.find({"$text": {"$search": raw_keyword}}).explain()[
    #         "queryPlanner"
    #     ]["winningPlan"]["parsedTextQuery"]["terms"]
    #     if keyword:
    #         keywords = keyword.copy()
    #     for item in search_result:
    #         if item not in result_id:
    #             result_id.append(item["id"])
    #             result.append(get_post(request, item["id"]))

    search_result = collection.find({"$text": {"$search": raw_keywords}})
    keywords = collection.find({"$text": {"$search": raw_keywords}}).explain()[
        "queryPlanner"
    ]["winningPlan"]["parsedTextQuery"]["terms"]
    for item in search_result:
        result.append(item)

    return keywords, result


def load_dictionary():
    f = open("blog\\static\\dictionary.txt", "r")
    temp = f.read()
    temp = temp.replace("'", '"')
    temp = temp[temp.find("{"): -1]
    dictionary = json.loads(temp)
    f.close()
    return dictionary


def add_css_highlight_background(regex, item):
    matches = re.finditer(regex, item, re.MULTILINE | re.IGNORECASE)
    result = []
    for matchNum, match in enumerate(matches, start=1):
        result = item[0: match.start(
        )] + fr"<span style=background-color:yellow>{item[match.start(): match.end()]}</span>" + item[match.end():]

    return result


def search(request, page=1):
    raw_request = unquote(str(request))
    raw_keywords = raw_request[raw_request.find(
        "keyword") + 8: -2].replace("+", " ")
    print(raw_keywords)
    keywords, search_result = search_in_mongo(request, raw_keywords)
    print(keywords)
    dictionary = load_dictionary()
    new_format = add_css_highlight_background
    data = []
    index = 0
    remove_index = []
    for item in search_result:
        index += 1
        flag = 0
        item["title"] = remove_html_tags(item["title"])
        item["content"] = remove_html_tags(item["content"])
        for keyword in keywords:
            if keyword in dictionary:
                for value in dictionary[keyword]:
                    print(value)
                    temp = new_format(value, item["title"])
                    if temp:
                        item["title"]= temp
                        flag += 1

                    temp = new_format(value, item["content"])
                    if temp:
                        item["content"]= temp
                        flag += 1
            else:
                temp = new_format(keyword, item["title"])
                if temp:
                    item["title"]= temp
                    flag += 1
                temp = new_format(keyword, item["content"])
                if temp:
                    item["title"]= temp
                    flag += 1
        
        if flag == 0:
            remove_index.append(index)

    remove_index.sort(reverse= True)
    for i in remove_index:
        search_result.pop(i-1)
    max_length=len(search_result)

    nav_bar=modify_bottom_nav_bar(max_length, page, MAX_SEARCH_RESULT)

    for i in range(MAX_SEARCH_RESULT):
        index=i + (page - 1) * MAX_POST_HOME_PAGE
        if index < max_length:
            data.append(
                {
                    "id": search_result[index]["id"],
                    "category": Category.objects.get(id=int(search_result[index]["category_id"])),
                    "title": search_result[index]["title"],
                    "content": truncate_for_search_highlight(search_result[index]["content"], 10),
                    "date": search_result[index]["created_at"],
                }
            )
        else:
            break

    if not search_result:
        context={"not_found": True, "keyword": raw_keywords}
    else:
        context={
            "data": data,
            "nav_bar": nav_bar,
            "page": page,
            "keyword": raw_keywords,
        }

    return render(request, "search.html", context)


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean=re.compile('<.*?>')
    return re.sub(clean, '', text)

def truncate_for_search_highlight(string, length):
    regex = "<span style=background-color:yellow>.*?</span>"
    result = ""
    matches = re.finditer(regex, string, re.MULTILINE | re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=1):
        splitted_string = string[0:match.start()].split()
        if len(splitted_string) > length:
            result = result + " ... " + " ".join(map(str, splitted_string[-length:])) + " " + string[match.start():match.end()]
        else:
            result = result + string[0: match.end()]

        splitted_string = string[match.end():].split()
        if len(splitted_string) > length:
            result = result + " " + " ".join(map(str, splitted_string[:length])) + " ... "
        else:
            result = result + string[match.end():]

    return result
    
