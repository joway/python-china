from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

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
    return HttpResponse(access_token)


def callback(request):
    """ get the code and request for jwt token
    """
    access_token, refresh_token = AuthService.get_tokens(code=request.GET['code'])
    return HttpResponse(access_token)
