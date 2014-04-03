import datetime
import config
import PyRSS2Gen
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from models import blog

import config
import view

# The theme used by the template configured in config.py
THEME = config.SETTINGS['theme']

class IndexHandler(webapp.RequestHandler):

    def get(self):
        query = blog.Post.all()
        query.order('-pub_date')

        user = users.get_current_user()

        # Retrieve all pages registered on datastore
        # to list on the page
        pages = blog.Page.all()

        template_values = {
            'pages':pages
        }

        page = view.Page()

        path = 'templates/%s/blog/index.html' % THEME

        page.render_paginated_query(self, query, 'posts', path, template_values)

class PostHandler(webapp.RequestHandler):

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
            template_values = {
                'post': post
                }

            page = view.Page()

            path = 'templates/%s/blog/post.html' % THEME

            page.render(self, path, template_values)

class TagHandler(webapp.RequestHandler):
    def get(self, tag):
        query = blog.Post.all()
        query.filter('tags = ', tag)
        query.order('-pub_date')

        template_values = {'page_title': 'Posts tagged "%s"' % (tag),
                           'page_description': 'Posts tagged "%s"' % (tag),
                          }

        page = view.Page()

        path = 'templates/%s/blog/index.html' % THEME

        page.render_paginated_query(self, query, 'posts', path, template_values)

class YearHandler(webapp.RequestHandler):

    def get(self, year):
        year = int(year)

        # Build the time span to check for posts
        start_date = datetime.datetime(year, 1, 1)
        end_date = datetime.datetime(year + 1, 1, 1)

        # Create a query to find posts in the given time span
        query = blog.Post.all()
        query.filter('pub_date >= ', start_date)
        query.filter('pub_date < ', end_date)
        query.order('-pub_date')

        template_values = {'page_title': 'Yearly Post Archive: %d' % (year),
                           'page_description': 'Yearly Post Archive: %d' % (year),
                          }

        page = view.Page()

        path = 'templates/%s/blog/index.html' % THEME

        page.render_paginated_query(self, query, 'posts', path, template_values)

class MonthHandler(webapp.RequestHandler):

    def get(self, year, month):
        year = int(year)
        month = int(month)

        # Build the time span to check for posts
        start_date = datetime.datetime(year, month, 1)
        end_year = year if month < 12 else year + 1
        end_month = month + 1 if month < 12 else 1
        end_date = datetime.datetime(end_year, end_month, 1)

        # Create a query to find posts in the given time span
        query = blog.Post.all()
        query.filter('pub_date >= ', start_date)
        query.filter('pub_date < ', end_date)
        query.order('-pub_date')

        month_text = start_date.strftime('%B %Y')
        template_values = {'page_title': 'Monthly Post Archive: %s' % (month_text),
                           'page_description': 'Monthly Post Archive: %s' % (month_text),
                          }

        page = view.Page()

        path = 'templates/%s/blog/index.html' % THEME

        page.render_paginated_query(self, query, 'posts', path, template_values)

class DayHandler(webapp.RequestHandler):

    def get(self, year, month, day):
        year = int(year)
        month = int(month)
        day = int(day)

        # Build the time span to check for posts
        start_date = datetime.datetime(year, month, day)
        time_delta = datetime.timedelta(days=1)
        end_date = start_date + time_delta

        # Create a query to find posts in the given time span
        query = blog.Post.all()
        query.filter('pub_date >= ', start_date)
        query.filter('pub_date < ', end_date)
        query.order('-pub_date')

        day_text = start_date.strftime('%x')
        template_values = {'page_title': 'Daily Post Archive: %s' % (day_text),
                           'page_description': 'Daily Post Archive: %s' % (day_text),
                          }

        page = view.Page()

        path = 'templates/%s/blog/index.html' % THEME

        page.render_paginated_query(self, query, 'posts', path, template_values)

class RSS2Handler(webapp.RequestHandler):

    def get(self):
        
        query = blog.Post.all()
        query.order('-pub_date')
        posts = query.fetch(10)

        rss_items = []
        for post in posts:
            item = PyRSS2Gen.RSSItem(title=post.title,
                                     link="%s%s" % (config.SETTINGS['url'], post.get_absolute_url()),
                                     description=post.excerpt_html or post.body_html,
                                     guid=PyRSS2Gen.Guid("%s%s" % (config.SETTINGS['url'], post.get_absolute_url())),
                                     pubDate=post.pub_date
                                    )
            rss_items.append(item)

        rss = PyRSS2Gen.RSS2(title=config.SETTINGS['title'],
                             link=config.SETTINGS['url'],
                             description=config.SETTINGS['description'],
                             lastBuildDate=datetime.datetime.now(),
                             items=rss_items
                            )
        rss_xml = rss.to_xml()
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss_xml)

class PageHandler(webapp.RequestHandler):

    def get(self, page_url):
        
        # Retrieve a page based on its url
        page_obj = blog.Page.all().filter('url =', page_url).get()
        
        template_values = {}

        if page_obj == None:
            page = view.Page()
            page.render_error(self, 404)
        else:
            template_values = {
                'page': page_obj
            }

        page = view.Page()

        path = 'templates/%s/blog/page.html' % THEME

        page.render(self, path, template_values)
