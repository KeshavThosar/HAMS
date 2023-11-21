from django.contrib import admin
from .models import *

admin.site.register([
    Asset,
    PurchaseOrder,
    PurchaseOrderDetails,
    Organization,
    OrganizationStock,
    UserOrganization,
])
