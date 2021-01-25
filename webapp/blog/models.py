from djongo import models
# from autoslug import AutoSlugField
from django.utils.text import slugify
from django.contrib.auth import get_user_model


# Create your models here.

# class Post(models.Model):
#     _id = models.ObjectIdField()
#     # id = models.AutoField()
#     # category = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     content = models.JSONField()
#     comment = models.JSONField()
#     date = models.DateTimeField(auto_now_add=True)
#     # tag = models.JSONField()
#     # author_details = models.JSONField()
#     objects = models.DjongoManager()
#
#     def __str__(self):
#         return f"{self.title}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    objects = models.DjongoManager()

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    # title_vn = models.CharField(max_length=255)
    content = models.TextField()
    # content_vn = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    thumbnail = models.TextField(null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', default=1)
    author_username = models.CharField(max_length=100, default="admin")
    # publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    objects = models.DjongoManager()

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='children', null=True)
    reply_to = models.CharField(max_length=100, editable=False)
    author_username = models.CharField(max_length=100, default="admin")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', default=1)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)

    level = models.SlugField(
        default='0',
        editable=False,
    )
    def save(self, *args, **kwargs):
        if self.parent:
            value = int(self.parent.level) + 1
        else:
            value = 0
        self.level = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Post:{self.post}/Author:{self.author}'