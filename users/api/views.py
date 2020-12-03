from django.contrib.auth import login, authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


from ..models import User


class loginUser(APIView):
    def post(self, request, format=None):

        user = authenticate(
            request,
            email=request.data['email'],
            password=request.data['password'])
        if user is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': 'Invalid information'
            }, status=status.HTTP_404_NOT_FOUND)

        login(request, user)

        token = Token.objects.get(user=user)

        return Response({
            'status': status.HTTP_200_OK,
            'token': token.key,
        }, status=status.HTTP_200_OK)
