from django.db.models import Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.helpers import create_error_response
from cars.models import fetch_make, fetch_model, fetch_trim

from ..models import Price, PriceType

from .serializers import PriceSerializer, PriceTrimSerializer  # nopep8


class make(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, make, format=None):
        make = fetch_make(slug=make)
        if make is None:
            return create_error_response("This make is invalid")

        prices = Price.objects.filter(
            is_active=True,
            trim__model__make=make
        )

        serializer = PriceTrimSerializer(
            instance=prices, many=True
        )

        return Response({
            'status': status.HTTP_200_OK,
            'makes': serializer.data
        }, status=status.HTTP_200_OK)


class trim(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, make, model, trim, format=None):
        # Validate the make
        make = fetch_make(slug=make)
        if make is None:
            return create_error_response("This make is invalid")

        # Validate the model with this Foreign ID doesn't already exists
        model = Model.objects.filter(
            make=make,
            foreign_id=request.data['foreign_id']
        ).first()
        if model is not None:
            return create_error_response("This model already exists")

        serializer = ModelWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(make=make)

            return Response({
                'status': status.HTTP_200_OK,
            })
        else:
            return create_error_response(serializer.error_messages)

    def get(self, request, make, model, trim, format=None):
        make = fetch_make(slug=make)
        if make is None:
            return create_error_response("This make is invalid")

        model = fetch_model(slug=model)
        if model is None:
            return create_error_response("This model is invalid")

        trim = fetch_trim(slug=trim)
        if trim is None:
            return create_error_response("This trim is invalid")

        prices = Price.objects.filter(
            is_active=True,
            trim=trim
        )

        serializer = PriceSerializer(
            instance=prices, many=True
        )

        return Response({
            'status': status.HTTP_200_OK,
            'makes': serializer.data
        }, status=status.HTTP_200_OK)
