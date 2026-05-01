from rest_framework import serializers
from .models import InboundRecord, InboundDetail
from unit.models import Unit
from specifications.models import Specification
import logging

logger = logging.getLogger(__name__)


class InboundDetailSerializer(serializers.ModelSerializer):
    unit_name_display = serializers.SerializerMethodField()
    specification_display = serializers.SerializerMethodField()

    def get_unit_name_display(self, obj):
        if obj.unit_id:
            try:
                return Unit.objects.get(id=obj.unit_id).unit_name
            except Unit.DoesNotExist:
                return obj.unit_name or ''
        return obj.unit_name or ''

    def get_specification_display(self, obj):
        if obj.specification:
            try:
                specs = Specification.objects.filter(spec_name=obj.specification).first()
                if specs:
                    return specs.spec_name
            except Exception:
                pass
        return obj.specification or ''

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