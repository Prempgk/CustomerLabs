from django.core.validators import MinLengthValidator
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import requests

from .serializers import *


# Create your views here.

# Api for create an account
@api_view(['POST'])
@permission_classes([AllowAny])
def create_account(request):
    inp_data = request.data
    account_serializer = AccountSerializer(data=inp_data)
    if not account_serializer.is_valid():
        return Response({"error": error(account_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    pv = PasswordCharacterValidator(min_length_lower=4, min_length_digit=2,
                                    min_length_upper=1, min_length_special=1)  # password validation
    try:
        pv.validate(request.data['password'])
        pass
    except Exception as e:
        return Response({"error": {"password": e}}, status=status.HTTP_400_BAD_REQUEST)
    account_serializer.save()
    return Response(account_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_account(request):
    login_serializer = AccountLoginSerializer(data=request.data)
    if not login_serializer.is_valid():
        return Response({"error": error(login_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    try:
        acc = Accounts.objects.get(email_id=request.data['email'])
    except:
        return Response({"error": {"email": "Account not found"}}, status=status.HTTP_404_NOT_FOUND)
    if acc.password != request.data['password']:
        return Response({"error": {"password": "Wrong password"}}, status=status.HTTP_400_BAD_REQUEST)
    headers = {
        "Access-Control-Expose-Headers": "*, Authorization",
        "CL-X-TOKEN": acc.acc_secret.hex
    }
    acc_serializer = AccountSerializer(acc)
    return Response({"message": "success!, your secret token was sent in headers name was ** CL-X-TOKEN **",
                     "account_detail": acc_serializer.data},
                    headers=headers, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_account(request):
    try:
        acc = Accounts.objects.get(acc_secret=request.headers['CL-X-TOKEN'])
    except:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if 'account_id' not in request.data:
        return Response({"error": {"account_id": "This field is required"}}, status=status.HTTP_400_BAD_REQUEST)
    try:
        inp_acc = Accounts.objects.get(account_id=request.data['account_id'])
    except:
        return Response({"error": {"account_id": "Invalid account details"}}, status=status.HTTP_400_BAD_REQUEST)
    if acc.acc_secret != inp_acc.acc_secret:
        return Response({"error": {"account_id": "Invalid account details"}}, status=status.HTTP_401_UNAUTHORIZED)
    request.data['created_at'] = inp_acc.created_at
    request.data['updated_at'] = timezone.now()
    acc_serializer = AccountSerializer(inp_acc, data=request.data)
    if not acc_serializer.is_valid():
        return Response({"error": error(acc_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    acc_serializer.save()
    return Response(acc_serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_account(request):
    try:
        acc = Accounts.objects.get(acc_secret=request.headers['CL-X-TOKEN'])
    except:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    acc.delete()
    return Response({"message": "Deleted"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def all_accounts(request):
    acc = Accounts.objects.all()
    acc_serializer = AccountSerializer(acc, many=True)
    return Response(acc_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_destination(request):
    try:
        acc = Accounts.objects.get(acc_secret=request.headers['CL-X-TOKEN'])
    except:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    request.data['account'] = acc.account_id
    dest_serializer = DestinationSerializer(data=request.data)
    if not dest_serializer.is_valid():
        return Response({"error": error(dest_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    if type(request.data['headers']) != dict:
        return Response({"error": {"headers": "Headers must be a key value pair (i.e:'JSON Format')"}},
                        status=status.HTTP_400_BAD_REQUEST)
    dest_serializer.save()
    return Response(dest_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_destination(request):
    try:
        acc = Accounts.objects.get(acc_secret=request.headers['CL-X-TOKEN'])
    except:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    destinations = Destinations.objects.filter(account=acc.account_id)
    dest_serializer = DestinationSerializer(destinations, many=True)
    return Response(dest_serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_destination(request):
    try:
        acc = Accounts.objects.get(acc_secret=request.headers['CL-X-TOKEN'])
    except:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if 'id' not in request.data:
        return Response({"error": {"id": "This field is required"}}, status=status.HTTP_400_BAD_REQUEST)
    try:
        destination = Destinations.objects.get(id=request.data['id'])
    except:
        return Response({"error": {"id": "Invalid destination"}}, status=status.HTTP_400_BAD_REQUEST)
    if destination.account != acc:
        return Response({"error": {"id": "Invalid destination"}}, status=status.HTTP_401_UNAUTHORIZED)
    request.data['account'] = acc.account_id
    request.data['created_at'] = destination.created_at
    request.data['updated_at'] = timezone.now()
    dest_serializer = DestinationSerializer(destination, data=request.data)
    if not dest_serializer.is_valid():
        return Response({"error": error(dest_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
    if type(request.data['headers']) != dict:
        return Response({"error": {"headers": "Headers must be a key value pair (i.e:'JSON Format')"}},
                        status=status.HTTP_400_BAD_REQUEST)
    dest_serializer.save()
    return Response(dest_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_destination(request):
    try:
        acc = Accounts.objects.get(acc_secret=request.headers['CL-X-TOKEN'])
    except:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if 'id' not in request.data:
        return Response({"error": {"id": "This field is required"}}, status=status.HTTP_400_BAD_REQUEST)
    if type(request.data['id']) != list:
        return Response({"error": {"id": "This field must be a list of integers(i.e: [1, 2, 3,..]"}},
                        status=status.HTTP_400_BAD_REQUEST)
    for i in request.data['id']:
        try:
            destination = Destinations.objects.get(id=i)
        except:
            return Response({"error": {i: "Invalid destination"}}, status=status.HTTP_400_BAD_REQUEST)
        if destination.account != acc:
            return Response({"error": {i: "Invalid destination"}}, status=status.HTTP_401_UNAUTHORIZED)
        destination.delete()
    return Response({"message": "Deleted"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def server_data(request):
    try:
        acc = Accounts.objects.get(acc_secret=request.headers['CL-X-TOKEN'])
    except:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    if type(request.data) != dict:
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    destinations = acc.destinations_set.all()
    if len(destinations) == 0:
        return Response({"message": "There is no destination to send the data"}, status=status.HTTP_200_OK)
    res_data = []
    for i in destinations:
        r = []
        if i.http_method == 'POST':
            r = requests.post(
                i.url, data=request.data, headers=i.headers
            )
        elif i.http_method == 'GET':
            r = requests.get(
                i.url, params=request.data, headers=i.headers
            )
        res_data.append({i.url: r.status_code})
    return Response(res_data, status=status.HTTP_200_OK)


def error(data):
    error_list = {}
    for i in data:
        for j in data.get(i):
            err = {i: j}
            error_list.update(err)
    return error_list
