# Django Backend for _Adventure Shop_

This project exists to showcase my “incredible” backend skills… or lack thereof. Judge responsibly.

## Hear Me Out

Of course, I had the help of my bro _**ChatGPT**_.  
This was my first time creating a project with Django, and let’s be honest—it’s pretty big for a first project.  
I also needed to use _**DRF**_, which really helped me understand some pretty tricky concepts, like:

- What **Serializers**, **Models**, **Views**, and **URLs** are
- How to configure **settings.py**
- What a **.env** file does
- How to publish code to GitHub without exposing sensitive keys

So yeah… shoutout to ChatGPT for always supporting me and preventing me from crying when I hit a bug at 3AM. 😅

## What This README Covers

I’ll walk you through every feature so you understand why I implemented it. Or why it’s a mess.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Serializers](#serializers)
- [Views](#views)
- [Models](#models)

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-4.3-green)

⚠️ **Still under development! Don’t pick on me!**

## Serializers

Alright, now we get to the scary stuff.  
Here’s where DRF really shows its magic, or makes you question your life .  
Below are the main serializers I created for Adventure Shop, with a _***short***_ explanation of why they exist:

1. [UserRegisterSerializer](#1-userregisterserializer)
2. [UserLoginSerializer](#2-userloginserializer)

### what are serializers?

#### it creates a response so that the frontend can use like json!

### 1. UserRegisterSerializer

As the name suggests, this serializer **registers users**.  
In the request data, it looks for unique **email** and **username**:

```python
email = serializers.CharField(
    validators=[UniqueValidator(queryset=MyUser.objects.all(), message="Email already exists")]
)

username = serializers.CharField(
    validators=[UniqueValidator(queryset=MyUser.objects.all(), message="Username already exists")]
)
```

Then we have our `Meta` class. Using my custom `MyUser` model, which extends Django's `AbstractUser`,  
we create an instance of the model user and expose only the **required fields** to the serializer.

```python
class Meta:
    model = MyUser
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password'
    ]
    extra_kwargs = {'password': {'write_only': True}}
```

the **create** function gets the **validated_data** from Serializer and executes automaticly wich results in creating the user with hashed password and returns the users data

```python
def create(self, validated_data):

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
```

this line:

```python
profilePic=random.randint(0,11)
```

picks a random rumber between 1,11.
why?  
cause in my react frontend I wanted users to have **randomized** profile pictures.  
so i downloaded 11 pictures and renamed then to 1.png, 2.pn etc...  
so now everyone has randomized profile pictures and its saved so its not going to refresh after logout or refreshing the page! XD  
_We get to **is_active = False** Later in **VerifyEmailView**!_

### 2. UserLoginSerializer
