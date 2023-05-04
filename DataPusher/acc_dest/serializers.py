from rest_framework.serializers import ModelSerializer, Serializer, CharField, EmailField
from .models import *


class AccountSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context:
            self.fields['acc_secret'].read_only = True
        else:
            self.fields['acc_secret'].write_only = True

    class Meta:
        model = Accounts
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }


class AccountLoginSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(required=True, max_length=20, min_length=1)


class DestinationSerializer(ModelSerializer):
    class Meta:
        model = Destinations
        fields = '__all__'
