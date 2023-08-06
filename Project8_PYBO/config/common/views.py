from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from common.forms import UserForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # form.cleaned_data.get 함수: 회원가입 회면에서 입력한 값을 얻기 위해 사용하는 함수
            raw_password = form.cleaned_data.get('password1')
            # 회원가입이 완료된 이후에 자동으로 로그인되도록 authenticate 함수와 login 함수를 사용
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})