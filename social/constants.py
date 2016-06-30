from .social_oauth import GithubSocialOauth, QQSocialOauth, CodingSocialOauth


class Providers:
    Github = 'github'
    QQ = 'qq'
    Coding = 'coding'


PROVIDERS_CHOICES = (
    (Providers.Github, "Github"),
    (Providers.QQ, "QQ"),
    (Providers.Coding, "Coding"),
)

SOCIAL_OAUTH_URLS = {
    'github': GithubSocialOauth.get_auth_url(),
    'qq': QQSocialOauth.get_auth_url(),
    'coding': CodingSocialOauth.get_auth_url()
}
