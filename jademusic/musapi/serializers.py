from rest_framework.serializers import ModelSerializer

from musapi.models import JadeMusicUser


class JadeMusicUserSerializer(ModelSerializer):
    class Meta:
        model = JadeMusicUser
        fields = ('id', 'telegram_user_id', 'username', 'email', 'is_staff', 'is_superuser', 'date_joined')
