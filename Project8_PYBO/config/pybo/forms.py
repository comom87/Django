from django import forms
from pybo.models import Question, Answer, Comment

# QuestionForm: 질문을 등록하기 위해 사용하는 장고의 폼
# ModelForm: 모델과 연결된 폼이며, 모델 폼 객체를 저장하면 연결된 모델의 데이터를 저장
#            내부 클래스로 Meta 클래스를 반드시 가져야 하며, Meta 클래스에는 모델 폼이 사용할 모델과 모델의 필드를 적어야 한다.
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        # }
        labels = {
            'subject': '제목',
            'content': '내용'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변 내용'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용'
        }