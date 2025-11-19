from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account, Transaction

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Account'

class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_balance', 'is_staff')
    
    def get_balance(self, obj):
        if hasattr(obj, 'account'):
            return obj.account.balance
        return "No account"
    get_balance.short_description = 'Balance'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'transaction_type', 'timestamp', 'description', 'status', 'recipient_email', 'recipient_bank')
    list_filter = ('transaction_type', 'timestamp', 'status')
    search_fields = ('account__user__username', 'description', 'recipient_email', 'recipient_bank')
    list_editable = ('status',)