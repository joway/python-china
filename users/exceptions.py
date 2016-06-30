# coding=utf-8


class EmailExist(Exception):
    pass


class PasswordError(Exception):
    pass


class UserNotExist(Exception):
    pass


class VerifyCodeError(Exception):
    pass


class VerifyTimeFrequently(Exception):
    pass


class VerifyCodeExpire(Exception):
    pass


class UserHasActivated(Exception):
    pass
