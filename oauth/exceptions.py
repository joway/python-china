# coding=utf-8


class ApplicationNotExist(Exception):
    pass


class ClientSecretError(Exception):
    pass


class GrantNotExist(Exception):
    pass


class TokenNotExist(Exception):
    pass


class RefreshTokenError(Exception):
    pass


class TokenExpired(Exception):
    pass
