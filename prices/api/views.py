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


class trim_type(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, make, model, trim, price_type, format=None):
        make = fetch_make(slug=make)
        if make is None:
            return create_error_response("This make is invalid")

        model = fetch_model(slug=model)
        if model is None:
            return create_error_response("This model is invalid")

        trim = fetch_trim(slug=trim)
        if trim is None:
            return create_error_response("This trim is invalid")

        price_type = PriceType.objects.filter(slug=price_type).first()
        if price_type is None:
            return create_error_response("This price type is invalid")

        price = None
        price_is_new = True

        # Verify with the active and pending price if they are not the same
        price_pending = Price.objects.filter(trim=trim, is_pending=True).order_by("-id").first()  # nopep8
        if price_pending is not None:
            if price_pending.hash != request.data['hash']:
                price = price_pending
            else:
                # Same hash as the pending price
                price_is_new = False
        else:
            price_active = Price.objects.filter(trim=trim, is_active=True).order_by("-id").first()  # nopep8
            if price_active is not None:
                # Same hash as the active price (and no pending price)
                if price_active.hash == request.data['hash']:
                    price_is_new = False

        if price_is_new:
            serializer = PriceSerializer(data=request.data)
            if serializer.is_valid():
                if price is None:
                    serializer.save(is_active=False, trim=trim, type=price_type, is_pending=True)  # nopep8
                else:
                    print(request.data['data'])
                    print(serializer.fields['data'])
                    price.data = serializer.validated_data['data']
                    price.hash = serializer.validated_data['hash']
                    price.save()

                return Response({
                    "status": status.HTTP_200_OK,
                    "message": ("Created" if price is None else "Updated")
                })
            else:
                return create_error_response(serializer.error_messages)
        else:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Skipped"
            })
