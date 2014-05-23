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
                                      [webapp2.Route('r/', handler='blog.IndexHandler'),
                                      webapp2.Route('r/blog/rss2', handler='blog.RSS2Handler'),
                                      webapp2.Route('r/blog/tag/<:\w+>', handler='blog.TagHandler'),
                                      webapp2.Route('r/blog/<:\d{4}+>', handler='blog.YearHandler'),
                                      webapp2.Route('r/blog/<:\d{4}+>/<:\d{2}+>', handler='blog.MonthHandler'),
                                      webapp2.Route('r/blog/<:\d{4}+>/<:\d{2}+>/<:\d{2}+>', handler='blog.DayHandler'),
                                      webapp2.Route('r/blog/<:\d{4}+>/<:\d{2}+>/<:\d{2}+>/<:\w+>', handler='blog.PostHandler'),
                                      webapp2.Route('r/admin/clear-cache', handler='admin.ClearCacheHandler'),
                                      webapp2.Route('r/admin/posts', handler='admin.ListPostsHandler'),
                                      webapp2.Route('r/admin/post/create', handler='admin.CreatePostHandler'),
                                      webapp2.Route('r/admin/post/edit/<:\d{4}+>/<:\d{2}>/<:\d{2}>/<:\w+>', handler='admin.EditPostHandler'),
                                      webapp2.Route('r/admin/post/delete/<:\d{4}+>/<:\d{2}>/<:\d{2}>/<:\w+>', handler='admin.DeletePostHandler'),
                                      webapp2.Route('r/admin/pages', handler='admin.ListPagesHandler'),
                                      webapp2.Route('r/admin/page/create', handler='admin.CreatePagesHandler'),
                                      webapp2.Route('r/admin/page/edit/<:\w+>', handler='admin.EditPagesHandler'),
                                      webapp2.Route('r/admin/page/delete/<:\w+>', handler='admin.DeletePagesHandler'),
                                      webapp2.Route('r/<:\w+>', handler='blog.PageHandler'),
                                      webapp2.Route('r/.*', handler='error.Error404Handler')], debug=True)
