from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import TodoList, ListItem

# Create your views here.

def index(request):
    todolists = TodoList.objects.all()

    context = {
        'todolists': todolists,
    }
    return render(request, 'TodoList/index.html', context)

def detail(request, list_id):
    if request.method == 'POST':
        newItem = request.POST['addItem']
        dueDate = request.POST['duedate']

        todoList = get_object_or_404(TodoList, id = list_id)
        ListItem.objects.create(desc = newItem, due_date = dueDate, parent_list = todoList)
        itemList = ListItem.objects.filter(parent_list = todoList)

        context = {
            'todoList' : todoList,
            'itemList' : itemList,
        }
        return HttpResponseRedirect(reverse('TodoList:detail', args=(list_id,)))

    else:
        todoList = get_object_or_404(TodoList, id = list_id)
        itemList = ListItem.objects.filter(parent_list = todoList)

        context = {
            'todoList' : todoList,
            'itemList' : itemList,
        }
        return render(request, 'TodoList/detail.html', context)

def create(request):
    if request.method == 'POST':
        name = request.POST['name']
        newList = TodoList.objects.create(list_name = name)
        allLists = TodoList.objects.all()
        context = {
            'todolists' : allLists,
        }
        return HttpResponseRedirect(reverse('TodoList:detail', args=(newList.id,)))
    else:
        return render(request, 'TodoList/create.html')

def deleteList(request, list_id):
    if request.method == "POST":
        list = get_object_or_404(TodoList, id = list_id)
        list.delete()
        return HttpResponseRedirect(reverse('TodoList:index'))
    return HttpResponseRedirect(reverse('TodoList:index'))
    

def updateItem(request, list_id, item_id):
    if request.method == "POST":
        todoList = get_object_or_404(TodoList, id = list_id)
        item = ListItem.objects.filter(parent_list = todoList, id = item_id)

        newItem = request.POST['updatedItem']
        newDate = request.POST['duedate']
        buff = request.POST.get('isDone', False)
        check = False
        if buff == "on":
            check = True
        item.update(desc = newItem, due_date = newDate, isDone = check)
        return HttpResponseRedirect(reverse('TodoList:detail', args=(list_id,)))

    else:
        todoList = get_object_or_404(TodoList, id = list_id)
        item = ListItem.objects.filter(parent_list = todoList, id = item_id)[0]

        context = {
            'todoList' : todoList,
            'item' : item,
        }
        return render(request, 'TodoList/update.html', context)

def deleteItem(request, list_id, item_id):
    if request.method == "POST":
        todoList = get_object_or_404(TodoList, id = list_id)
        to_del = ListItem.objects.filter(parent_list = todoList, id = item_id)
        to_del.delete()
        return HttpResponseRedirect(reverse('TodoList:detail', args=(list_id,)))
        
    return HttpResponseRedirect(reverse('TodoList:detail', args=(list_id,)))