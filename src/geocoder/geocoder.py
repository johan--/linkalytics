import functools

from geopy.geocoders import GoogleV3

def memoize(func):
    """
    Memoizing decorator for functions, methods, or classes, exposing
    the cache publicly.

    Currently only works on positional arguments.
    """
    cache = func.cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        if args not in cache:
            cache[args] = func(*args, **kwargs)

        return cache[args]

    return wrapper

@memoize
def get_lat_long(geocoder, query):
    """
    Get's the latitude and longitude using geopy geocoder

    Input
    =====
    geocoder: <geopy.geocoders>
        geopy geocoder instance

    query: str
        Query string
    """
    location = geocoder.geocode(query)

    return location.latitude, location.longitude


google = GoogleV3()

lat_long = functools.partial(get_lat_long, google)

def run(node):
    return {
        'city': [
            {"name": n, 
             "latitude": lat_long(n)[0], 
             "longitude": lat_long(n)[1]
            } for n in node.get('city')]
    }
