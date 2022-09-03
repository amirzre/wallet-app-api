from django.contrib import admin
from wallet import models


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'created_time')
    list_filter = ('transaction_type',)


@admin.register(models.UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_time')
    list_filter = ('user__email',)


@admin.register(models.TransferTransaction)
class TransferTransaction(admin.ModelAdmin):
    list_display = ('sender_transaction', 'receiver_transaction')
