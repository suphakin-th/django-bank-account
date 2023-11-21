from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)

class BankAccount(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class TransferHistory(models.Model):
    sender = models.ForeignKey(BankAccount, related_name='transfers_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(BankAccount, related_name='transfers_received', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)