#!/lap/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Date-App/front-end/flaskapp")
from myapp import app as application
