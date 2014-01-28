import requests
from bs4 import BeautifulSoup
import flickrapi
import urllib

FLICKR_KEY = "44c4663f3b23213103952885bfbf8f01"
FLICKR_SECRET = "eca8bd05ac0d69e4"

HTML_TEMPLATE='''
<head></head>
<body>

%s

</body>'''


def get_trending_in_seattle():
    """Get the latest trending topic on twitter in Seattle"""

    url = "https://twitter.com/TrendsSeattle"
    response = requests.get(url)
    
    parsed = BeautifulSoup(response.content)
    tweet_class = "js-tweet-text tweet-text"
    latest_tweet = parsed.find('p', class_=tweet_class)

    # This is sorta hackish but but when a twitter topic is trending
    # (e.g. #<whatever>), then the first <a><b> element contains that topic.
    # When a word or phrase is trending on twitter, then #Seattle is the
    # first <a><b> element.
    if latest_tweet.b.string != "Seattle":
        # A '#<whatever>' topic is now trending.
        trending = "#" + latest_tweet.b.string
    
    else:
        # The trending topic is a word or phrase.
        trending = latest_tweet.next_element 
        if 'is now trending in' in trending:
            # The trending topic is a string
            end = trending.index('is now trending in')
            trending = trending[:end]
            trending = trending.strip()
    
            trending = urllib.unquote(trending).decode('utf8')
            trending = trending.replace("'","")
    print "Trending on twitter in Seattle: %s" % trending
    return trending


def text_to_pictures(trending):
    """This function takes an input string and returns a list of pictures. Each
    picture is a letter"""
    
    flickr = flickrapi.FlickrAPI(FLICKR_KEY)
    
    url_list = []
    
    # Build up a list of URLs, one for each character.
    for char in trending:

        if char.isdigit():
            # For numbers 0-9. The group id for the 'one digit' flickr group
            group_id = "54718308@N00"
            
        elif char.isalpha():
            # For letters a-z. The group id for the 'one letter' flickr group
            group_id = "27034531@N00"
            
        else:
            # For punctuation symbols. The group id for the 'punctuation' flickr group
            group_id = "34231816@N00"
        
        # Use the flickr api to make a request using the group id, and only requesting one image.
        digit = flickr.groups_pools_getPhotos(group_id=group_id, tags=char, per_page='1', page='1')
            
        for photos in digit:
            for photo in photos:
                url = '<img src="'+"http://farm%s.static.flickr.com/%s/%s_%s_m.jpg" % (photo.attrib['farm'], photo.attrib['server'], photo.attrib['id'], photo.attrib['secret']) +'" />'
                url_list.append(url)
                break
                    
    html = HTML_TEMPLATE % ''.join(url_list)

    # Create the html page.
    with open("twitter_flickr_mashup.html", 'w') as f:
        f.write(html)


def main():
        
    # Get the latest real time topic trending in Seattle on twitter.
    trending_now = get_trending_in_seattle()

    # Use the Flickr api to turn the text based trending topic into pictures.
    text_to_pictures(trending_now)
    
    
if __name__ == '__main__':
    main()
    