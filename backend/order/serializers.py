from rest_framework import serializers
from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    def get_details(self, obj):
        try:
            order_id = obj.pk if hasattr(obj, 'pk') else obj.id
            details = OrderDetail.objects.filter(order_id=order_id)
            return OrderDetailSerializer(details, many=True).data
        except Exception as e:
            return []

    class Meta:
        model = Order
        fields = '__all__'
