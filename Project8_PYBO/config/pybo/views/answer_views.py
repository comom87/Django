from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import HttpResponse
from ..models import Question, Answer, Comment
from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# @login_required 애너테이션을 통해 로그인이 되었는지를 우선 검사하여 오류를 방지한다.
# 만약 로그아웃 상태에서 @login_required 애너테이션이 적용된 함수가 호출되면 자동으로 로그인 화면으로 이동할 것이다.
# @login_required 애너테이션의 login_url은 이동해야 할 로그인 화면의 URL을 의미한다.
@login_required(login_url='common:login')
def answer_create(request, question_id): # request: pybo/question_detail.html에서 textarea에 입력된 데이터가 파이썬 객체에 담겨 넘어온다.
    question = get_object_or_404(Question, pk=question_id)
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now()) # request.POST.get('content'): POST 형식으로 전송된 form 데이터 항목 중 name이 content인 값
    # return redirect('pybo:detail', question_id=question.id) # redirect 함수: 함수에 전달된 값을 참고하여 페이지 이동을 수행. 첫 번째 인수에는 이동할 페이지의 별칭을, 두 번째 인수에는 해당 URL에 전달해야 하는 값을 입력

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # request.user가 바로 현재 로그인한 계정의 User 모델 객체
            answer.question = question
            answer.create_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id)) # resolve_url 함수: 실제 호출되는 URL을 문자열로 반환하는 장고 함수
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'pybo/answer_form.html', {'answer': answer, 'form': form})

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)