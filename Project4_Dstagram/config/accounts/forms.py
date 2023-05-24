from django.contrib.auth.models import User
from django import forms

# RegisterForm 클래스를 통해 회원 가입 양식을 출력
# forms.ModelForm: 모델이 있고 그에 대한 자료를 입력받고 싶을 때 사용
class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput) # password의 경우에는 fields에 설정할 수 있지만 종류가 CharField이기 때문에 별도의 widget 옵션을 사용해 password 속성의 input 태그를 사용하려고 클래스 변수로 지정
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta: # Meta 클래스를 이용하면 기존에 있는 모델의 입력 폼을 쉽게 만들 수 있음.
        model = User
        fields = ['username', 'first_name', 'last_name', 'email'] # fields: 입력받을 필드들을 지정
    
    # clean_password2: clean_필드명 형태의 메서드
    #                  이런 형태의 메서드들은 각 필드의 clean 메서드가 호출된 후에 호출되는 메서드들
    #                  특별한 유효성 검사나 조작을 하고 싶을 때 만들어서 
    #                  clean_필드명 형태의 메서드에서 해당 필드의 값을 사용할 때는 꼭 cleaned_data에서 필드 값을 찾아서 사용해야 함
    #                  cleaned_data는 이전 단계까지 기본 유효성 검사같은 처리를 마친 값
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords not matched!')
        return cd['password2']