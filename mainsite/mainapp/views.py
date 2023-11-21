import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q 

from .forms import RegisterUserForm
from .utils import *
from .models import *


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    org = get_user_org(request.user)
    assets = get_org_assets(org)

    return render(request, 'index.html', {'assets': assets})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        
        messages.success(request, "Error logging in. Try again")

    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('index')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('index')
        
    form = RegisterUserForm()   
    return render(request, 'register.html', {'form': form})

def store(request):
    if request.method == 'POST' and request.user.is_authenticated:
        org_id = get_user_org(request.user).org_id

        # raising purchase orders
        cart_text = request.POST['cart_text']
        # separate POs are created for each supplier
        cart = json.loads(cart_text)
        for supplier_id in cart:
            # create purchase order
            po = PurchaseOrder(src_org_id=supplier_id, dest_org_id=org_id)
            po.save()
            order_id = po.order_id

            # create purchase order details
            for asset_id, qty in supplier_id:
                pod = PurchaseOrderDetails(order_id=order_id, asset_id=asset_id, qty=qty)
                pod.save()

        return redirect('orders')
    
    return render(request, 'store.html')
    

def orders(request):
    # only supplier will see an approve reject option, and only pending status can be changed
    if request.user and request.user.is_authenticated:
        purchase_orders = {}
        org_id = get_user_org(request.user).org_id

        temp_orders = PurchaseOrder.objects.filter(Q(src_org_id=org_id) | Q(dest_org_id=org_id))
        for po in temp_orders:
            purchase_orders[po.order_id]['can_edit'] = False 
            if po.src_org_id == org_id and po.approval_status == 'P':
                purchase_orders[po.order_id]['can_edit'] = True 

            purchase_orders[po.order_id]['items'] = PurchaseOrderDetails.objects.filter(order_id=po.order_id)

        return render(request, 'billing.html', {'orders': purchase_orders}) 

    return redirect('index') 


def approve_or_reject_po(request):
    # remember to add csrf token
    if request.method == 'POST':
        decision = request.POST['decision']
        order_id = request.POST['order_id']
        comment  = request.POST['comment']
        po = PurchaseOrder.objects.filter(order_id=order_id)
        if decision == 'approve':
            # reduce items in source and add to destination
            po.approval_status = 'A'

        elif decision == 'reject':
            po.approval_status = 'R'
            po.comment = comment
        
        po.updated_on = datetime.now()
        po.save()

        return redirect('orders')