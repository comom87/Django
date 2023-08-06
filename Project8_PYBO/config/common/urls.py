from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'common'
urlpatterns = [
    # LoginView는 registration이라는 템플릿 디렉터리에서 login.html 파일을 찾는다.
    # 이 파일을 찾지 못해 오류가 발생한다면 registration/login.html 템플릿 파일을 작성해야 한다.
    # 로그인은 common 앱에 구현할 것이므로 오류 메시지에 표시한 것처럼 registration 디렉터리에 템플릿 파일을 생성하기보다는 common 디렉터리에 템플릿을 생성하는 것이 좋다.
    # as_view 함수에 template_name으로 'common/login.html'을 설정하면 registration 디렉터리가 아닌 common 디렉터리에서 login.html 파일을 참조한다.
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]