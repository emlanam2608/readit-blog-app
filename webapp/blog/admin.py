from django.contrib import admin
from blog.models import Post, Category, Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "created_at","hidden"]

    class Meta:
        ordering = ["title"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

    class Meta:
        ordering = ["name"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "content", "created_at"]

# @admin.RelatedFieldListFilter
# class HiddenPost(admin.ModelAdmin):
#     list_display = ('display_hidden_posts',)

#     def display_hidden_posts(self, obj):
#         post = obj.all().order_by('created_date')
#         if post.hidden:
#             return post
#         else:
#             return None
