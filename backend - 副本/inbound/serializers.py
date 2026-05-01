from rest_framework import serializers
from .models import InboundRecord, InboundDetail
import logging

logger = logging.getLogger(__name__)


class InboundDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InboundDetail
        fields = '__all__'


class InboundRecordSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    def get_details(self, obj):
        try:
            inbound_id = obj.pk if hasattr(obj, 'pk') else obj.id
            details = InboundDetail.objects.filter(inbound_id=inbound_id)
            logger.info(f"Inbound {inbound_id} has {details.count()} details")
            return InboundDetailSerializer(details, many=True).data
        except Exception as e:
            logger.error(f"Error getting details for inbound {obj.id}: {e}")
            return []

    class Meta:
        model = InboundRecord
        fields = '__all__'


class InboundRecordSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InboundRecord
        fields = ['id', 'inbound_no', 'inbound_type', 'status']