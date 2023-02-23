from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from courses.serializers import SimplifiedCourseSerializer
from courses.models import PurchasedCourse, WatchedLesson


class PurchasedCourseSerializer(serializers.ModelSerializer):
    course = SimplifiedCourseSerializer()

    class Meta:
        model = PurchasedCourse
        exclude = ['user']


class WatchedLessonSerializer(serializers.ModelSerializer):
    lesson = serializers.SerializerMethodField()

    def get_lesson(self, obj):
        return obj.lesson.id

    class Meta:
        model = WatchedLesson
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    purchased_courses = PurchasedCourseSerializer(many=True)
    watched_lessons = WatchedLessonSerializer(many=True)

    class Meta:
        model = User
        exclude = ['password']


class TokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainSerializer, cls).get_token(user)
        avatar = getattr(user, "avatar")
        avatar = getattr(avatar, "url")

        # Add custom claims
        token['email'] = user.email
        token['firstName'] = user.first_name
        token['lastName'] = user.last_name
        token['isStaff'] = user.is_staff
        token['avatar'] = avatar
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
