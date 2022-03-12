from django.contrib.auth.models import User
from rest_framework import serializers
from backend.models import Account, Operation


class PersonalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'title', 'user')


class UserSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class FullOperationSerializer(serializers.ModelSerializer):
    operation_from = AccountSerializer(
        many=True,
        read_only=True)
    operation_to = AccountSerializer(
        read_only=True)

    class Meta:
        model = Operation
        fields = '__all__'


class ShortOperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        sum = validated_data['sum']
        separated_sum = sum / len(validated_data['operation_from'])

        operation_from = validated_data['operation_from']
        operation_to = validated_data['operation_to']
        for account in operation_from:
            balance = account.balance - separated_sum

            account = Account.objects.filter(id=account.id)
            account.update(balance=balance)
        balance = operation_to.balance + separated_sum
        account = Account.objects.filter(id=operation_to.id)
        account.update(balance=balance)

        return super().create(validated_data)
