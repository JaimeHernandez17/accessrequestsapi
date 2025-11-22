from rest_framework import serializers
from accessrequestsapi.access_control.models import System, AccessRequest
from accessrequestsapi.users.api.serializers import UserSerializer

class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ['id', 'name', 'code', 'criticality']

class AccessRequestSerializer(serializers.ModelSerializer):
    requester = UserSerializer(read_only=True)
    system_details = SystemSerializer(source='system', read_only=True)
    acted_by = UserSerializer(read_only=True)

    class Meta:
        model = AccessRequest
        fields = [
            'id', 'requester', 'system', 'system_details', 'reason', 
            'status', 'created_at', 'updated_at', 'acted_by', 'acted_at'
        ]
        read_only_fields = ['id', 'requester', 'status', 'created_at', 'updated_at', 'acted_by', 'acted_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['requester'] = request.user
        return super().create(validated_data)
