import requests

from helpers import settings


def get_coordinates_from_words(words):
    url = "https://api.what3words.com/v2/forward?addr=%s&display=full&format=json&key=%s" % (words, settings.gps.key)
    try:
        r = requests.get(url)
        result = r.json()
        return result['geometry']['lat'], result['geometry']['lng']
    except Exception:
        return 0.0, 0.0


def get_words_from_coordinates(coordinates):
    url = "https://api.what3words.com/v2/reverse?coords=%f,%f&display=full&format=json&key=%s" % (
        coordinates[0], coordinates[1], settings.gps.key)
    try:
        r = requests.get(url)
        result = r.json()
        return result['words']
    except Exception:
        return 'd.e.f'


if __name__ == '__main__':
    origin = (35.082241, -89.652481)
    words = get_words_from_coordinates(origin)
    coordinates = get_coordinates_from_words(words)
    print("origin:%s, words: %s, coordinates: %s" % (origin, words, str(coordinates)))
