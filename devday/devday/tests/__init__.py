import logging
from django.utils import translation

# FIXME this should be in a central location for all tests, not randomly in
# one of the modules.
logging.disable(logging.CRITICAL)

translation.activate('en')
