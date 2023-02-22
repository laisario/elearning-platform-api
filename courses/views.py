from rest_framework import viewsets, permissions, response, filters
from rest_framework.decorators import action
from .models import Course, Category, Lesson, Section, WatchedLesson, PurchasedCourse
from .serializers import CourseSerializer, CategorySerializer, LessonSerializer, SectionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'summary']
    ordering = ['created_at', 'price']

    def get_queryset(self):
        queryset = Course.objects.all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category__name=category)
        return queryset

    @action(detail=True, methods=["GET"], serializer_class=SectionSerializer)
    def sections(self, request, pk=None):
        return response.Response(Section.objects.filter(course__id=pk))

    @action(detail=True, methods=["POST"])
    def purchase(self, request, pk=None):
        if int(pk) in request.user.purchased_courses.values_list('course', flat=True):
            return response.Response({"success": False, "error": "Already purchased"})
        PurchasedCourse.objects.create(course=self.get_object(), user=request.user)
        return response.Response({"success": True})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["POST"])
    def watch(self, request, pk=None):
        WatchedLesson.objects.create(lesson=self.get_object(), user=request.user)
        return response.Response({"created": True})


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["GET"], serializer_class=LessonSerializer)
    def lessons(self, request, pk=None):
        return response.Response(Lesson.objects.filter(section__id=pk))
