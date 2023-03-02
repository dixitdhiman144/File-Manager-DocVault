from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="user_panel" ),
    path('login', views.login, name="login"),
    path('try-admin', views.admin_panel, name="admin_panel"),
    path('upload_file', views.upload, name="upload_file"),
    path('open_file', views.open_file, name="open_file"),
    path('download_file', views.download_file, name="download_file"),
]
