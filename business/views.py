from django.shortcuts import render
from accounts.models import User
from business.models import Business,Location,Area,OperatingHours
from business.serializers import BusinessSerializer,LocationSerializer
from rest_framework import (
    viewsets, views,
    status, permissions
    )
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes

# Create your views here.
@authentication_classes([])
@permission_classes([])
class BusinessRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    # def perform_create(self, serializer):
    #     return serializer.save(user = self.request.user)


class BusinessLocation(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def update(self, request, *args, **kwargs):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            print(instance)
            area_list = request.data.get('area')

            # iterate over each dictionary in the list and update it
            for item in area_list:
                # item_instance = Area.objects.get(area_of_work=item['area_of_work'])
                physical_address = item['physical_address']
                area_of_work = item['area_of_work']
                address = item['address']

                Area.objects.create(physical_address=physical_address,area_of_work=area_of_work,address=address)

            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            print(serializer.is_valid())
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
    

class CopySettings(APIView):
     def post(self, request):
        source_id = request.data.get('source_id')
        print(source_id)
        destination_ids = request.data.get('destination_ids')
        print(destination_ids)

        operating_hours = OperatingHours.objects.get(id=source_id)
        for id in destination_ids:
            destination = Location.objects.get(id)
            destination.operating_hours = operating_hours
        
            return destination