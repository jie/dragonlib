import jinja2
import tornado.web
from .jinja_loader import Jinja2Loader


class CoreApplication(tornado.web.Application):

    def __init__(self, handlers=None, default_host="", transforms=None, **settings):
        template_path = settings.get('template_path')
        if template_path:
            jinja2_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(template_path), autoescape=False)
            jinja2_env.add_extension('jinja2.ext.do')
            jinja2_loader = Jinja2Loader(jinja2_env)
            settings.update(template_loader=jinja2_loader)
        super(CoreApplication, self).__init__(
            handlers, default_host, transforms, **settings)
