import datetime
from rest_framework import serializers
import accounts.models as account_models


class UserSerializers(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = account_models.CustomUser
        fields = ["name", "gender", "date_of_birth", "date_joined"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    dob = serializers.DateField(help_text="Date of birth (YYYY-MM-DD)")
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_dob(self, value):
        if value >= datetime.date.today():
            raise serializers.ValidationError(
                "Date of birth must be in the past."
            )

        return value
