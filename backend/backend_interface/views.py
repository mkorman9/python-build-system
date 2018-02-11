import logging
import random

import os

import redis
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)


@api_view(['GET'])
def go_to(request, key, format=None):
    try:
        url = _retrieve_url_by_key(key)
        if not url:
            return JsonResponse(status=404, data={
                'error': 'key not found'
            })
    except Exception as e:
        logger.error('exception encountered while retrieving url: {}'.format(e))

        return JsonResponse(status=500, data={
            'error': 'server error'
        })

    return HttpResponseRedirect(redirect_to=url)


@api_view(['GET'])
def shorten(request, format=None):
    url = request.GET['url']
    if not url:
        return JsonResponse(status=400, data={
            'error': 'missing url parameter'
        })

    if not _is_url_valid(url):
        return JsonResponse(status=400, data={
            'error': 'invalid URL'
        })

    try:
        key = _store_url_and_get_key(url)
        return JsonResponse(status=200, data={
            'key': key
        })
    except Exception as e:
        logger.error('exception encountered while storing URL: {}'.format(e))

        return JsonResponse(status=500, data={
            'error': 'server error'
        })


def _retrieve_url_by_key(key):
    connection = _get_redis_connection()
    return connection.get(key)


def _is_url_valid(url):
    return True  # TODO: validate


def _store_url_and_get_key(url):
    key = _generate_key()
    _store_pair(key, url)
    return key


def _generate_key():
    return str(random.randint(0, 2000000))  # TODO: something better + check for collisions


def _store_pair(key, url):
    connection = _get_redis_connection()
    connection.set(key, url)


def _get_redis_connection():
    host, port = os.getenv("REDIS_SERVICE_HOST"), os.getenv("REDIS_SERVICE_PORT")
    if not host or not port:
        raise Exception('REDIS_SERVICE_HOST or REDIS_SERVICE_PORT not set')

    return redis.StrictRedis(host=host, port=int(port), db=0)