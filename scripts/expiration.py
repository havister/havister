# scripts/expiration.py
#
# Usage:
# python manage.py runscript expiration --script-args arg_code arg_action

from decimal import Decimal

from expiration.models import Period 
from index.models import Index, Day, Expiration

def run(*args):
