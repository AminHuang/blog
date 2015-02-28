import sae
import os
import sys

root = os.path.dirname(__file__)
sys.path.insert(2,os.path.join(root, 'site-packages'))

from views import app

application = sae.create_wsgi_app(app)