from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from oauth.exceptions import ApplicationNotExist, TokenNotExist, TokenExpired
from oauth.models import Application
from oauth.serializers import ApplicationAuthSerializer, ApplicationAccessTokenSerializer, \
    ApplicationRegisterSerializer, \
    RefreshTokenSerializer, ApplicationSerializer, TokenSerializer, AccessTokenSerializer
from oauth.services import OauthService
from users.serializers import UserSerializer
from utils.permissions import check_permission


class OauthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()

    @list_route(methods=['post'])
    def register(self, request):
        """注册一个application
        """
        check_permission((IsAuthenticated,), self, request)
        serializer = ApplicationRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(data=serializer.data)

    @list_route(methods=['get'])
    def applications(self, request):
        """查询application信息
        """
        check_permission((IsAuthenticated,), self, request)
        instances = Application.objects.filter(owner=request.user)
        serializer = ApplicationSerializer(instances, many=True)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def authorize(self, request):
        """获取code
        :param:
            client_id:
            [redirect_url]:
            [scope]:
            [state]:
        Returns:
            code
        """
        check_permission((IsAuthenticated,), self, request)
        serializer = ApplicationAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            grant = OauthService.grant(serializer.data['client_id'], request.user)
        except ApplicationNotExist:
            return Response(data={'message': '应用不存在'}, status=status.HTTP_403_FORBIDDEN)
        return Response(data=grant.code)

    @list_route(methods=['post'])
    def access_token(self, request):
        """获取access_token
        :param:
            client_id:
            client_secret:
            code:
            [redirect_url]:
            [scope]:

        Returns:
            access_token, refresh_token
        """
        serializer = ApplicationAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        token = OauthService.gen_tokens(client_id=data['client_id'],
                                        client_secret=data['client_secret'],
                                        code=data['code'],
                                        redirect_url=data.get('redirect_url', None),
                                        state=data.get('state', None))

        return Response(TokenSerializer(token).data)

    @list_route(methods=['post'])
    def refresh_token(self, request):
        """刷新access_token
        :param:
            refresh_token:

        Returns:
            access_token, refresh_token
        """
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        token = OauthService.refresh_token(data['client_id'], data['client_secret'],
                                           data['refresh_token'])
        return Response(TokenSerializer(token).data)

    @list_route(methods=['post'])
    def user(self, request):
        """获取user info
        :param:
            access_token:

        Returns:
            user info
        """
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = OauthService.verify_access_token(serializer.data['access_token'])
        except TokenNotExist:
            return Response(data={'message': 'Token 无效'}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenExpired:
            return Response(data={'message': 'Token 过期'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(token.user).data)
