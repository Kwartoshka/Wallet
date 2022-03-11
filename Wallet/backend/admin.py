from django.contrib import admin

# Register your models here.
from backend.models import Account, Operation


@admin.register(Account)
class ProductAdmin(admin.ModelAdmin):
    exclude = ()
    pass

@admin.register(Operation)
class ProductAdmin(admin.ModelAdmin):
    exclude = ()
    pass