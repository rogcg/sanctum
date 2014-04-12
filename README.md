sanctum <img src="/static/img/favicon.png" width="50" alt="sanctum logo" />
=======

Sanctum is a blog engine for Google App Engine, using webapp and some django templates based on [joeyb-blog](https://github.com/joeyb/joeyb-blog).

Licensed under MIT License

#### Features

* Support for page creation;
* Support for post creation, edit and delete;
* Support for themes;
* Texts can be formatted using markdown or html;
* Represent post with tags, separated by commas;
* Support for disqus comments on your posts.
* RSS feed;

#### Authentication

The authentication is made using [GAE's User Service](https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingusers), so, the application must be deployed to an App Engine account registered with your email, so, you only need to login with your google account and you are authenticated. Other emails won't have access to the administration page.

##### Accessing the Administration Page

All administration pages are under the admin route:

* `yourdomain.appspot.com/admin/posts`
* `yourdomain.appspot.com/admin/post/create`
* `yourdomain.appspot.com/admin/pages`
* `yourdomain.appspot.com/admin/page/create`

#### Sanctum's directory hierarchy

As you can see, the engine itself has multiple folders, they are explained here:

* `externals` all plugins and other libraries used by the python application.
* `handlers` the handlers of the application, that deals with blog execution and also admin. The main implementation of the blog are in side this folder.
* `models` this is where the model for each entity in application is defined, like Blog, Page, Post, etc, also some rules for each specific entity, in their respective files.
* `static` this is where the engine's static files resides. Engine's purpose only.
* `templates` all your themes must live inside this folder. For more information on creating a custom theme, see the **Creating Custom Themes** section.

Now there are some files in the root of the application that deserve some attention, they are:

* `app.yaml` as a GAE developer, you must know what this file is. HEHEHEH
* `config.py` the configuration of the blog lives inside this file. For more information read the **Configuration** section.
* `main.py` in this file, the routes of the blog engine is defined.
* `view.py` this file handles the rendering of the pages, handling the theme name, etc.

#### Creating custom themes

Currently, _sanctum_ has two themes by default, **genesis** and **simple**, but you can create your own.

**IF YOU ARE GOING TO CREATE A NEW THEME, FOLLOW THOSE LAYOUTS CODE, THERE ARE SOME DJANGO TAGS THAT YOU MUST RESPECT THE NAMES.**

To create a custom theme, you must create a folder inside the `templates` directory, with the name of your theme. Each theme must have the same directory hierarchy, as you can see in themes `genesis` and `simple`, they both have the same hierarchy, **the hierarchy must follow this rule**:

    +-- theme_folder
        +-- admin
            -- base.html
            -- index.html
            -- page_form.html
            -- pages.html
            -- post_form.html
            -- posts.html
        +--blog
            -- base.html
            -- index.html
            -- page.html
            -- post.html
        +--error
            -- base.html
            -- 404.html
        +--res 
            +-- css
            +-- img
            +-- js

###### Folders explanation

* `admin` folder contains the layouts for the blog admin, where you can create new posts and pages and manage it. 
* `blog` folder contains the layouts for the blog itself, the page that is shown to the reader.
* `error` folder that contains the html error pages.
* `res` all static resources for the template must be inside this folder, css, img and js, also, if you want to use other plugins or libraries, like the default templates use bootstrap, they all reside inside this folder.

##### Django templates

You must obbey these django templates in order to present the correct information on the page.

###### Blocks

* `{% block meta_keywords  %}{% endblock %}` place the meta keywords in your html files.
* `{% block title %}{% endblock %}` place the title of your page inside this block. This block goes in the the html <head><title></title></head> tag.
* `{% block content %}{% endblock %}` all the content of your page must go inside this block. E.g.: in your `base.html`, to load the content of the **index.html**.
* `{% block menu %}{% endblock %}` the menu shown in your page. In this blog, the options like, _Home_, _My Account_, _Logout_ and other pages you create, are shown inside this block.
* `{% block pages %}{%endblock%}` this block goes inside the `{% block menu %}` block, it will load the pages you created inside the menu block and present it correctly in your page.
* `{% block sidebar %}{% endblock %}` in case you want to use a sidebar, it must live inside this block.
* `{% block footer %}{% endblock %}` the name is self obvious. Your footer goes inside this block.

###### Variables

You may access content on your html pages by using these variables.

- `{{ settings.attr_name }}` If you want to access the values set in the `config.py`, where **attr_name** is one of those attributes from config.py.
- `{{ user }}` the information of the current user logged.
- `{{ pages }}` a list with all the pages retrieved from datastore.
- `{{ page }}` the page object loaded by django on the template, this way you may access the Page model attributes:
 - `{{ page.name }}` the name of the page. It will be shown accross the whole application.
 - `{{ page.url }}` the url of the page, from where the users might reach it.
 - `{{ page.body }}` the content of the page without html tags.
 - `{{ page.body_html }}` the content of the page with html tags.
- `{{ posts }}` a list of posts retrieved from datastore. You can fetch this list and get a single post object, where you can access its attributes.
- `{{ post }}` a specific post retrieved from datastore, where you can access its attributes.
 - `{{ post.title }}` the title of the post
 - `{{ post.slug }}` the slug of the post. It's a unique value.
 - `{{ post.tags }}` a list of tags representing the post. You can fetch this list and retrieve single tags from it.
 - `{{ post.excerpt }}` the excerpt of the post without html tags.
 - `{{ post.excerpt_html }}` the excerpt of the post with html tags.
 - `{{ post.body }}` the body of the post without html tags.
 - `{{ post.body_html }}` the body of the post with html tags.
 - `{{ post.pub_date }}` the date the post has been published.
- `{{ prev_offset }}` offset for previous page on posts list.
- `{{ next_offset }}` offset for next page on posts list.
- `{{ tag_list }}` a list of tags retrieve from the post.
- `{{ tag_obj }}` when you fetch a tag list with a for loop, a tag object is retrieved from the `tag_list` tag, which you can access its specific attributes.
 - `{{ tag_obj.tag }}` the name of the tag, the label you defined for it on the creation of your post.
 - `{{ tag_obj.count }}` the amount of posts that uses this tag.
 - `{{ tag_obj.url }}` the url of the tag, which you can link to, and retrieve all posts in this tag.
- `{{ archive_list }}` a list of months with archives.
- `{{ archive_obj }}` when you fetch the `archive_list` with a for loop, an achive object is retrieved, and you can access its attributes.
 - `{{ archive_obj.url }}` the url of the archive, which you can link to, and get all posts from that epoch.
 - `{{ archive_obj.count }}` the amount of posts on that epoch.
 - `{{ archive_obj.date }}` the date of the archive, which you can format and present to the user in a friendly format.


#### Switching themes

When you have a new theme on your blog living inside the `templates` directory and following the previous rules, then you are ready to use it. If you want to switch to your new theme follow these steps:

1. In the `config.py`, change the value of the `theme` option to the name of your theme folder (**THE NAME MUST BE EXACTLY THE SAME**)
2. In the `app.yaml` inside the `handlers` option, the first rule defines the theme `res` files location, and you must change the `<theme-name>` to the name of your them directory (**THE NAME MUST BE EXACTLY THE SAME**), so you will find a rule like this in line 9:

        - url: /res
          static_dir: templates/theme_name/res

Change the **theme_name** to your theme directory name.


> I know, I must work on this better, so it will detect the tempalte folder automatically, but for now it works like that.


#### Configuration

When you download the application, there are a few options you must configure before uploading it to your App Engine account. They are set in the `config.py` file and are self explanatory, but I'm gonna mention them here too:

* `title` a title for your page that will be shown across the whole blog.
* `description` a description for your blog, it can be a quote, a slogan, anything you want. It will be shown on the header and other pages.
* `author` the name of the author to be shown on the posts.
* `email` your email, to be shown as a contact, but you can leave this empty if you want.
* `url` the url of your blog. You can leave this empty, but sometimes it's needed when using google analytics, or other references to your blog using the url.
* `meta_description` meta description content to be added to the html file.
* `theme` the name of the theme being used. The name here must be exactly the same as the theme folder inside `templates` directory.
* `items_per_page` amount of items to be shown on the posts list on the index page.
* `google_analytics` if you want to use google analytics with your blog, set your tracking code (UA-xxxxxx-x) or False to disable it.
* `disqus` if you want to use disqus comments on your blog, just set your disqus username of False to disable it. The theme `genesis` contains a disqus comment implemented.

**Please consider leaving the "Powered by _sanctum_" label on bottom of your page, as an act of recognisiment for this work.**
`<span><i>powered by <a href="{{ settings.sanctum_url }}">sanctum</a></i> <img src="/favicon.ico" width="30"></span>`
