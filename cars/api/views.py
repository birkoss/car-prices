from django.db.models import Count, Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Make, Model, Trim

from .serializers import MakeSerializer, ModelSerializer, ModelWriteSerializer, TrimSerializer, TrimWriteSerializer  # nopep8


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


class models(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, make, format=None):
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

    def get(self, request, make, format=None):

        # Validate the make
        make = fetch_make(slug=make)
        if make is None:
            return invalid_make()

        models = Model.objects.filter(
            make=make
        ).order_by("name")

        serializer = ModelSerializer(
            instance=models,
            many=True
        )

        return Response({
            'status': status.HTTP_200_OK,
            'models': serializer.data
        }, status=status.HTTP_200_OK)


class trims(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, make, model, format=None):
        # Validate the make
        make = fetch_make(slug=make)
        if make is None:
            return create_error_response("This make is invalid")

        # Validate the model
        model = fetch_model(slug=model, make=make)
        if model is None:
            return create_error_response("This model is invalid")

        # Validate the a trim with this ID doesn't already exists
        trim = Trim.objects.filter(
            model=model,
            foreign_id=request.data['foreign_id']
        ).first()
        if trim is not None:
            return create_error_response("This trim already exists")

        serializer = TrimWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(model=model)

            return Response({
                'status': status.HTTP_200_OK,
            })
        else:
            return create_error_response(serializer.error_messages)

    def get(self, request, make, model, format=None):
        # Validate the make
        make = fetch_make(slug=make)
        if make is None:
            return invalid_make()

        # Validate the model
        model = fetch_model(slug=model, make=make)
        if model is None:
            return invalid_model()

        trims = Trim.objects.filter(
            model=model
        ).order_by("name")

        serializer = TrimSerializer(
            instance=trims,
            many=True
        )

        return Response({
            'status': status.HTTP_200_OK,
            'trims': serializer.data
        }, status=status.HTTP_200_OK)


def fetch_make(**kwargs):
    make = Make.objects.filter(**kwargs).first()
    return make


def fetch_model(**kwargs):
    print(kwargs)
    model = Model.objects.filter(**kwargs).first()
    return model


def create_error_response(message):
    return Response({
        'status': status.HTTP_400_BAD_REQUEST,
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)
