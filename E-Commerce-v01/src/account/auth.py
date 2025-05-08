from rest_framework.decorators import action
from .serializers import UserModelSerializer
from rest_framework.viewsets import ModelViewSet
from .models import User

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'], url_path='change-password')
    def change_password(self, request, pk=None):
        user = self.get_object()

        # Validation des données
        if 'old_password' not in request.data or 'new_password' not in request.data:
            return Response(
                {'error': 'old_password and new_password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification de l'ancien mot de passe
        if not user.check_password(request.data['old_password']):
            return Response(
                {'error': 'Wrong old password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mise à jour du mot de passe
        user.set_password(request.data['new_password'])
        user.save()

        return Response({'status': 'password set'}, status=status.HTTP_200_OK)
