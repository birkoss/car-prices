from django.db.models import Count, Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Make

from .serializers import MakeSerializer


class makes(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        filters = Q()

        makes = Make.objects.filter(
            filters
        ).order_by("name")

        serializer = MakeSerializer(
            instance=makes, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'makes': serializer.data
        }, status=status.HTTP_200_OK)


class make(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, make, format=None):

        # Validate the make
        make = fetch_make(slug=make)
        if make is None:
            return invalid_make()

        print(make)
        filters = Q()

        makes = Make.objects.filter(
            filters
        ).order_by("name")

        serializer = MakeSerializer(
            instance=makes, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'makes': serializer.data
        }, status=status.HTTP_200_OK)


def fetch_make(**kwargs):
    make = Make.objects.filter(**kwargs).first()
    return make


def invalid_make():
    return Response({
        'status': status.HTTP_403_FORBIDDEN,
    }, status=status.HTTP_403_FORBIDDEN)
