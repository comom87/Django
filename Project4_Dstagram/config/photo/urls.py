from django.urls import path
from django.views.generic import DetailView

from .views import *
from .models import Photo

 # app_name: 네임스페이스(namespace)로 사용되는 값
 #           템플릿에서 url 템플릿 태그를 사용할 때 app_name 값이 설정되어 있다면 [app_name:URL 패턴이름] 형태로 사용
app_name = 'photo'

urlpatterns = [
    path('', photo_list, name='photo_list'),
    path('detail/<int:pk>/', DetailView.as_view(model=Photo, template_name='photo/detail.html'), name='photo_detail'), # DetailView를 인라인 코드로 작성
    path('upload/', PhotoUploadView.as_view(), name='photo_upload'),
    path('delete/<int:pk>/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('update/<int:pk>/', PhotoUpdateView.as_view(), name='photo_update')
]