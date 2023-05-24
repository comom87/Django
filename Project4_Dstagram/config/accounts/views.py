from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST': # 회원 가입 정보가 서버로 전달됐다는 의미
        user_form = RegisterForm(request.POST) # RegisterForm을 이용해 유효성 검사 수행
        if user_form.is_valid():
            # user_form.save(): 폼 객체에 지정된 모델을 확인하고 이 모델의 객체를 만듦
            # commit=False: 데이터베이스에 저장 X, 메모리 상에 객체만 생성
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password']) # set_password(): 비밀번호를 암호화된 상태로 저장
            new_user.save() # 실제로 데이터베이스에 저장
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form':user_form})