from django.db.models import Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.helpers import create_error_response

from ..models import Make, Model, Trim, fetch_make, fetch_model, fetch_trim

from .serializers import MakeSerializer, ModelSerializer, ModelWriteSerializer, TrimSerializer, TrimWriteSerializer  # nopep8


class make(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, make_slug, format=None):
        make = fetch_make(slug=make_slug)
        if make is None:
            return create_error_response("This make is invalid")

        serializer = MakeSerializer(
            instance=make, many=False)

        return Response({
            'status': status.HTTP_200_OK,
            'make': serializer.data
        }, status=status.HTTP_200_OK)


class makes(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        makes = Make.objects.all().order_by("name")

        serializer = MakeSerializer(instance=makes, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'makes': serializer.data
        }, status=status.HTTP_200_OK)


class model(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, model_id, format=None):
        model = fetch_model(id=model_id)
        if model is None:
            return create_error_response("This model is invalid")

        serializer = ModelSerializer(
            instance=model,
            many=False
        )

        return Response({
            'status': status.HTTP_200_OK,
            'model': serializer.data
        }, status=status.HTTP_200_OK)


class models(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, make_slug, format=None):
        # Validate the make
        make = fetch_make(slug=make_slug)
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

    def get(self, request, make_slug, format=None):

        # Validate the make
        make = fetch_make(slug=make_slug)
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

    def post(self, request, model_id, format=None):
        model = fetch_model(id=model_id)
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

    def get(self, request, model_id=None, make_slug=None, format=None):
        filters = Q()
        filters.add(Q(is_active=True), Q.AND)

        # Validate the model (if provided)
        if model_id is not None:
            model = fetch_model(id=model_id)
            if model is None:
                return create_error_response("This model is invalid")
            filters.add(Q(model=model), Q.AND)
        else:
            make = fetch_make(slug=make_slug)
            if make is None:
                return create_error_response("This make is invalid")

            filters.add(Q(model__make=make), Q.AND)

        trims = Trim.objects.filter(
            filters
        ).order_by("model__name", "model__year", "name")

        serializer = TrimSerializer(
            instance=trims,
            many=True
        )

        return Response({
            'status': status.HTTP_200_OK,
            'trims': serializer.data
        }, status=status.HTTP_200_OK)


class trim(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, trim_id, format=None):
        trim = fetch_trim(id=trim_id)
        if trim is None:
            return create_error_response("This trim is invalid")

        serializer = TrimSerializer(
            instance=trim,
            many=False
        )

        return Response({
            'status': status.HTTP_200_OK,
            'trim': serializer.data
        }, status=status.HTTP_200_OK)


def create_error_response(message):
    return Response({
        'status': status.HTTP_400_BAD_REQUEST,
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)
