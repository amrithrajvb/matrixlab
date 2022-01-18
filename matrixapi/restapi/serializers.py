from rest_framework.serializers import ModelSerializer

from restapi.models import MyUser, Worknotes
from rest_framework import serializers


class UserCreationSerializer(ModelSerializer):
    class Meta:
        model=MyUser
        fields=["email","password","role","phone",]

    def create(self, validated_data):
        return MyUser.objects.create_user(email=validated_data["email"],
                                          phone=validated_data["phone"],
                                          role="member",
                                          password=validated_data["password"])


class WorknotesSerializers(ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Worknotes
        fields=["id","title","notes","notes_image","user"]

class SigninSerializer(serializers.Serializer):
    email=serializers.CharField()
    password=serializers.CharField()

