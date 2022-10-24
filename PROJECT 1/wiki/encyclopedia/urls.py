from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.detail,name="detail"),
    path("find/",views.find,name="find"),
    path("new/",views.new_page,name="new_page"),
    path("edit/",views.edit,name="edit"),
    path("save_edit/",views.save_edit,name="save_edit"),
    path("randomm/",views.randomm,name="randomm")
]
