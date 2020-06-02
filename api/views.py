from django.shortcuts import render
from rest_framework import filters, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from . import models, permissions, serializers

# Create your views here.


class UserLoginApiView(ObtainAuthToken):
    """ Login view """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handles UserProfile views """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = (permissions.UpdateOwnProfile,)


class UserStatusViewSet(viewsets.ModelViewSet):
    """ Handles UserStatus views """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserStatusSerializer
    queryset = models.UserStatus.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """ Sets the user profile to the logged-in user """
        serializer.save(user_profile=self.request.user)
