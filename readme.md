Site Builder
============

This is a relatively small script used to automatically generate plain HTML files for websites. Its goal is to replace heavier and more complex systems involving PHP or other server side scripts for simpler, mostly static websites.

This script is written in Python, and is tested with python 3.3.3. It will not work with python 2.x. It requires the "json" and "markdown" packages. Install them like this:

	pip3 install markdown
	pip3 install json

You may need to use "pip" instead of "pip3". If it still doesn't work, you may need to do:

	sudo apt-get install python3-pip

or your OS' equavilent.

This script relies on Apache's mod_rewrite to create the pretty URL structure. If you don't have mod_rewrite installed, enable it like this:

	sudo a2enmod rewrite
	sudo service apache2 restart

Documentation
-------------
Each post or page is stored in a json file like so:

	{
		"title": "display name",
		"slug": "url-name",
		"sort": sort order (number),
		"type": "page or post",
		"content": "the actual content. Make sure to escape your quotation marks!"
	} 

The "content" field should be formatted as markdown.

There are some modules you may include in your content:
* ***{allposts-full}***: show all posts in their full length [todo]
* ***{allposts-link}***: show all posts as links
