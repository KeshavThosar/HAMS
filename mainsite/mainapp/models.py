from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    org_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=48)
    address = models.CharField(max_length=255)
    org_type = models.CharField(max_length=1, choices=[('H', 'Hospital'), ('S', 'Supplier')])

    def __str__(self):
        return self.org_type + '_' + self.name

class Asset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=48)
    img_url = models.URLField(default='default_logo.png')

    def __str__(self):
        return f'{self.asset_id} - {self.name}'

class OrganizationStock(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='org_id')
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE, to_field='asset_id')
    price_per_unit = models.IntegerField()
    qty_available = models.IntegerField()

    def __str__(self):
        return f'{self.org_id} | {self.asset_id} x {self.qty_available}'

class PurchaseOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    src_org_id = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, to_field='org_id', related_name='src_org_id')
    dest_org_id = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, to_field='org_id', related_name='dest_org_id')
    approval_status = models.CharField(max_length=1, choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P')
    comments = models.CharField(max_length=255, default='')
    created_on = models.DateTimeField(default=datetime.now())
    updated_on = models.DateTimeField(default=datetime.now())

class PurchaseOrderDetails(models.Model):
    order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, to_field='order_id')
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE, to_field='asset_id')
    qty = models.IntegerField()

class UserOrganization(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    org_id  = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='org_id')