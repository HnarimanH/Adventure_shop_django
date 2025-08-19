# Django Backend for _Adventure Shop_

This project exists to showcase my “incredible” backend skills… or lack thereof. Judge responsibly.

## Hear Me Out

Of course, I had the help of my bro _**ChatGPT**_.  
This was my first time creating a project with Django, and let’s be honest, it’s pretty big for a first project.  
I also needed to use _**DRF**_, which really helped me understand some pretty tricky concepts, like:

- What **Serializers**, **Models**, **Views**, and **URLs** are
- How to configure **settings.py**
- What a **.env** file does
- How to publish code to GitHub without exposing sensitive keys

So yeah… shoutout to ChatGPT for always supporting me and preventing me from crying when I hit a bug at 3AM.

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
3. [UserForgotPasswordSerializer](#3-userforgotpasswordserializer)
4. [CartSerializer](#4-cartserializer)
5. [ProductSerializer](#5-productserializer)

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

Like the name screams, this one handles logging users in.
It validates the incoming data (email + password), and checks if the user exists if the password matches.
If anything is off it spits back: "Invalid username or password".
</br>

```python
def validate(self, data):

        try:
            userObj = MyUser.objects.get(email=data.get('email')).username
        except MyUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")
        user = authenticate(
            username= userObj,
            password= data.get('password')
        )

```

_**Note**:_ **(Djangos built in auth system needs username to login, you cant login with email, so i took the email and found the username assosiated with it and loged the user in, this way in the future i can login with both the username and password if i change the code a little, but it works for now!)**
</br>
</br>
</br>
</br>

in this line:

```python
if not user.is_active:
            return serializers.ValidationError("Please verify your email before logging in.")
```

**user.isActive** checks if the user is active, why?  
because when a user registers they need to verify their email.  
so their is active is set to **True** only after they verify their email  
if not verifyed but registered: spit out _**(Please verify your email before logging in)**_

### 3. UserForgotPasswordSerializer

this serializer expects 2 fields **email** and **password**  
it validates the data by creating an instance of the user by email from the model  
 if it does not exists it raises a **ValidationError (email not registered)**

```python
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:

            user = MyUser.objects.get(email=data.get('email'))
        except MyUser.DoesNotExist:
            raise serializers.ValidationError("Email not registered")


```

then it generates a **ResetPasswordToken**  
and it encodes the id of the user in a **url** safe format

```python
    token = PasswordResetTokenGenerator().make_token(user)


    uid = urlsafe_base64_encode(force_bytes(user.pk))

```

and returns the data (uid, token, user) back to the view

### 4. CartSerializer

here is the most horrifying thing i had to endore in this project _**The Cart Logic!**_  
first I use the SerializerMethodField, the best explanation i could find was **(it calls a method to figure out what values to return)**

```python
    cart_items = serializers.SerializerMethodField()
```

then we have the **Meta Class** it gets the values **(only the cart_items)** inside the MyUser model

```python
class Meta:
    model = MyUser
    fields = ['cart_items']
```

the function **get_cart_items** gets the user(obj) and looks for cart_entries in **MyUserProduct** models and then returns the filtered carts

```python
def get_cart_items(self, obj):
        cart_entries = MyUserProduct.objects.filter(user=obj)

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
```

### 5. ProductSerializer

its pretty straight forward  
it just serializes all the products in the Product

```python

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


```

### 6. CreateProductSerializer

he name should be self explaintory  
it expects for 2 fields to be like below;  
_**price: Has 10 max digits and a maximum of 2 decimal places**_  
_**name: Uniqe**_

```python
price = serializers.DecimalField(max_digits=10, decimal_places=2)
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Product.objects.all(), message="a product by this name exists!")]
    )
```

and then the create function gets executed automaticly after the data is validated by the meta class

```python
class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image_url', 'updated_by']
        read_only_fields = ['updated_by']

    def create(self, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data)
```

_**Note**_: this line

```python
validated_data['updated_by'] = self.context['request'].user
```

it basicly goes like:  
I dont trust frontend to send the currect user for updated_by field! let me do my own research
