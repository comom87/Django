from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200) # CharField: 글자 수 제한이 있는 데이터
    content = models.TextField() # TextField: 글자 수 제한이 없는 데이터
    create_date = models.DateTimeField()
    # null=True: 데이터베이스에서 해당 칼럼에 null을 허용한다는 의미
    # blank=True: form.is_valid()를 통한 입력 폼 데이터 검사 시 값이 없어도 된다는 의미
    modify_date = models.DateTimeField(null=True, blank=False)
    voter = models.ManyToManyField(User, related_name='voter_question') # 같은 사용자가 하나의 질문을 여러 번 추천해도 추천 수가 증가하지는 않는다. ManyToManyField는 중복을 허락하지 않는다.

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # on_delete=models.CASCADE: 답변에 연결된 질문이 삭제되면 답변도 함께 삭제
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)