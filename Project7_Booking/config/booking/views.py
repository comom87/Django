from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsOwnerOrReadOnly
# Create your views here.
class BookingList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,) # authentication_classes: 어떤 인증 방식으로 이용 가능한지 설정
    # permission_classes: 인증을 해야만 볼 수 있다는 옵션 설정
    #                     기존에는 토큰이 있는 사용자만 조회할 수 있었지만 거기에 더해 IsOwnerOrReadOnly를 더해서 소유자가 아닐 경우 수정은 불가능하도록 만듦
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer