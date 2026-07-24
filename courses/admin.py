from django.contrib import admin
from .models import Course, Note

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'updated_at')