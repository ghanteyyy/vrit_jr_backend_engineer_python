from rest_framework import serializers
import accounts.models as account_models


class UserSerializers(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = account_models.CustomUser
        fields = ["name", "gender", "date_of_birth", "date_joined"]
