from rest_framework import serializers
from .models import Customer, BankAccount, TransferHistory

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
class CustomerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    initial_deposit = serializers.IntegerField(required=True)
    
    def validate(self, value):
        # filter out for same name.
        customer_list = Customer.objects.filter(name=value['name'])
        if self.instance:
            customer_list = customer_list.exclude(pk=self.instance.pk)
        if customer_list.exists():
            raise serializers.ValidationError('Customer code already exists.')
        
        if isinstance(value['initial_deposit'], int) and int(value['initial_deposit']) <= 0:
            raise serializers.ValidationError('initial deposit code is below zero.')
            
        return value

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
        
class BankAccountListSerializer(serializers.ModelSerializer):
    customer_details = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = (
            'id',
            'balance',
            'customer_details'
        )
    
    def get_customer_details(self, instance):
        return CustomerSerializer(instance.customer).data

class BankAccountCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(required=True)
    initial_deposit = serializers.IntegerField(required=True)
    
    def validate(self, value):
        if isinstance(value['initial_deposit'], int) and int(value['initial_deposit']) <= 0:
            raise serializers.ValidationError('initial deposit code is below zero.')
        return value

class TransferHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferHistory
        fields = '__all__'

class TransferCreateSerializer(serializers.Serializer):
    from_acc_id = serializers.IntegerField(required=True)
    to_acc_id = serializers.IntegerField(required=True)
    amount = serializers.FloatField(required=True)
    
    def validate(self, value):
        if isinstance(value['amount'], float) and float(value['amount']) <= 0.0:
            raise serializers.ValidationError('amount code is below zero.')
        return value
        
        
