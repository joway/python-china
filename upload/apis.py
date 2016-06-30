import logging

from qiniu import Auth
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from config.settings import QINIU_SECRET_KEY, QINIU_ACCESS_KEY, QINIU_CALLBACK_URL
from utils.permissions import check_permission

logger = logging.getLogger(__name__)

bucket_name = 'i2pserver'
base_url = 'https://o7kiomgt3.qnssl.com'

policy = {
    'callbackUrl': QINIU_CALLBACK_URL,
    'callbackBody': 'filename=$(fname)&key=$(key)&filesize=$(fsize)&type=$(mimeType)&hash=$(etag)'
}
q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)


# 七牛云存储支持
class UploadViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]

    @list_route(methods=['post'])
    def token(self, request, *args, **kwargs):
        """
        Get open problem detail
        """
        check_permission((IsAuthenticated,), self, request)
        token = q.upload_token(bucket_name, None, 7200, policy)
        return Response({"token": token})

    @list_route(methods=['post'])
    def callback(self, request, *args, **kwargs):
        """
        Get open problem detail
        """
        info = {
            'key': request.POST.get('key'),
            'filename': request.POST.get('filename'),
            'filesize': request.POST.get('filesize'),
            'type': request.POST.get('type'),
            'hash': request.POST.get('hash'),
        }
        logger.info(info)
        return Response({"message": "callback success"})
