from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('api/demo/', views.DemoListCreate.as_view()),

    path('assets/<str:file>', views.assets),
    path('test/<int:test>', views.test),
    path('createStudent', views.createStudent),
    path('getStudents', views.getStudents),
    path('getStudentInfoByStudentID/<int:user_id>', views.getStudentInfoByStudentID),
    path('admin/', admin.site.urls),
    path('', views.index),
]