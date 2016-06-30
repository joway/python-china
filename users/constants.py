from django.utils.translation import ugettext_lazy as _

MAX_MAIL_INTERVAL_SECONDS = 60
MAX_MAIL_VALID_SECONDS = 12 * 60 * 60
ALINK_VERIFY_CODE_LENGTH = 32

# ERROR INFO
INVALID_CREDENTIALS_ERROR = _('Unable to login with provided credentials.')
INACTIVE_ACCOUNT_ERROR = _('User account is disabled.')
