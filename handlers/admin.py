import datetime
import logging
import time

from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import users

from models import blog
import view

class IndexHandler(webapp.RequestHandler):

    def get(self):
        page = view.Page()
        page.render(self, 'templates/admin/index.html')

class CreatePostHandler(webapp.RequestHandler):

    def get(self):
        page = view.Page()
        page.render(self, 'templates/admin/post_form.html')

    def post(self):
        new_post = blog.Post()
        new_post.title = self.request.get('title')
        new_post.body = self.request.get('body')

        slug = self.request.get('slug').strip()
        if slug == '':
            slug = blog.slugify(new_post.title)
        new_post.slug = slug

        excerpt = self.request.get('excerpt').strip()
        if excerpt == '':
            excerpt = None
        new_post.excerpt = excerpt

        new_post.tags = self.request.get('tags').split(',')

        if self.request.get('submit') == 'Submit':
            if new_post.put():
                # for now I use this sleep here to wait the post be created. I can't find a way to 
                # solve it. invesigate better later.
                time.sleep(2)
                self.redirect(new_post.get_absolute_url())
        else:
            new_post.populate_html_fields()
            template_values = {
                'post': new_post,
                }
            page = view.Page()
            page.render(self, 'templates/admin/post_form.html', template_values)

class ListPostsHandler(webapp.RequestHandler):

    def get(self):
        query = blog.Post.all()
        query.order('-pub_date')

        template_values = {'page_title': 'Posts'}

        page = view.Page()
        page.render_paginated_query(self, query, 'posts', 'templates/admin/posts.html', template_values)

class DeletePostHandler(webapp.RequestHandler):

    def get(self, year, month, day, slug):
        year = int(year)
        month = int(month)
        day = int(day)

        # Build the time span to check for the given slug
        start_date = datetime.datetime(year, month, day)
        time_delta = datetime.timedelta(days=1)
        end_date = start_date + time_delta

        # Create a query to check for slug uniqueness in the specified time span
        query = blog.Post.all()
        query.filter('pub_date >= ', start_date)
        query.filter('pub_date < ', end_date)
        query.filter('slug = ', slug)

        post = query.get()

        if post == None:
            page = view.Page()
            page.render_error(self, 404)
        else:
            post.delete() 

            template_values = {
                'message': 'Your post has been deleted.'
                }
            
            page = view.Page()
            page.render(self, 'templates/blog/post.html', template_values)

class EditPostHandler(webapp.RequestHandler):

    def get(self, year, month, day, slug):
        year = int(year)
        month = int(month)
        day = int(day)

        # Build the time span to check for the given slug
        start_date = datetime.datetime(year, month, day)
        time_delta = datetime.timedelta(days=1)
        end_date = start_date + time_delta

        # Create a query to check for slug uniqueness in the specified time span
        query = blog.Post.all()
        query.filter('pub_date >= ', start_date)
        query.filter('pub_date < ', end_date)
        query.filter('slug = ', slug)

        post = query.get()

        if post == None:
            page = view.Page()
            page.render_error(self, 404)
        else:
            action_url = post.get_edit_url()

            template_values = {
                'action': action_url,
                'post': post,
                }

            page = view.Page()
            page.render(self, 'templates/admin/post_form.html', template_values)

    def post(self, year, month, day, slug):
        year = int(year)
        month = int(month)
        day = int(day)

        # Build the time span to check for the given slug
        start_date = datetime.datetime(year, month, day)
        time_delta = datetime.timedelta(days=1)
        end_date = start_date + time_delta

        # Create a query to check for slug uniqueness in the specified time span
        query = blog.Post.all()
        query.filter('pub_date >= ', start_date)
        query.filter('pub_date < ', end_date)
        query.filter('slug = ', slug)

        post = query.get()

        if post == None:
            page = view.Page()
            page.render_error(self, 404)
        else:
            action_url = post.get_edit_url()
            post.title = self.request.get('title')
            post.body = self.request.get('body')

            slug = self.request.get('slug').strip()
            if slug == '':
                slug = blog.slugify(post.title)
            post.slug = slug

            excerpt = self.request.get('excerpt').strip()
            if excerpt == '':
                excerpt = None
            post.excerpt = excerpt

            post.tags = self.request.get('tags').split(',')

            if self.request.get('submit') == 'Submit':
                post.put()
                self.redirect(post.get_absolute_url())
            else:
                post.populate_html_fields()
                template_values = {
                    'action': action_url,
                    'post': post,
                }
                page = view.Page()
                page.render(self, 'templates/admin/post_form.html', template_values)

class ClearCacheHandler(webapp.RequestHandler):

    def get(self):
        memcache.flush_all()

class CreatePageHandler(webapp.RequestHandler):

    def get(self):
        page = view.Page()
        page.render(self, 'templates/admin/page_form.html')

    def post(self):
        new_page = blog.Page()
        new_page.name = self.request.get('name')
        new_page.url = self.request.get('url')
        new_page.body = self.request.get('body')

        if self.request.get('submit') == 'Submit':
            new_page.put()
            # for now I use this sleep here to wait the post be created. I can't find a way to 
            # solve it. invesigate better later.
            time.sleep(2)
            self.redirect(new_page.get_absolute_url())
        else:
            new_page.populate_html_fields()
            template_values = {
                'page': new_page,
                }
            page = view.Page()
            page.render(self, 'templates/admin/page_form.html', template_values)

class ListPagesHandler(webapp.RequestHandler):

    def get(self):
        pages = blog.Page.all()
        pages.order('-name')

        template_values = {
            'page_title': 'Pages'
            }

        page = view.Page()
        page.render_paginated_query(self, pages, 'pages', 'templates/admin/pages.html', template_values)

class EditPageHandler(webapp.RequestHandler):

    def get(self, page_url):

        page_obj = blog.Page.all().filter('url =', page_url).get()
        
        if page_obj == None:
            page = view.Page()
            page.render_error(self, 404)
        else:
            action_url = page_obj.get_edit_url()

            template_values = {
                'action': action_url,
                'page': page_obj,
                }

            page = view.Page()
            page.render(self, 'templates/admin/page_form.html', template_values)

    def post(self):
        
        # Create a query to check for slug uniqueness in the specified time span
        query = blog.About.all()
        
        post = query.get()

        if post == None:
            page = view.Page()
            page.render_error(self, 404)
        else:
            action_url = post.get_edit_url()
            post.title = self.request.get('title')
            post.body = self.request.get('body')

            if self.request.get('submit') == 'Submit':
                post.put()
                self.redirect(post.get_absolute_url())
            else:
                post.populate_html_fields()
                template_values = {
                    'action': action_url,
                    'post': post,
                }
                page = view.Page()
                page.render(self, 'templates/admin/about_form.html', template_values)

class DeletePageHandler(webapp.RequestHandler):

    def get(self, url):
        
        # Create a query to check for slug uniqueness in the specified time span
        page_obj = blog.Page.all().filter('url =', url).get()
        
        if page_obj == None:
            page = view.Page()
            page.render_error(self, 404)
        else:
            page_obj.delete()

            template_values = {
                'message': 'Your post has been deleted.'
                }
            
            page = view.Page()
            page.render(self, 'templates/blog/page.html', template_values)