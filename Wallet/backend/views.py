from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .models import Account, Operation
from .serializers import AccountSerializer, UserSerializer, PersonalAccountSerializer, FullOperationSerializer,\
    ShortOperationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class PersonalAccountsViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = PersonalAccountSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ProductFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['list']:
            return [IsAuthenticated()]
        return []

class AccountsViewSet(ModelViewSet):

    queryset = Account.objects.all()
    # serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user']

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['list']:
            return [IsAuthenticated()]
        else:
            return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            account = Account.objects.filter(id=self.kwargs['pk']).first()
            print(account)
            if account.user == self.request.user:
                return PersonalAccountSerializer
            else:
                return AccountSerializer
        else:
            return AccountSerializer

class OperationsViewSet(ModelViewSet):
    queryset = Operation.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation_to', 'operation_from', 'sum', 'date']

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        queryset = self.queryset.filter(Q(operation_to__in=accounts) | Q(operation_from__in=accounts)).distinct()
        return queryset

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'list':
            return FullOperationSerializer
        else:
            return ShortOperationSerializer


