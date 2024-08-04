from rest_framework import serializers
from .models import Medicine, MedicineTag
from tags.serializers import TagSerializer

class MedicineTagSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    tag = TagSerializer()
    class Meta:
        model = MedicineTag
        fields = ['id','tag']

class MedicineSerializer(serializers.ModelSerializer):
    medicine_id = serializers.IntegerField(source='id')

    class Meta:
        model = Medicine
        fields = ['medicine_id', 'name']