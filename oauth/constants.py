class Scopes:
    Read = 'read'
    ReadWrite = 'read write'


SCOPE_CHOICES = (
    (Scopes.Read, "读"),
    (Scopes.ReadWrite, "读写"),
)


class GrantTypes:
    AUTHORIZATION_CODE = 'authorization_code'


GRANT_TYPE_CHOICES = (
    (GrantTypes.AUTHORIZATION_CODE, '授权码'),
)
