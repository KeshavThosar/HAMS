from django.db import models
from django.contrib.auth.models import AbstractUser

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

class OrganizationStock(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='org_id')
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE, to_field='asset_id')
    price_per_unit = models.IntegerField()
    qty_available = models.IntegerField()

class PurchaseOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    src_org_id = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, to_field='org_id', related_name='src_org_id')
    dest_org_id = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, to_field='org_id', related_name='dest_org_id')

class PurchaseOrderDetails(models.Model):
    order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, to_field='order_id')
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE, to_field='asset_id')
    qty = models.IntegerField()

class OrganizationUser(AbstractUser):
    groups = None
    user_permissions = None
    
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='org_id', null=True, blank=True)