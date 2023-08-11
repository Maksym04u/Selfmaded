from rest_framework import serializers
from .models import MyUser, Interest
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(write_only=True, required=True)
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True)


    class Meta:
        model = MyUser
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "interests"
        ]
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        user = MyUser(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            
        )
        user.set_password(validated_data["password"])
        user.save()
        user.interests.set(validated_data["interests"])
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True, required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model=MyUser
        fields=[
            "username", 
            "email", 
            "first_name", 
            "last_name", 
            "interests", 
            "image", 
            "description", 
            "links"
        ]