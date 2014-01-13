Site Builder
============

This is a relatively small script used to automatically generate plain HTML files for websites. Its goal is to replace heavier and more complex systems involving PHP or other server side scripts for simpler, mostly static websites.

This script is written in Python, and is tested with python 3.3.3. It will not work with python 2.x. It requires the "ementtree" and "markdown" packages. Install them like this:

	pip3 install markdown
	pip3 install elementtree

You may need to use "pip" instead of "pip3". If it still doesn't work, you may need to do:

	sudo apt-get install python3-pip

or your OS' equavilent.

This script relies on Apache's mod_rewrite to create the pretty URL structure. If you don't have mod_rewrite installed, enable it like this:

	sudo a2enmod rewrite
	sudo service apache2 restart

Alternatively, you can set the "mod_rewrite" option to "false" if you don't use apache, or for some reason can't use mod_rewrite. The only difference is that it will append a ".html" to all your links.

Documentation
-------------
Each post or page is stored in an xml file like so:

	<entry>
		<title>display name</title>
		<slug>url name, http://example.com/[slug]</slug>
		<sort>sort number</sort>
		<type>page or post</type>
		<content>the actual content, formatted with markdown</content> 
	</entry>

There are some modules you may include in your content:
* ***{allposts-full}***: show all posts in their full length [todo]
* ***{allposts-link}***: show all posts as links
