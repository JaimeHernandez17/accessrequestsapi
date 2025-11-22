from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accessrequestsapi.users.api.serializers import UserSerializer


class CurrentUserView(APIView):
    """
    View that returns the information of the authenticated user.
    It only accepts the GET method.
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
