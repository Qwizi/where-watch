from http.client import responses
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django_q.tasks import async_task
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import Process


@api_view(['GET'])
def test(request):
    async_task('sites.tasks.run_bots')
    return Response({'msg': 'ok'})


@api_view(['POST'])
def process(request):
    serializer = Process(data=request.data)
    serializer.is_valid(raise_exception=True)
    print(serializer)
    return Response(data=serializer.data)
