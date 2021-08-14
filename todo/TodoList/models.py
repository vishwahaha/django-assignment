from django.db import models

# Create your models here.

class TodoList(models.Model):

    list_name = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.list_name}"

class ListItem(models.Model):

    desc = models.CharField(max_length = 10000)
    isDone = models.BooleanField(default = False)
    due_date = models.DateTimeField()
    parent_list = models.ForeignKey(TodoList, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.parent_list.list_name} :: {self.desc}"