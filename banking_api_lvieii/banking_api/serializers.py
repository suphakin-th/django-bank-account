from rest_framework import serializers
from .models import Customer, BankAccount, TransferHistory

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class TransferHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferHistory
        fields = '__all__'