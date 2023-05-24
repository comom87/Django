from django.db import models
from django.urls import reverse

# Create your models here.
class Bookmark(models.Model):
    site_name = models.CharField(max_length=100)
    url = models.URLField('Site URL')

    # 매직 메서드 or 던더 메서드: 클래스 내부에 있는 메서드 중에서 _가 앞 뒤로 두 개씩 붙어있는 함수로 특별한 기능들이 존재
    # __str__ 메서드: 클래스의 객체를 출력할 때 나타날 내용을 결정하는 메서드, 항상 문자열을 반환해야 함
    def __str__(self):
        return "이름: " + self.site_name + ", 주소: " + self.url
    
    # get_absolute_url: 보통은 객체의 상세 화면 주소를 반환
    # reverse 메서드: URL 패턴의 이름과 추가 인자를 전달받아 URL을 생성하는 메서드
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])