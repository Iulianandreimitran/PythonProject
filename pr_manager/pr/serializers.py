from rest_framework import serializers
from .models import Reteta
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reteta
        fields = ["name", "accounts", "ingredients", "owner" , "text", "timp", 'created_at' ]