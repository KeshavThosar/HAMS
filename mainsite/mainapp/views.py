import json
import logging
from datetime import datetime
from urllib.parse import unquote

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q 

from .forms import RegisterUserForm
from .utils import *
from .models import *

logger = logging.getLogger(__name__)

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    org = get_user_org(request.user)
    assets = get_org_assets(org)

    return render(request, 'index.html', {'assets': assets, 'org': org})

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
    if not request.user.is_authenticated:
        return redirect('login')

    
    # check for zero qty as well
    if request.method == 'POST':
        user_org = get_user_org(request.user)
        org = user_org.org_id

        cartJson = unquote(request.POST['cartText'])
        cartDict = json.loads(cartJson)
        cart = list(cartDict['cart'])
        # return HttpResponse(cart[0])

        supplierPO = {}
        purchases = []
        # generate PO for each supplier
        for item in cart:
            if not item['qty']: continue
            try:
                _ = supplierPO[item['orgId']]
            except Exception:
                src_org = Organization.objects.get(pk=item['orgId'])
                po = PurchaseOrder(src_org_id=src_org, dest_org_id=org)
                po.save()
                supplierPO[item['orgId']] = po
                
            
        # populate each purchase order
        for item in cart:
            if not item['qty']: continue

            pod = PurchaseOrderDetails(order_id=supplierPO[item['orgId']], asset_id=Asset.objects.get(pk=item['assetId']), qty=item['qty'])
            pod.save()
            purchases.append(pod)

            # edit inventory instantaneously as of now
            try:
                hospitalStock = OrganizationStock.objects.get(org_id=org, asset_id=pod.asset_id)
            except OrganizationStock.DoesNotExist:
                hospitalStock = OrganizationStock(org_id=org, asset_id=pod.asset_id, qty_available=0, price_per_unit=0)
            
            hospitalStock.qty_available += int(pod.qty)
            hospitalStock.save()


            for pod in purchases:
                supplierStock = OrganizationStock.objects.get(org_id=pod.order_id.src_org_id, asset_id=pod.asset_id)
                supplierStock.qty_available -= int(pod.qty)
                supplierStock.save()

        return redirect('orders')

    products = []
    suppliers = Organization.objects.filter(org_type='S')
    for supp in suppliers:
        stock = OrganizationStock.objects.filter(org_id=supp)
        for item in stock:
            products.append(item)
    return render(request, 'store.html', {'products': products, 'org': get_user_org(request.user)})
    

def orders(request):
    if  request.user.is_authenticated:
        purchase_orders = []
        org_id = get_user_org(request.user).org_id

        temp_orders = PurchaseOrder.objects.filter(Q(src_org_id=org_id) | Q(dest_org_id=org_id))

        for po in temp_orders:
            items = []
            total_price = 0
            pod = PurchaseOrderDetails.objects.filter(order_id=po.order_id)
            for item in pod:
                stock_item = OrganizationStock.objects.get(org_id=po.src_org_id, asset_id=item.asset_id)
                price = stock_item.price_per_unit
                items.append(
                    {'name': item.asset_id.name,
                     'qty': item.qty,
                     'price': price})
                total_price += item.qty * price
                
            purchase_orders.append({'order_id': po.order_id, 'src_org': po.src_org_id.name, 'dest_org': po.dest_org_id.name, 'items': items, 'total_price': total_price, 'created_on': po.created_on})
        purchase_orders.sort(key=lambda x: x['created_on'], reverse=True)
        return render(request, 'billing.html', {'orders': purchase_orders}) 

    return redirect('index') 


def getAsset(request):
    asset_id = request.GET['asset_id']
    if asset_id.isnumeric():
        assets = Asset.objects.filter(pk=asset_id)
        for asset in assets:
            return HttpResponse(asset.name)
    return HttpResponse('N/A')

def addAsset(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        asset_id_text = request.POST['assetId']
        asset_id = Asset.objects.get(pk=asset_id_text)
        qty = request.POST['qty']

        org = get_user_org(request.user)
        # check if item already there, create new only if it is not there
        try:
            stock = OrganizationStock.objects.get(org_id=org.org_id, asset_id=asset_id)
        except OrganizationStock.DoesNotExist:
            stock = OrganizationStock(org_id=org.org_id, asset_id=asset_id, qty_available=0, price_per_unit=0)

        if org.org_id.org_type == 'S':
            stock.price_per_unit = int(request.POST['price'])
        
        stock.qty_available = int(qty)
        stock.save()

    return redirect('index')