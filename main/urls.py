"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views as core_views
from courses import views as courses_views
from reviews import views as reviews_views

core_router = routers.DefaultRouter()
core_router.register(r'users', core_views.UserViewSet)
core_router.register(r'reviews', reviews_views.ReviewViewSet)
core_router.register(r'testimonials', reviews_views.TestimonialViewSet)

courses_router = routers.DefaultRouter()
courses_router.register(r'courses', courses_views.CourseViewSet, basename="courses")
courses_router.register(r'categories', courses_views.CategoryViewSet)
courses_router.register(r'lessons', courses_views.LessonViewSet)
courses_router.register(r'sections', courses_views.SectionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include(core_router.urls)),
    path("e-learning/", include(courses_router.urls)),
    path("login/", core_views.MyObtainTokenPairView.as_view(), name="login"),
    path("register/", core_views.RegisterView.as_view(), name="register"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
