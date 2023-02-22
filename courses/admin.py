from django.contrib import admin
from .models import Course, Category, Lesson, Section


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class SectionAdmin(admin.ModelAdmin):
    inlines = [
        LessonInline,
    ]

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Section, SectionAdmin)