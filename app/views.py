from django.http import request, response
from django.http.response import Http404  # for bad request
from django.shortcuts import get_object_or_404, render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView  # view set to send data in api form
# used to return response of a API class
from rest_framework.response import Response
from rest_framework import status  # for response status
from rest_framework import viewsets  # for viewsets.read-only viewsets
# authenticating a user using username and password
from django.contrib.auth import authenticate
# to add filters in a read only viewset
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.

from .models import *
from .serializers import *

class registerUser(APIView):
  def post(self,request,format=None):
    data = request.data
    user = User.objects.create_user(data["username"], data["email"], data["password"])
    user.name = data["name"]
    user.is_industry = data["is_industry"] 
    user.phone = data["phone"]
    user.location = data["location"]
    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)

class login(APIView):
  def post(self,request):
    data = request.data
    username = data['username']
    password = data['password'] 
    user = authenticate(username = username,password = password)
    if user is not None:
      serializer = UserSerializer(user)
      return Response(serializer.data)
    return Response({"Error":"invalid credentials"},status = status.HTTP_400_BAD_REQUEST)   

class UserViewset(APIView):
  
  def get_object(self,pk):
    try:
      return User.objects.get(pk=pk)
    except User.DoesNotExist:
      raise Http404
  
  def get(self,request,pk):
    user = self.get_object(pk)
    Serializer = UserSerializer(user)
    return Response(Serializer.data)

  def put(self,request,pk):
    user = self.get_object(pk)
    serializer = AddUser(user,data = request.data,partial= True)
    if serializer.is_valid():
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  def delete(self,request,pk):
    user = self.get_object(pk)
    user.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)

class NewMachinesViewset(APIView):
  def post(self,request):
    serializer = MachineSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MachineViewset(APIView):
  def get_object(self,pk):
    try:
      return Machine.objects.get(pk=pk)
    except Machine.DoesNotExist:
      raise Http404
  
  def get(self,request,pk):
    machine = self.get_object(pk)
    serializer = MachineSerializer(machine)
    return Response(serializer.data)
  
  def put(self,request,pk):
    machine = self.get_object(pk)
    serializer = MachineSerializer(machine ,data=request.data,partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self,request,pk):
    user = self.get_object(pk)
    user.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)

class Machinelist(viewsets.ReadOnlyModelViewSet):

  model = Machine
  serializer_class = MachineSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
  filterset_fields = ['industry__location', 'discount','name']
  search_fields = ('name','industry__name')

  def get_queryset(self):
    machines = Machine.objects.all()
    return machines

