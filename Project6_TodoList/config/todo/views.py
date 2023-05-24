from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Todo
from .forms import TodoForm
# Create your views here.
# todo_fetch(): 목록을 불러오는 역할
def todo_fetch(request):
    todos = Todo.objects.all() # 저장된 모든 할 일 데이터를 불러오 후에
    todo_list = []
    for index, todo in enumerate(todos, start=1): # 하나씩 json 데이터로 가공할 수 있게
        todo_list.append({'id':index, 'title':todo.title, 'completed':todo.completed}) # 사전형 데이터로 저장
    
    return JsonResponse(todo_list, safe=False)

# todo_save(): 할 일 목록 전체 데이터를 받아서 그대로 저장하는 역할
#              저장할 때마다 전체 데이터를 지우고 다시 입력하는 방식 사용
#              뷰를 호출할 때마다 데이터를 확인 없이 지우게 되면 문제가 생길 수 있으므로 전달된 데이터가 확실히 있을 때만 전체 데이터를 삭제
@csrf_exempt
@require_POST
def todo_save(request):
    if request.body:
        data = json.loads(request.body)
        if 'todos' in data:
            todos = data['todos']
            Todo.objects.all().delete()
            for todo in todos:
                print('todo', todo)
                form = TodoForm(todo)
                if form.is_valid():
                    form.save()
    
    return JsonResponse({})

def index(request):
    return render(request, 'todo/list.html')