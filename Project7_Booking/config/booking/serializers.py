# Serializer는 요청한 모델의 API를 보여줄 때 사용하는 클래스. 보통 GET 방식으로 모델에 대한 데이터를 요청했을 때 Serializer를 활용해 데이터를 제공.

from .models import Booking
from rest_framework import serializers

class BookingSerializer(serializers.ModelSerializer): # ModelSerializer를 상속받아 만들면 간단하게 직렬화 가능
    class Meta:
        model = Booking
        fields = '__all__'