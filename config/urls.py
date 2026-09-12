from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts import views as account_views
from explainer import views as explainer_views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", explainer_views.landing, name="home"),
    path("explainer/", include("explainer.urls")),

    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="explainer/login.html"
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "account/delete/",
        account_views.delete_account,
        name="delete_account",
    ),
    path("signup/", account_views.signup, name="signup"),
]
