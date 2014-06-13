#!/usr/bin/env python
#

import webapp2
import config
import os
import sys
import cgi


# Force sys.path to have our own directory first, so we can import from it.
sys.path.insert(0, config.APP_ROOT_DIR)
sys.path.insert(1, os.path.join(config.APP_ROOT_DIR, 'externals'))

import wsgiref.handlers

from handlers import blog, admin, error

app = webapp2.WSGIApplication(
                                [('/', blog.IndexHandler),
                                ('/blog/rss2', blog.RSS2Handler),
                                ('/blog/tag/<:\w+>', blog.TagHandler),
                                ('/blog/<:\d{4}+>', blog.YearHandler),
                                ('/blog/<:\d{4}+>/<:\d{2}+>', blog.MonthHandler),
                                ('/blog/<:\d{4}+>/<:\d{2}+>/<:\d{2}+>', blog.DayHandler),
                                ('/blog/<:\d{4}+>/<:\d{2}+>/<:\d{2}+>/<:\w+>', blog.PostHandler),
                                ('/admin/clear-cache', admin.ClearCacheHandler),
                                ('/admin/posts', admin.ListPostsHandler),
                                ('/admin/post/create', admin.CreatePostHandler),
                                ('/admin/post/edit/<:\d{4}+>/<:\d{2}>/<:\d{2}>/<:\w+>', admin.EditPostHandler),
                                ('/admin/post/delete/<:\d{4}+>/<:\d{2}>/<:\d{2}>/<:\w+>', admin.DeletePostHandler),
                                ('/admin/pages', admin.ListPagesHandler),
                                ('/admin/page/create', admin.CreatePageHandler),
                                ('/admin/page/edit/<:\w+>', admin.EditPageHandler),
                                ('/admin/page/delete/<:\w+>', admin.DeletePageHandler),
                                ('/<:\w+>', blog.PageHandler),
                                ('/.*', error.Error404Handler)], debug=True)
