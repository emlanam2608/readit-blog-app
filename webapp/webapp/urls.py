"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', views.home, name="home"),
    path('blog/', include('blog.urls')),
    path('accounts/signup/', views.signup, name="signup"),
    path('accounts/signin/', views.signin, name="signin"),
    path('accounts/signout/', views.signout, name="signout"),
    path('accounts/profile/', views.profile, name="profile"),
    path('accounts/password/change/', views.password_change, name="password_change"),
    path('accounts/user/', views.get_user_session, name="get_user_session"),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('accounts/password/reset/', auth_views.PasswordResetView.as_view(template_name = "password_reset_form.html", email_template_name = "password_reset_email.html", subject_template_name = "password_reset_subject.txt"), name ='password_reset'),
    path('accounts/password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_done.html"), name ='password_reset_done'),
    path('accounts/pasword/reset/comfirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_confirm.html"), name ='password_reset_confirm'),
    path('accounts/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_complete.html"), name ='password_reset_complete'),
    # prefix_default_language=True
)
