from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


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


class UserStatus(models.Model):
    """ Handles the user status """
    user_profile = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ String representaion """
        return self.status_text
