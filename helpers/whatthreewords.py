import requests

from helpers import settings


def get_coordinates_from_words(words):
    url = "https://api.what3words.com/v2/forward?addr=%s&display=full&format=json&key=%s" % (words, settings.gps.key)
    r = requests.get(url)
    result = r.json()
    return result['geometry']['lat'], result['geometry']['lng']


def get_words_from_coordinates(coordinates):
    url = "https://api.what3words.com/v2/reverse?coords=%f,%f&display=full&format=json&key=%s" % (
        coordinates[0], coordinates[1], settings.gps.key)
    r = requests.get(url)
    result = r.json()
    return result['words']


if __name__ == '__main__':
    settings.gps.key = '111'
    origin = (35.060675, -89.664574)
    words = get_words_from_coordinates(origin)
    coordinates = get_coordinates_from_words(words)
    print("origin:%s, words: %s, coordinates: %s" % (origin, words, str(coordinates)))
