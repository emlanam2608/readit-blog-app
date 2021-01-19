from django.urls import path
from blog import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('home/page=<int:page>', views.home, name="home"),
    path('category/<str:cat>', views.category, name="category"),
    path('contact/', views.contact, name="contact"),
    path('post/<str:id>', views.post, name="post"),
    path('search', views.search, name="search"),
    path('search/page=<int:page>', views.search, name="search"),
    path('post_comment', views.post_comment, name="post_comment"),
    path('load_comments/post=<int:id>', views.load_comments, name="load_comments"),
    path('get_recent_posts', views.get_recent_posts, name="get_recent_posts"),
    # path('accounts/signup/', views.signup, name="signup"),
    # path('accounts/login/', views.login_user, name="login"),
    # path('logout/', views.logout_user, name="logout"),
    path('admin/', views.admin, name="admin"),
    path('admin/post/create/', views.create_post, name="create_post"),
    path('admin/post/update/<str:id>', views.update_post, name="update_post"),
]
