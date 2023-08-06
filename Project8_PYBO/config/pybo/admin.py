# 장고 Admin에서는 현재 등록된 그룹 및 사용자에 대한 정보 확인과 수정을 할 수 있다.

from django.contrib import admin
from .models import Question

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject'] # 제목으로 질문을 검색할 수 있는 검색 항목

admin.site.register(Question, QuestionAdmin)