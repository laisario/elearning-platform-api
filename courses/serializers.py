from rest_framework import serializers
from .models import Course, Category, Section, Lesson, PurchasedCourse
from reviews.serializers import ReviewSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    next = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()

    def get_next(self, obj):
        lessons = Lesson.objects.filter(section__course=obj.section.course, order__gt=obj.order).exclude(id=obj.id)
        return {"id": lessons.first().id, "name": lessons.first().name} if lessons.first() else None
    
    def get_prev(self, obj):
        lessons = Lesson.objects.filter(section__course=obj.section.course, order__lt=obj.order).exclude(id=obj.id)
        return {"id": lessons.last().id, "name": lessons.last().name} if lessons.last() else None
    
    class Meta:
        model = Lesson
        exclude = ['section']


class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    class Meta:
        model = Section
        exclude = ['course']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sections = SectionSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    lessons_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        count = 0
        for section in obj.sections.all():
            count += section.lessons.count()
        return count

    def get_students_count(self, obj):
        return PurchasedCourse.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = '__all__'


class SimplifiedCourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Course
        fields = '__all__'
