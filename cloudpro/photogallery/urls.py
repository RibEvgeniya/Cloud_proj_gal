from django.urls import path
from .views import gallery, create_folder, upload_photo,folder_detail,photo_detail,photo_delete,folder_delete,upload_photo1



urlpatterns = [
    path('gallery/', gallery, name='gallery'),
    path('cr_f/', create_folder, name='create_folder'),
    path('up_ph/', upload_photo, name='upload_photo'),
    path('upload_st/', upload_photo1, name='upload_photo_st'),
    path('folder/<int:pk>/', folder_detail, name='folder_detail'),
    path('photo/<int:pk>/', photo_detail, name='photo_detail'),
    path('photo/delete/<int:pk>/', photo_delete, name='photo_delete'),
    path('folder/delete/<int:pk>/', folder_delete, name='folder_delete'),
]