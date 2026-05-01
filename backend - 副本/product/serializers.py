from rest_framework import serializers
from .models import ProductCategory, Product, Supplier


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    image_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def get_category_name(self, obj):
        try:
            if obj.category_id:
                category = ProductCategory.objects.get(id=obj.category_id)
                return category.category_name
        except ProductCategory.DoesNotExist:
            pass
        return ''

    class Meta:
        model = Product
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'