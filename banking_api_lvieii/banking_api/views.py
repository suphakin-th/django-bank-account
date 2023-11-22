from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, mixins
from utils.response import Response
from rest_framework.exceptions import NotFound
from .models import Customer, BankAccount, TransferHistory
from .serializers import BankAccountCreateSerializer, BankAccountListSerializer, CustomerCreateSerializer, CustomerSerializer, BankAccountSerializer, TransferCreateSerializer, TransferHistorySerializer

class CustomerView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    # Query for all data first file called by server
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    action_serializers = {
        'retrieve': CustomerSerializer,
        'list': CustomerSerializer,
        'create': CustomerCreateSerializer,
    }
    
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
    
        customer = Customer.objects.create(name=data.get('name'))
        back_account = BankAccount.objects.create(
            customer_id=customer.id, 
            balance=data.get('initial_deposit')
        )
        result = {
            'customer_id': customer.id,
            'customer_name': customer.name,
            'back_account_id': back_account.id,
            'back_account_balance': back_account.balance
            }
        return Response(data=result, status=status.HTTP_201_CREATED)
    

class BankAccountViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    
    action_serializers = {
        'retrieve': BankAccountListSerializer,
        'list': BankAccountListSerializer,
        'create': BankAccountCreateSerializer,
    }
    
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
    
        customer = Customer.objects.filter(name=data.get('customer_name')).first()
        if not customer:
            raise NotFound
        bank_account = BankAccount.objects.create(
            customer_id=customer.id, 
            balance=data.get('initial_deposit')
        )
        result = {
            'customer_id': customer.id,
            'customer_name': customer.name,
            'bank_account_id': bank_account.id,
            'bank_account_balance': bank_account.balance
            }
        return Response(data=result, status=status.HTTP_201_CREATED)
    
    

class TransferHistoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = TransferHistory.objects.all()
    serializer_class = TransferHistorySerializer
    
    action_serializers = {
        'retrieve': TransferHistorySerializer,
        'list': TransferHistorySerializer,
        'create': TransferCreateSerializer,
    }
    
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        #set variable
        cus_sent = data.get('from_customer_name')
        cus_to = data.get('to_customer_name')
        amount = float(data.get('amount'))
        
        customer = dict(list(Customer.objects.filter(name__in=[cus_sent, cus_to]).values_list("id", "name")))
        print(customer.values())
        
        if data.get('from_customer_name') not in customer.values() or data.get('to_customer_name') not in customer.values():
            raise NotFound
        
        # Check balance        
        is_remain_customer = BankAccount.objects.filter(customer__name=cus_sent, balance__gte=amount).exists()
        if not is_remain_customer:
            return Response(data={'Details': "Account don't have enough money"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # create and transfer money
        ## create transaction
        transaction = TransferHistory.objects.create(
            sender_id=list(customer.keys())[list(customer.values()).index(cus_sent)],
            receiver_id=list(customer.keys())[list(customer.values()).index(cus_to)],
            amount=amount
        )
        sender_account = BankAccount.objects.get(id=list(customer.keys())[list(customer.values()).index(cus_sent)])
        receiver_account = BankAccount.objects.get(id=list(customer.keys())[list(customer.values()).index(cus_to)])

        sender_account.balance = float(sender_account.balance) - amount
        receiver_account.balance = float(receiver_account.balance) + amount
        sender_account.save()
        receiver_account.save()
        return Response(data=TransferHistorySerializer(transaction).data, status=status.HTTP_201_CREATED)