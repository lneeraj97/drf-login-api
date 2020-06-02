# Django Notes

## Initial Steps


1. Starting a project

    `django-admin startproject [project name]`

2. Starting an app

    `django-admin startapp [app name]`

3. Adding an app to the project
    
    - Go to the project's `settings.py`
    - Add the app to the list of `INSTALLED_APPS`
    - Add the apps's `urls.py` to the urlpatterns list in the project's `urls.py`

        ```python 
        path('[pattern]',include([app name].urls))
        ```
    - Import the app's `views.py` into its `urls.py`

4. Adding templates and static files
    - In the project's `settings.py`, add the templates folder path to the `DIRS` list in the list called `TEMPLATES`. You can add multiple paths
    - Put app specific templates and static files inside the app directory
    ```bash
        [app name]
        ├── admin.py
        ├── apps.py
        ├── __init__.py
        ├── static
        │   └── [app name]
        │       ├── image.jpg
        │       └── style.css
        ├── [app name]
        │   └── generator
        │       └── index.html
        ├── tests.py
        ├── urls.py
        └── views.py
    ```

5. Creating admin user - `python manage.py createsuperuser`

6. To register a model to appear in the admin website, register it in it's app's `admin.py` 
    
    ```python
    from .models import [your model] 
    admin.site.register([your model])
    ```

## Using a custom User model

1. Declare the model and model manager in `models.py`

    ```python
    from django.db import models
    from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


    class UserProfileManager(BaseUserManager):
        """ Custom Manager class for our UserProfile. Must implement create_user and create_superuser methods """

        def create_user(self, email, first_name, last_name=None, password=None):
            """ Creates a new user with the given deets """
            if not email:
                raise ValueError("Please provide an email address")
            if not first_name:
                raise ValueError("Please provide the first name")

            # Create the object. self.model is automatically assigned to the User Model
            user = self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, email, first_name, last_name=None, password=None):
            """ Creates and saves a superuser with the given deets """
            user = self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
            )
            user.is_staff = True
            user.save(using=self._db)
            return user


    class UserProfile(AbstractBaseUser, PermissionsMixin):
        """ A custom User model with email id as the way of authentication """
        # Define fields
        email = models.EmailField(unique=True)
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30, blank=True, null=True)
        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)

        # Define the custom model manager
        objects = UserProfileManager()

        # Specify which field to use as the username field
        USERNAME_FIELD = 'email'

        # Specify required fields
        REQUIRED_FIELDS = ['first_name', ]

        def __str__(self):
            """ String representation of our user model """
            return self.email

        def get_full_name(self):
            """ Get the full name of our user """
            return self.first_name + self.last_name
    ```

2. Set `AUTH_USER_MODEL='[app name].[model name]` in the project's settings.py

3. Register the model in the `admin.py` file
    ```python
    from django.contrib import admin
    from . import models

    admin.site.register(models.UserProfile)
    ```
4. Create a serializer in `serializers.py`


    ```python 
    from rest_framework import serializers
    from . import models


    class UserProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.UserProfile
            # Add id here
            fields = ['email', 'first_name', 'last_name', 'password']
            extra_kwargs = {
                'password': {
                    'write_only': True,
                    'style': {
                        'input_type': 'password',
                    }
                }
            }

        def create(self, validated_data):
            """ Overrides the default create function """
            user = models.UserProfile.objects.create_user(
                email=validated_data['email'],
                name=validated_data['name'],
                password=validated_data['password']
            )
            return user

        def update(self, instance, validated_data):
            """ Handles updating a user model """
            if 'password' in validated_data:
                password = validated_data.pop('password')
                instance.set_password(password)
            return super().update(instance, validated_data)        
    ```

5. Create a permission manager in `permissions.py`

    ```python
    from rest_framework import permissions

    class UpdateOwnProfile(permissions.BasePermission):
        """ Controls access to profiles """

        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True

            return obj.id == request.user.id
    ```

6. Create a view in `views.py`

    ```python
    class UserProfileViewSet(viewsets.ModelViewSet):
        """ Handles UserProfile views """
        authentication_classes = (TokenAuthentication,)
        serializer_class = serializers.UserProfileSerializer
        queryset = models.UserProfile.objects.all()
        permission_classes = (permissions.UpdateOwnProfile,)
    ```

7. Register the view in `urls.py`kv
    ```python
    from django.urls import path, include
    from . import views
    from rest_framework.routers import DefaultRouter

    router = DefaultRouter()
    router.register('api', views.UserProfileViewSet)

    urlpatterns = [
        path('', include(router.urls)),
    ]
    ```