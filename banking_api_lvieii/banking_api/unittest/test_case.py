
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from ..models import Customer, BankAccount, TransferHistory

class BankAPITest(APITestCase):
    
    def __init__(self, *args, **kwargs):
        super(BankAPITest, self).__init__(*args, **kwargs)
    
    def setUp(self):
        self.client = APIClient()
        self.customer_1 = Customer.objects.create(name="Test Customer")
        self.account_1 = BankAccount.objects.create(customer_id=self.customer_1.id, balance=1000.00)
        self.account_2 = BankAccount.objects.create(customer_id=self.customer_1.id, balance=2000.00)
        
        self.customer_2 = Customer.objects.create(name="Test Customer 2")
        self.account_3 = BankAccount.objects.create(customer_id=self.customer_2.id, balance=3000.00)
        

    def test_get_customer(self):      
        response = self.client.get('/api/banking/customers/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_account(self):      
        response = self.client.get('/api/banking/accounts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_transaction(self):      
        payload = {
            "from_acc_id": 1,
            "to_acc_id": 3,
            "amount": 5.0
        }
        self.client.post('/api/banking/transfers/', payload, format='json')
        response = self.client.get('/api/banking/transfers/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_account(self):
        payload = {
            "name": "Test Customer xxx",
            "initial_deposit": 500.00
            }
        # Your test case for creating an account        
        response = self.client.post('/api/banking/customers/', payload, format='json')

        is_customer = Customer.objects.filter(name='Test Customer xxx').exists()
        is_acc_bal = BankAccount.objects.filter(customer__name='Test Customer xxx').exists()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(is_customer, True)
        self.assertEqual(is_acc_bal, True)
        
        
    def test_create_same_account(self):
        payload = {
            "name": "Test Customer xxx",
            "initial_deposit": 500.00
            }
        # Your test case for creating an account        
        response = self.client.post('/api/banking/customers/', payload, format='json')
        response = self.client.post('/api/banking/customers/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_amount(self):
        # Your test case for transferring amount between accounts
        payload = {
            "from_acc_id": 1,
            "to_acc_id": 3,
            "amount": 5.0
        }
        
        response = self.client.post('/api/banking/transfers/', payload, format='json')
        acc_from = BankAccount.objects.get(id=1)
        acc_bal = BankAccount.objects.get(id=3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(acc_from.balance), 995)
        self.assertEqual(int(acc_bal.balance), 3005)
        
    def test_transfer_over_price_amount(self):
        # Your test case for transferring amount between accounts
        payload = {
            "from_acc_id": 1,
            "to_acc_id": 3,
            "amount": 10005.00
        }
        response = self.client.post('/api/banking/transfers/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_transfer_over_price_amount(self):
        # Your test case for transferring amount between accounts
        payload = {
            "from_acc_id": 1,
            "to_acc_id": 3,
            "amount": 10005.00
        }
        response = self.client.post('/api/banking/transfers/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)