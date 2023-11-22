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
        from_acc_id = data.get('from_acc_id')
        to_acc_id = data.get('to_acc_id')
        amount = float(data.get('amount'))
        
        customer = dict(list(BankAccount.objects.filter(id__in=[from_acc_id, to_acc_id]).values_list("customer_id", "customer__name")))
        print(customer.keys())
        if from_acc_id not in customer.keys() or to_acc_id not in customer.keys():
            raise NotFound
        
        # Check balance        
        is_remain_customer = BankAccount.objects.filter(id=from_acc_id, balance__gte=amount).exists()
        if not is_remain_customer:
            return Response(data={'Details': "Account don't have enough money"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # create and transfer money
        ## create transaction
        transaction = TransferHistory.objects.create(
            sender_id=from_acc_id,
            receiver_id=to_acc_id,
            amount=amount
        )
        sender_account = BankAccount.objects.get(id=from_acc_id)
        receiver_account = BankAccount.objects.get(id=to_acc_id)

        sender_account.balance = float(sender_account.balance) - amount
        receiver_account.balance = float(receiver_account.balance) + amount
        sender_account.save()
        receiver_account.save()
        return Response(data=TransferHistorySerializer(transaction).data, status=status.HTTP_201_CREATED)