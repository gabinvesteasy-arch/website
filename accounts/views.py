from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout  # ADD THIS IMPORT
# ---------------------------
# LOGIN VIEW
# ---------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


# ---------------------------
# LOGOUT VIEW
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------------------
# SIGNUP VIEW
# ---------------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Account is automatically created via signal
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "signup.html")


# ---------------------------
# DASHBOARD VIEW
# ---------------------------
@login_required
def dashboard(request):
    # Use the account from the logged-in user - fresh database query
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')[:10]
    
    # DEBUG: Print to console
    print(f"DASHBOARD - User: {request.user.username}, Balance: {account.balance}")
    
    return render(request, "dashboard.html", {
        "account": account,
        "transactions": transactions,
    })





# ---------------------------
# TRANSFER VIEW - UPDATED
# ---------------------------
@login_required
def transfer(request):
    account = request.user.account
    if request.method == "POST":
        recipient_email = request.POST.get("to_user")
        recipient_bank = request.POST.get("recipient_bank")
        amount = request.POST.get("amount", "0")
        
        if not amount:
            messages.error(request, "Amount is required.")
            return redirect("transfer")
            
        # Prevent transferring to yourself
        if recipient_email == request.user.email:
            messages.error(request, "Cannot transfer to yourself.")
            return redirect("transfer")
        
        # ALWAYS CREATE TRANSACTION - NO BALANCE CHECKS, NO CONVERSIONS
        Transaction.objects.create(
            account=account,
            amount=amount,  # Store as text directly
            transaction_type="transfer",
            description=f"Transfer to {recipient_email} - {recipient_bank}",
            status="Processing",
            recipient_email=recipient_email,
            recipient_bank=recipient_bank
        )
        
        messages.success(request, f"Transfer initiated! ${amount} processing to {recipient_email}")
        return redirect("dashboard")
    
    return render(request, "transfer.html", {"account": account})