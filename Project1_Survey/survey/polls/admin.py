from django.contrib import admin
from polls.models import Question, Choice

# Register your models here.

# class ChoiceInline(admin.StackedInline):   # Question 및 Choice 한 화면에서 변경하기
class ChoiceInline(admin.TabularInline):   # 테이블 형식으로 보여주기
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']   # 필드 순서 변경
    fieldsets = [   # 각 필드를 분리해서 보여주기
        ('Question Statement', {'fields': ['question_text']}),
        # ('Date Information', {'fields': ['pub_date']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),   # 필드 접기
    ]
    inlines = [ChoiceInline]   # Choice 모델 클래스 같이 보기
    list_display = ('question_text', 'pub_date')   # 레코드 리스트 컬럼 지정하기
    list_filter = ['pub_date']   # list_filter 필터
    search_fields = ['question_text'] # search_fields

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)