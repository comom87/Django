from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Photo(models.Model):
    # author:photo=1:N
    # on_delete: 연결될 모델이 삭제될 경우 현재 모델의 값의 변경 방법
    # CASCADE: 연결된 객체가 지워지면 해당 하위 객체도 같이 삭제
    # related_name: 연결된 객체에서 하위 객체의 목록을 부를 때 사용할 이름
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photos')
    # upload_to: 사진이 업로드 될 경로를 설정, 만약 업로드가 되지 않을 경우 default 값으로 대체
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default='photos/no_image.png')
    # TextField: 문자열 길이 제한 X
    text = models.TextField()
    # auto_now_add: 객체가 추가될 때 자동으로 값을 설정
    created = models.DateTimeField(auto_now_add=True)
    # auto_now: 객체가 수정될 때마다 자동으로 값을 설정
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering: 해당 모델의 객체들을 어떤 기준으로 정렬할 것인지 설정
        ordering = ['-updated']
    
    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=[str(self.id)]) # reverse 메서드: URL 패턴 이름을 가지고 해당 패턴을 찾아 주소를 만들어주는 함수