import os, datetime

APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

SETTINGS = {
    'title': 'a title',
    'description': 'a cool slogan',
    # Author name or empty
    'author': '<author name>',
    # Your email or empty
    'email': '',
    # Your blog url
    'url': '',
    # The name of the theme (must match the folder name)
    'theme':'',
    # Number of items to be shown on the posts index
    'items_per_page': 10,
    # Enable/disable Google Analytics
    # Set to your tracking code (UA-xxxxxx-x), or False to disable
    'google_analytics': '',
    # Enable/disable Disqus-based commenting for posts
    # Set to your Disqus short name, or False to disable
    'disqus': '',
    # This gets the the current yeat to be display on your page,
    # so you won't need to keep updating it.
    'year': datetime.datetime.now().year
}
