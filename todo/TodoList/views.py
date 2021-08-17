from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import TodoList, ListItem

# Create your views here.

def index(request):
    """
    Shows list of all todo lists
    """
    todolists = TodoList.objects.all()

    context = {
        'todolists': todolists,
    }
    return render(request, 'TodoList/index.html', context)

def detail(request, list_id):
    """
    Detailed view of a list, a form to add more items to list.
    Also, with each list option to edit the list item and delete it is present this is handled by the post request
    """
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
    """
    Handles simple form to create a new list
    """
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
    """
    Deletes a list with a form by taking the list_id
    """
    if request.method == "POST":
        list = get_object_or_404(TodoList, id = list_id)
        list.delete()
        return HttpResponseRedirect(reverse('TodoList:index'))
    else:
        list = get_object_or_404(TodoList, id = list_id)
        return HttpResponseRedirect(reverse('TodoList:index'))
    

def updateItem(request, list_id, item_id):
    """
    Handles form which updates todo item
    """
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
        item = get_object_or_404(ListItem, id = item_id)

        context = {
            'todoList' : todoList,
            'item' : item,
        }
        return render(request, 'TodoList/update.html', context)

def deleteItem(request, list_id, item_id):
    """
    Deletes list item by finding it from list_id
    """
    if request.method == "POST":
        todoList = get_object_or_404(TodoList, id = list_id)
        to_del = get_object_or_404(ListItem, id = item_id)
        to_del.delete()
        return HttpResponseRedirect(reverse('TodoList:detail', args=(list_id,)))
        
    else:
        todoList = get_object_or_404(TodoList, id = list_id)
        to_del = get_object_or_404(ListItem, id = item_id)
        return HttpResponse(reverse('TodoList:detail', args=(list_id,)))