import os
from mako import exceptions
from mako.lookup import TemplateLookup
from mako.runtime import Context
from StringIO import StringIO
import tornado.ioloop
import tornado.web
from tornado import httpclient
from twisted.internet import reactor
from data_functions import get_stats

root = os.path.dirname(__file__)
template_root = os.path.join(root, 'templates')
blacklist_templates = ('layouts',)
template_lookup = TemplateLookup(input_encoding='utf-8',
                                 output_encoding='utf-8',
                                 encoding_errors='replace',
                                 directories=[template_root])

def render_template(filename, context=None):
    if os.path.isdir(os.path.join(template_root, filename)):
        filename = os.path.join(filename, 'index.html')
    else:
        filename = '%s' % filename
    if any(filename.lstrip('/').startswith(p) for p in blacklist_templates):
        raise httpclient.HTTPError(404)
    try:
        return template_lookup.get_template(filename).render_context(context)
    except exceptions.TopLevelLookupException:
        raise httpclient.HTTPError(404)

class DefaultHandler(tornado.web.RequestHandler):
    def get_error_html(self, status_code, exception, **kwargs):
        if hasattr(exception, 'code'):
            self.set_status(exception.code)
            if exception.code == 500:
                return exceptions.html_error_template().render()
            return render_template(str(exception.code))
        return exceptions.html_error_template().render()

class MainHandler(DefaultHandler):
    def get(self, filename):
        ctx_dict = {'userstats': get_stats()}
        buf = StringIO()
        ctx=Context(buf, **ctx_dict)
        self.write(render_template(filename,context=ctx))

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(str(get_stats()))