from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 画面に出したい項目だけ並べれば OK
        fields = ("id", "username", "email", "first_name", "last_name")

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
     # email を optional にして、空文字も許容
    email = serializers.EmailField(required=False, allow_blank=True)


    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # create_user を使うことでパスワードがハッシュ化されます
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", "")

            )


