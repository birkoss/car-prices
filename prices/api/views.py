from django.db.models import Q
from django.core.exceptions import ValidationError

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.helpers import create_error_response
from cars.models import fetch_make, fetch_model, fetch_trim

from ..models import Price

from .serializers import PriceSerializer, PriceTrimSerializer  # nopep8


# Get the prices for this make
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


# Get the active and pending prices for this model
class models(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, model_id, format=None):
        model = fetch_model(id=model_id)
        if model is None:
            return create_error_response("This model is invalid")

        prices_active = Price.objects.filter(
            is_active=True,
            trim__model=model
        )
        serializer_active = PriceTrimSerializer(
            instance=prices_active, many=True
        )

        prices_pending = Price.objects.filter(
            is_pending=True,
            trim__model=model
        )
        serializer_pending = PriceTrimSerializer(
            instance=prices_pending, many=True
        )

        return Response({
            'status': status.HTTP_200_OK,
            'prices': {
                "active": serializer_active.data,
                "pending": serializer_pending.data,
            }
        }, status=status.HTTP_200_OK)

    def put(self, request, model_id, format=None):
        model = fetch_model(id=model_id)
        if model is None:
            return create_error_response("This model is invalid")

        # Validate the prices id
        if "prices" not in request.data or not isinstance(request.data['prices'], list) or len(request.data['prices']) == 0:  # nopep8
            return create_error_response("You must specify prices ID")

        total_updated_prices = 0

        for price_id in request.data['prices']:
            try:
                price = Price.objects.filter(id=price_id, trim__model=model, is_pending=True).first()  # nopep8
                if price is not None:
                    # Unvalidate all prices of this trim
                    Price.objects.filter(trim=price.trim, is_active=True).update(is_active=False)  # nopep8

                    # Remove pending and activate it
                    price.is_active = True
                    price.is_pending = False
                    price.save()

                    total_updated_prices = total_updated_prices + 1
            except ValidationError:
                pass

        return Response({
            "status": status.HTTP_200_OK,
            "total": total_updated_prices,
        })


class prices(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, trim_id, format=None):
        trim = fetch_trim(id=trim_id)
        if trim is None:
            return create_error_response("This trim is invalid")

        prices_active = Price.objects.filter(
            is_active=True,
            trim=trim
        )
        serializer_active = PriceTrimSerializer(
            instance=prices_active, many=True
        )

        prices_pending = Price.objects.filter(
            is_pending=True,
            trim=trim
        )
        serializer_pending = PriceTrimSerializer(
            instance=prices_pending, many=True
        )

        return Response({
            'status': status.HTTP_200_OK,
            'prices': {
                "active": serializer_active.data,
                "pending": serializer_pending.data,
            },
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


def getPrices(**kwargs):
    price = Price.objects.filter(**kwargs).first()
    if price is not None:
        price = PriceSerializer(instance=price, many=False).data  # nopep8

    return price
