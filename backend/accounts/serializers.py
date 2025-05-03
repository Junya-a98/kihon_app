from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 画面に出したい項目だけ並べれば OK
        fields = ("id", "username", "email", "first_name", "last_name")

