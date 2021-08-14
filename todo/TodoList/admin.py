from django.contrib import admin
"""
For admin:
Username : vishwa
Email : admin@admin.com
Password : newAdmin

"""
from .models import TodoList
from .models import ListItem

# Register your models here.

admin.site.register(TodoList)
admin.site.register(ListItem)