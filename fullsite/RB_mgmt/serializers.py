"""
Models serializers for RB_mgmt app
"""
from rest_framework import serializers
from RB_mgmt.models import Element, Connection, Powerplant, PowerPlantConnection


class ElementSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """Element model serializer"""

    class Meta:
        """Meta data for model"""
        model = Element
        fields = ['pk', 'code', 'name', 'dt_from', 'dt_to',
                  'element_type', 'author', 'modified_by']


class ConnectionSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """Connection model serializer"""
    POB_code = serializers.CharField(
        source='POB.code', read_only=True)
    SE_code = serializers.CharField(
        source='SE.code', read_only=True)

    class Meta:
        """Meta data for model"""
        model = Connection
        fields = ['pk', 'POB', 'SE', 'POB_code', 'SE_code', 'dt_from',
                  'dt_to', 'author', 'modified_by']


class PowerPlantSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """Powerplant model serializer"""

    class Meta:
        """Meta data for model"""
        model = Powerplant
        fields = ['pk', 'name', 'PPE', 'POB', 'dt_from',
                  'dt_to', 'author', 'modified_by', 'is_added', 'element_type']


class PowerPlantConnectionSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """Powerplant model serializer"""
    POB_code = serializers.CharField(
        source='POB.code', read_only=True)

    class Meta:
        """Meta data for model"""
        model = PowerPlantConnection
        fields = ['pk', 'POB', 'POB_code', 'PowerPlantItem', 'dt_from', 'dt_to', 'created',
                  'author', 'modified', 'modified_by', 'element_type']
