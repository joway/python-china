from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from users.models import User
from users.services import AuthService


def redirect(request):
    """ redirect to auth server url and get the code
    """
    return HttpResponseRedirect(AuthService.get_auth_url())


@csrf_exempt
def login(request):
    """ login with code
    """
    access_token, refresh_token = AuthService.get_tokens(code=request.POST['code'])
    user_info = AuthService.get_user_info(access_token=access_token)
    try:
        user = User.objects.get(email=user_info['email'])
    except User.DoesNotExist:
        user = User.objects.create_user(email=user_info['email'],
                                        username=user_info['username'],
                                        avatar=user_info['avatar'])
    return HttpResponse(access_token)


def callback(request):
    """ get the code and request for jwt token
    """
    access_token, refresh_token = AuthService.get_tokens(code=request.GET['code'])
    return HttpResponse(access_token)
