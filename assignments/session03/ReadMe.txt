This mashup will get the trending topic in Seattle (in real time) and then
turn that topic into its picture representation. The output from running this
function will be twitter_flickr_mashup.html which you can open up in a web browser.

It uses 'requests' to get the html from twitter, and then 'BeautifulSoup' is
used to parse and pull out the currently trending topic on twitter for #Seattle.
That string is passed to another function, and this function will iterate
over each character in the string. For each character, it will use the Flickr API
to request the picture representation from either the "one digit", "one letter",
or "punctuation" flickr groups. Once we have a URI for each picture we build the
html and write out that html file. Just open the html file!


Directions:
# Setup virtualenv.py
$ resources/common/virtualenv.py mashupenv
 
# Activate the env:
$ path-to-env\mashupenv\Scripts\activate

$ pip install requests
$ pip install beautifulsoup4
$ pip install flickrapi

