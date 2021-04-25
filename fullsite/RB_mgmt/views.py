"""
RB-mgmt module using class based views and django REST API
"""
#from rest_framework.response import Response
#from rest_framework.views import APIView
from rest_framework import generics  # , viewsets
#from django.shortcuts import render

from .models import Element, Connection, Powerplant, PowerPlantConnection
from .serializers import ElementSerializer, ConnectionSerializer, PowerPlantSerializer, PowerPlantConnectionSerializer
from django.http import JsonResponse
# Create your views here.


def hello(request):
    return JsonResponse({'response_text': 'hello world!'})


class ElementList(generics.ListCreateAPIView):
    serializer_class = ElementSerializer

    def get_queryset(self):
        el_type = self.kwargs['type']
        if el_type == 'POB':
            return Element.objects.filter(element_type=0)
        elif el_type == 'SE':
            return Element.objects.filter(element_type=1)


class ElementCreateView(generics.CreateAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


class ElementDeleteView(generics.DestroyAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


class ElementUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


class ConnList(generics.ListCreateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class ConnCreateView(generics.CreateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class ConnDeleteView(generics.DestroyAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class ConnUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class PowerPlantList(generics.ListCreateAPIView):
    queryset = Powerplant.objects.all()
    serializer_class = PowerPlantSerializer


class PowerPlantCreateView(generics.CreateAPIView):
    queryset = Powerplant.objects.all()
    serializer_class = PowerPlantSerializer


class PowerPlantDeleteView(generics.DestroyAPIView):
    queryset = Powerplant.objects.all()
    serializer_class = PowerPlantSerializer


class PowerPlantUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Powerplant.objects.all()
    serializer_class = PowerPlantSerializer


class PowerPlantConnectionList(generics.ListCreateAPIView):
    queryset = PowerPlantConnection.objects.all()
    serializer_class = PowerPlantConnectionSerializer
