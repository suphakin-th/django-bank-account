from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Customer, BankAccount, TransferHistory
from .serializers import CustomerSerializer, BankAccountSerializer, TransferHistorySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

class TransferHistoryViewSet(viewsets.ModelViewSet):
    queryset = TransferHistory.objects.all()
    serializer_class = TransferHistorySerializer