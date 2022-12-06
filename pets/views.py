from rest_framework.views import APIView, Response, Request, status
from .models import Pet
from .serializers import PetSerializer
from django.shortcuts import get_object_or_404


class PetView(APIView):
    def get(self, request: Request) -> Response:
        users = Pet.objects.all()

        serializer = PetSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:

        pet = get_object_or_404(
            Pet,
            id=pet_id,
        )

        serializer = PetSerializer(pet)

        return Response(serializer.data)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(
            Pet,
            id=pet_id,
        )

        serializer = PetSerializer(
            pet,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(
            Pet,
            id=pet_id,
        )

        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
