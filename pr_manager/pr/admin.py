from django.contrib import admin
from pr.models import Reteta, Account

@admin.register(Reteta)
class RetetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_accounts_nr')
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(owner=user)

    def get_fields(self, request, obj=None):
        all_fields = super().get_fields(request, obj)

        if not request.user.is_superuser:
            all_fields.remove('owner')

        return all_fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            owner = form.cleaned_data.get('owner')
            if not owner:
                obj.owner = request.user

        super().save_model(request, obj, form, change)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'reteta_name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(recipe__owner=user)
