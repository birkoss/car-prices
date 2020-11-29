from django.db.models import Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Make, Model, Trim

from .serializers import MakeSerializer, ModelSerializer, ModelWriteSerializer, TrimSerializer, TrimModelSerializer, TrimWriteSerializer  # nopep8


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
            return create_error_response("This make is invalid")

        models = Model.objects.filter(
            make=make,
            is_active=True
        ).order_by("name", "year")

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

    def get(self, request, make, model=None, format=None):
        # Validate the make
        make = fetch_make(slug=make)
        if make is None:
            return create_error_response("This make is invalid")

        serializer_class = TrimSerializer

        filters = Q()
        filters.add(Q(is_active=True), Q.AND)

        # Validate the model (if provided)
        if model is not None:
            model = fetch_model(slug=model, make=make)
            if model is None:
                return create_error_response("This model is invalid")
            filters.add(Q(model=model), Q.AND)
        else:
            serializer_class = TrimModelSerializer
            filters.add(Q(model__make=make), Q.AND)

        trims = Trim.objects.filter(
            filters
        ).order_by("model__name", "model__year", "name")

        serializer = serializer_class(
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
    kwargs['is_active'] = True
    model = Model.objects.filter(**kwargs).first()
    return model


def create_error_response(message):
    return Response({
        'status': status.HTTP_400_BAD_REQUEST,
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)
