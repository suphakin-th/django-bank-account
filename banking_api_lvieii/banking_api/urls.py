from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerView, BankAccountViewSet, TransferHistoryViewSet

router = DefaultRouter()
router.register(r'customers', CustomerView)
router.register(r'accounts', BankAccountViewSet)
router.register(r'transfers', TransferHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]