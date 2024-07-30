from django.shortcuts import render

from django.shortcuts import render

import os
import base64
import json

import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Tag
from medicines.models import MedicineTag, Medicine
from .serializers import TagRequestSerializer, TagSerializer


@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([AllowAny])
def tags_access(request):
    if request.method == 'POST':
        newTag = Tag.objects.create(content=request.data.get('content'))
        serializer = TagSerializer(newTag)
        return Response(serializer.data)
    elif request.method == 'GET':
        medicine_name = request.query_params.get('medicine-name')
        if not medicine_name:
            return Response({"error": "Medicine name is required."}, status=400)
        id = Medicine.objects.get(name=medicine_name)
        medicine_tags = MedicineTag.objects.filter(user=request.user, medicine=id)
        tags = set([medicine_tag.tag for medicine_tag in medicine_tags] + list(Tag.objects.filter(id__in=range(1, 11))))
        
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        medicine = Medicine.objects.get(name=request.query_params.get('medicine-name'))
        tag = Tag.objects.get(content=request.query_params.get('content'))
        MedicineTag.objects.get(medicine=medicine, tag=tag).delete()
        return Response({"detail": "태그를 삭제했습니다."}, status=status.HTTP_204_NO_CONTENT)