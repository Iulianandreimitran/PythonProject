from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from pr.models import Reteta, Account

AuthUserModel = get_user_model()

def get_permissions():
    generic_permissions = {"view", "add", "change", "delete"}
    model_names = {Reteta.__name__.lower(), Account.__name__.lower()}
    permissions = set()

    for model_name in model_names:
        for generic_permission in generic_permissions:
            permissions.add(f'{generic_permission}_{model_name}')

    return permissions

class Command(BaseCommand):
    help = "Give all the staff users the permissions to Reteta and Account models"

    def handle(self, *args, **options):
        try:
            reteta_permissions = get_permissions()
            db_permissions = Permission.objects.filter(codename__in=reteta_permissions)

            staff_users = AuthUserModel.objects.filter(is_superuser=False, is_staff=True).all()
            for user in staff_users:
                for db_permission in db_permissions:
                    user.user_permissions.add(db_permission)

        except BaseException as e:
            raise CommandError(e)