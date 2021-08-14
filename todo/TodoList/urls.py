from django.urls import path
from .views import create, deleteItem, deleteList, detail, index, updateItem

app_name = 'TodoList'
urlpatterns = [
    path('', index, name = 'index'),
    path('create/', create, name = 'create_list'),
    path('<int:list_id>', detail, name = 'detail'),
    path('<int:list_id>/delete', deleteList, name = 'delete_list'),
    path('<int:list_id>/<int:item_id>/delete', deleteItem, name = 'delete_item'),
    path('<int:list_id>/<int:item_id>/update', updateItem, name = 'update_item'),
]