from django.conf import settings
from django.urls import path

from .views import upload_media, about_page, handle_upload, handle_label_page, label_image, save_label_data

urlpatterns = [
    path('home/', upload_media, name="upload-page"),
    path('about/', about_page, name="about-page"),
    path('webMedia/', handle_upload, name="post-media"),
    path('label/', handle_label_page, name="label-page"),
    path('label/<int:pk>/', label_image, name="label-detail-page"),
    path('label/<int:pk>/media/', save_label_data, name="save-label-data")
]
