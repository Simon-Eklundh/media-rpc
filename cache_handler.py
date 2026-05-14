# Cache files
import json
import os

COVER_CACHE_FILE = "cover_cache.json"
POSTER_CACHE_FILE = "poster_cache.json"
LIBRARY_CACHE_FILE = "library_cache.json"

library_cache = {}
cover_cache = {}
poster_cache = {}


# SYSTEM UTILS
def load_caches():
    global cover_cache, poster_cache, library_cache
    if os.path.exists(COVER_CACHE_FILE):
        try:
            with open(COVER_CACHE_FILE, "r") as f:
                cover_cache = json.load(f)
        except:
            cover_cache = {}

    if os.path.exists(LIBRARY_CACHE_FILE):
        try:
            with open(LIBRARY_CACHE_FILE, "r") as f:
                library_cache = json.load(f)
        except:
            library_cache = {}  

    if os.path.exists(POSTER_CACHE_FILE):
        try:
            with open(POSTER_CACHE_FILE, "r") as f:
                poster_cache = json.load(f)
        except:
            poster_cache = {}


def get_poster_cache_key(cache_key):
    global poster_cache
    if cache_key in poster_cache:
        return poster_cache[cache_key]
    return None


def set_poster_cache_key(cache_key, value):
    global poster_cache
    poster_cache[cache_key] = value
    save_poster_cache()


def save_poster_cache():
    enforce_cache_limit(poster_cache, max_size=2000)
    try:
        with open(POSTER_CACHE_FILE, "w") as f:
            json.dump(poster_cache, f)
    except:
        pass


def save_cover_cache():
    enforce_cache_limit(cover_cache, max_size=2000)
    try:
        with open(COVER_CACHE_FILE, "w") as f:
            json.dump(cover_cache, f)
    except:
        pass


def get_cover_cache_key(cache_key):
    global cover_cache
    if cache_key in cover_cache:
        return cover_cache[cache_key]
    return None

def set_cover_cache_key(cache_key, value):
    global cover_cache
    cover_cache[cache_key] = value
    save_cover_cache()

def enforce_cache_limit(cache_dict, max_size=2000):
    while len(cache_dict) > max_size:
        oldest_key = next(iter(cache_dict))
        del cache_dict[oldest_key]


def save_library_cache():
    enforce_cache_limit(library_cache, max_size=2000)
    try:
        with open(LIBRARY_CACHE_FILE, "w") as f:
            json.dump(library_cache, f)
    except:
        pass

def get_library_cache_key(cache_key):
    global library_cache
    if cache_key in library_cache:
        return library_cache[cache_key]
    return None
def set_library_cache_key(cache_key, value):
    global library_cache
    library_cache[cache_key] = value
    save_library_cache()