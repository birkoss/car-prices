from django.db.models import Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.helpers import create_error_response
from cars.models import fetch_make, fetch_model, fetch_trim

from ..models import Price

from .serializers import PriceSerializer, PriceTrimSerializer  # nopep8


class make(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, make_slug, format=None):
        make = fetch_make(slug=make_slug)
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


class prices(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, trim_id, format=None):
        trim = fetch_trim(id=trim_id)
        if trim is None:
            return create_error_response("This trim is invalid")

        data = getPrices(trim=trim, is_active=True)

        return Response({
            'status': status.HTTP_200_OK,
            'prices': data,
        }, status=status.HTTP_200_OK)

    def post(self, request, trim_id, format=None):
        trim = fetch_trim(id=trim_id)
        if trim is None:
            return create_error_response("This trim is invalid")

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
                    serializer.save(is_active=False, trim=trim, is_pending=True)  # nopep8
                else:
                    price.msrp = serializer.validated_data['msrp']
                    price.taxes = serializer.validated_data['taxes']
                    price.delivery = serializer.validated_data['delivery']
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


class prices_pending(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, trim_id, format=None):
        trim = fetch_trim(id=trim_id)
        if trim is None:
            return create_error_response("This trim is invalid")

        data = getPrices(trim=trim, is_pending=True)

        return Response({
            'status': status.HTTP_200_OK,
            'prices': data,
        }, status=status.HTTP_200_OK)


class trim_type(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, trim_id, price_type, format=None):
        trim = fetch_trim(id=trim_id)
        if trim is None:
            return create_error_response("This trim is invalid")

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


def getPrices(**kwargs):
    price = Price.objects.filter(**kwargs).first()
    if price is not None:
        price = PriceSerializer(instance=price, many=False).data  # nopep8

    return price
