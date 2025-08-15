from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import random
from adminDashboard.serializers import ProductSerializer

from .models import MyUserProduct  

class UserRegisterSerializer(serializers.ModelSerializer):
    
        
    # validating the email and usenrame via UniqueValidator to check if the username or email exist.
    
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=MyUser.objects.all(), message="Email")]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=MyUser.objects.all(), message="Username")]
    )
    
    
    

    class Meta:
        
        # Using Django's built-in User model for registration
        model = MyUser
        
        
        # Limit serializer to only expose username and password fields
        fields = ['username', 'first_name', 'last_name', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
        

    def create(self, validated_data):
        
        # Creates and returns a new user with hashed password
        user =  MyUser.objects.create_user(
            
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profilePic=random.randint(0,11)
            
            
        )
        user.is_active = False
        user.save()
        return user
        
        
        
class UserLoginSerializer(serializers.Serializer):
    
    # Define expected fields for login input (email & password)
    email = serializers.CharField()
    password = serializers.CharField(write_only = True)
    
    
    
    
    
    
    
    
    def validate(self, data):
        

        
    
        
        try:
            userObj = MyUser.objects.get(email=data.get('email')).username
        except MyUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")
        # Authenticates user with provided credentials against the database
        user = authenticate(
            username= userObj,
            password= data.get('password')
        )
        
        
       # If authentication fails, raise a validation error
        # If successful, attach user object to validated data   
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            return serializers.ValidationError("Please verify your email before logging in.")

        data['user'] = MyUser.objects.get(username=user.username)
        return data
        
    
        


class UserForgotPasswprdSerializer(serializers.Serializer):
    
    # Define expected fields for reseting password (email & password)
    email = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        try:
            # checks if the user exists and creates an instance oof user
            user = MyUser.objects.get(email=data.get('email'))
        except MyUser.DoesNotExist:
            raise serializers.ValidationError("Email not registered")
        
        # genereates a token
        token = PasswordResetTokenGenerator().make_token(user)
        
        
        
        # Why do you care about user.pk?

        # Because when you generate tokens for email verification or password reset, 
        # you need to send a reference back to the backend so it knows which user to operate on.
        # The easiest way? Encode the primary key (pk) into a URL-safe format,
        # slap it in a link, and send it via email.
        
        # This encodes the user’s ID so it can be safely passed through URLs without breaking or exposing the raw ID directly.
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        
        data['uid'] = uid
        data['token'] = token
        data['user'] = user  

        return data
    
    
class CartSerializer(serializers.ModelSerializer):
    
    cart_items = serializers.SerializerMethodField()
    # serializers.SerializerMethodField is a special DRF (django rest framework) field that does not come from the model, 
    # instead it calls a method to figure out what values to return
    
    class Meta:
            model = MyUser        
            fields = ['cart_items']
    def get_cart_items(self, obj):
        cart_entries = MyUserProduct.objects.filter(user=obj)
        # obj is an instance of user
        result = []
        
        for item in cart_entries:
            result.append({
                "id": item.product.id,
                "name": item.product.name,
                "price": str(item.product.price), 
                "description": item.product.description,
                "image_url": item.product.image_url,
                "category": item.product.category,
                "updated_by": item.product.updated_by,
                "quantity": item.quantity,
            })
        return result
