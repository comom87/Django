from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    use_from = models.DateTimeField() # use_from: 쿠폰의 사용 기간
    use_to = models.DateTimeField() # use_to: 쿠폰의 사용 기간
    # amount: 할인 금액
    #         validators 인수로 MinValueValidator, MaxValueValidator를 추가해서 값을 0 ~ 100000 사이로만 설정할 수 있는 제약 조건
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    active = models.BooleanField()

    def __str__(self):
        return self.code