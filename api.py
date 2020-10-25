import requests
def get_coordinates(location):
    params = dict(
        navn=location
    )

    url = 'https://ws.geonorge.no/SKWS3Index/ssr/json/sok?'
    resp = requests.get(url=url, params=params)
    return resp.json()

def list_locations(location):
    locations = get_coordinates(location)
    hits = int(locations.get('totaltAntallTreff'))

    pretty = []

    if hits == 0:
        print('nulltreff')
        return pretty

    elif hits == 1:
        pretty.append(locations.get('stedsnavn'))

    else:
        for location in locations.get('stedsnavn'):
            pretty.append(location)
    return pretty

#Put this in conf, my dude
useragent = "skode github.com/toremalmedal/skode"

#Status codes from YR. 

#429
#Clients that dont follow TOS will be throttled and receive this instead of content. 
#Limit traffic, or check useragent.

#203
#If the version of the product is deprecated, this will be given instead of 200.
#Log and update to new version within about a month.

# https://developer.yr.no/doc/TermsOfService/
# Don't repeat requests until the time indicated in the Expires response header.
# Continous updates: Spread your traffic evenly out over time so it makes a 
# flat curve, not a sawtooth.
# Cache data locally and and use the If-Modified-Since request
#  header to avoid repeatedly downloading the same data.
# We only support encrypted HTTPS for security reasons.
# All clients must support redirects and gzip compression (Accept-Encoding: gzip, deflate) as described in RFC 2616.


#def get_basic_forecast(altitude, lat, lon):
    #Check expire time from last request, to see if we should make new request:    
    #https://api.met.no/weatherapi/locationforecast/2.0/#!/data/get_compact_format
