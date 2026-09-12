from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="explainer"),
    path("history/", views.history, name="history"),
    path(
        "history/<int:pk>/",
        views.history_detail,
        name="history_detail",
    ),
    path(
        "history/<int:pk>/delete/",
        views.history_delete,
        name="history_delete",
    ),
    path(
        "history/clear/",
        views.history_clear,
        name="history_clear",
    ),
]
