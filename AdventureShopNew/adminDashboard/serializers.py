from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Product
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CreateProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Product.objects.all(), message="a product by this name exists!")]
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image_url', 'updated_by']
        read_only_fields = ['updated_by']

    def create(self, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data)