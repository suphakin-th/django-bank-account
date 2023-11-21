from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, BankAccountViewSet, TransferHistoryViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'accounts', BankAccountViewSet)
router.register(r'transfers', TransferHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]