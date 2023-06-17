import datetime
import json
import logging
import os
import random
import re
import string
import sys
import traceback
from os import path, remove
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger('db')


def generateRandomString():
    try:
        N = 15
        res = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))
        return res
    except:
        return False


def precheck(required_data=None):
    if required_data is None:
        required_data = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            try:
                request_data = None
                if request.method == 'GET':
                    request_data = request.GET
                elif request.method == 'POST':
                    request_data = request.data
                    if not len(request_data):
                        request_data = request.POST
                if len(request_data):
                    for i in required_data:
                        if i not in request_data:
                            return Response({'action': "Pre check", 'message': str(i) + " Not Found"},
                                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'action': "Pre check", 'message': "Message Data not Found"},
                                    status=status.HTTP_400_BAD_REQUEST)

                return view_func(request, *args, **kwargs)
            except:
                logger.warning("Pre check: " + str(sys.exc_info()))
                return Response({'action': "Pre check", 'message': "Something went wrong"},
                                status=status.HTTP_400_BAD_REQUEST)

        return wrapper_func

    return decorator
