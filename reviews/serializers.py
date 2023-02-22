from rest_framework import serializers
from .models import Review, Testimonial
from core.models import User

class SimplifiedUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ['id', 'name', 'avatar']


class ReviewSerializer(serializers.ModelSerializer):
    user = SimplifiedUserSerializer()
    class Meta:
        model = Review
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'