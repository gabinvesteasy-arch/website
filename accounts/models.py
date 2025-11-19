from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Account"

# Signal to automatically create Account when User is created
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    if hasattr(instance, 'account'):
        instance.account.save()

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.CharField(max_length=100)  # CHANGED TO CharField
    transaction_type = models.CharField(max_length=10)  # deposit / withdraw / transfer
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, default="")
    status = models.CharField(max_length=20, default="Processing")  # Processing, Completed, Failed
    recipient_email = models.EmailField(blank=True, null=True)  # Store recipient email
    recipient_bank = models.CharField(max_length=100, blank=True, null=True)  # Store bank

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.status}"