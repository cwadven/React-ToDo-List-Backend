import re
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _

@deconstructible
class NewASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[\w\\]+$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers,'
    )