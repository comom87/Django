from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Question, Answer, Comment
from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST) # 화면에서 전달받은 데이터로 폼의 값이 채워지도록 객체를 생성
        if form.is_valid(): # form.is_valid 함수: POST 요청으로 받은 form이 유효한지 검사. form이 유효하지 않다면 form에 오류가 저장되어 화면에 전달.
            question = form.save(commit=False) # form으로 Question 모델 데이터를 저장하기 위한 코드. commit=False는 임시 저장. 즉, 실제 데이터는 아직 저장되지 않은 상태.
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form} # 템플릿에서 폼 엘리먼트를 생성할 때 사용
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 로그인한 사용자와 수정하려는 글쓴이가 다르면
        messages.error(request, '수정권한이 없습니다.') # '수정권한이 없습니다'라는 오류가 발생
        return redirect('pybo:detail', question_id=question.id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question) # 조회한 질문 question을 기본값으로 하여 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성하라는
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question) # instance 매개변수에 question을 지정하면 기존 값을 폼에 채울 수 있다. 그러면 사용자는 질문 수정 화면이 나타날 때 기존에 저장되어 있던 제목, 내용이 반영된 상태에서 수정을 시작할 수 있다.
    return render(request, 'pybo/question_form.html', {'form': form})

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')