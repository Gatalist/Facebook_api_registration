from rest_framework.views import APIView
from rest_framework.response import Response

from .serialirers import UserSerializer
from facebook_users.random_user import start_task

import threading


class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        count = request.data.get('count')
        print(count)
        # start_task(count_create_user=count)
        threading.Thread(target=start_task, args=(count,)).start()
        return Response({"Start register user to Facebook"})

