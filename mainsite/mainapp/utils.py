from .models import UserOrganization, OrganizationStock

def get_user_org(user):
    org = UserOrganization.objects.get(id=user.id)
    return org 

def get_org_assets(org):
    assets = OrganizationStock.objects.filter(org_id=org.org_id)
    return assets


def create_purchase_order(): pass # used by hospital
def update_purchase_order(): pass # used by supplier



 