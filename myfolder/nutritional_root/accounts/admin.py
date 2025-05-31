from django.contrib import admin
from .models import Page
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display=['id_no','last','first','middle', 'age', 'birthday', 'weight', 'height', 'gender']

admin.site.register(Page)
admin.site.register(Student,StudentAdmin)

