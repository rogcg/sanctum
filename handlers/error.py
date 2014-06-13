import webapp2

import view

class Error404Handler(webapp2.RequestHandler):

    def get(self):
        page = view.Page()
        page.render_error(self, 404)
