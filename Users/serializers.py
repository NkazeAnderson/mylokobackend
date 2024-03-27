from rest_framework import serializers
from Users.models import CustomUser

class UserSerializer (serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = [
           "phone", "password", "email", "first_name", "last_name",  "id", "profile_picture"
        ]
        
    def validate(self, attrs):
        password = attrs["password"]
        request = self.context.get("request")
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password too short"})
        return attrs