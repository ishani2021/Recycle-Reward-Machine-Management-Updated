from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Waste, wasteType, user, Order

def company_check(user):
    # Check if the user is part of the company group or has a company-specific attribute
    return user.is_staff  # Example: Assuming 'is_staff' is used to denote company users


@login_required
@user_passes_test(company_check)
def place_order_view(request):
    if request.method == 'POST':
        waste_type = request.POST.get('waste_type')
        quantity = int(request.POST.get('quantity', 1))
        company = request.user

        available_waste = Waste.objects.filter(waste_type=waste_type)[:quantity]

        if len(available_waste) == quantity:
            order = Order.objects.create(company=company, waste_type=waste_type, quantity=quantity, status='Placed')
            available_waste.delete()
            return redirect('company_dashboard')
        else:
            return render(request, 'place_order.html', {'error': 'Not enough waste available'})

    return render(request, 'place_order.html', {'waste_types': wasteType.choices()})

@login_required
@user_passes_test(company_check)
def cancel_order_view(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user == order.company:
        waste_type = order.waste_type
        quantity = order.quantity
        order.delete()

        for _ in range(quantity):
            Waste.objects.create(waste_type=waste_type)

        return redirect('company_dashboard')

    return redirect('company_dashboard')


@login_required
@user_passes_test(company_check)
def company_dashboard(request):
    company = request.user
    orders = Order.objects.filter(company=company)
    return render(request, 'company_dashboard.html', {'company': company, 'orders': orders})


@login_required
@user_passes_test(company_check)
def view_orders_view(request):
    orders = Order.objects.filter(company=request.user)  # Filter orders by the logged-in company
    return render(request, 'view_orders.html', {'orders': orders})


@login_required
def user_dashboard(request):
    user=request.user
    return render(request, 'user_dashboard.html', {'user':user})


@login_required
def enter_waste_view(request):
    if request.method == 'POST':
        waste_type = request.POST.get('waste_type')
        quantity = int(request.POST.get('quantity', 1))
        user = request.user

        for _ in range(quantity):
            Waste.objects.create(waste_type=waste_type)

        user.credits += quantity
        user.save()

        return redirect('user_dashboard')

    return render(request, 'enter_waste.html', {'waste_types': wasteType.choices()})


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        user.phone = request.POST.get('phone')
        user.name = request.POST.get('name')
        user.save()
        return redirect('user_dashboard')

    return render(request, 'update_profile.html', {'user': user})


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('company_dashboard')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

