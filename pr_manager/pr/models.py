from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reteta(MyModel):
    class Meta:
        db_table = 'retete'

    name = models.CharField(max_length=255, unique=True, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, default=1)
    accounts = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Account', related_name='accounts')
    ingredients = models.TextField(unique=False, null=False, default='sare')
    text = models.TextField(unique=False, null=False, default='nimic')
    timp = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def get_accounts_nr(self):
        return self.accounts.count()

    get_accounts_nr.short_description = 'Accounts No.'

    def __str__(self):
        return self.name


class Account(MyModel):
    class Meta:
        db_table = 'accounts'

    recipe = models.ForeignKey(Reteta, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def first_name(self):
        return self.user.first_name

    first_name.short_description = 'First Name'
    first_name.admin_order_field = 'user__first_name'

    def last_name(self):
        return self.user.last_name

    last_name.short_description = 'Last name'
    last_name.admin_order_field = 'user__last_name'

    def last_name(self):
        return self.user.last_name

    last_name.short_description = 'Last name'
    last_name.admin_order_field = 'user__last_name'

    def reteta_name(self):
        return self.recipe.name

    reteta_name.short_description = 'Reteta'
    reteta_name.admin_order_field = 'reteta__name'

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)