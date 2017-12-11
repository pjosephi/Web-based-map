# Web-based-map
Project Milestone (Final)

We generated 2 files - index.html(which has the list of keywords) and
inventor.html (which is the list of inventors)

On clicking on any keyword in the index.html file you will be
directed to another html file titled keyword.html which 
contains all the application name(s), application number(s), and inventor(s)


Clicking on the inventors name will  direct you to the an html page titled inventorname.html and this page lists all the application the inventor is a part of 


Similarly, on clicking on any authors name  you will be directed to html file
titled - author.html, which contains  all patent application numbers and names for every patent application that the inventor is linked to.


Packages to install :

BeautifulSoup 

	sudo pip3 install BeautifulSoup4
	sudo pip3 install bs4

requests
	pip install requests

re

	don’t need to install

nltk

	Type python in the command line
	A window will pop up
	Copy and  paste the following in the  command line

	import nltk
	import ssl

	try:
   	 _create_unverified_https_context = ssl._create_unverified_context
	except AttributeError:
    		pass
	else:
  	  ssl._create_default_https_context = _create_unverified_https_context

	nltk.download()

	Then download all

csv
  	no need to install
math
	
	no need to install
