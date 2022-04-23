# 필수 값
from rest_framework.exceptions import APIException

from config.common.response_code import STATUS_RSP_MISSING_MANDATORY_PARAM


def response_serializer(code, data=None, message=None):
    json_data = dict()
    json_data["code"] = code.get("code")
    json_data["message"] = message
    json_data["data"] = data
    return json_data


def mandatory_key(request, name):
    try:
        if request.method == 'GET':
            data = request.GET[name]
        else:
            data = request.POST[name]
        if data in ["", None]:
            raise APIException(STATUS_RSP_MISSING_MANDATORY_PARAM, {"keywords": [name]})
    except:
        try:
            json_body = request.data
            data = json_body[name]
            if data in ["", None]:
                raise APIException(STATUS_RSP_MISSING_MANDATORY_PARAM, {"keywords": [name]})
        except:
            raise APIException(STATUS_RSP_MISSING_MANDATORY_PARAM, {"keywords": [name]})

    return data


# 선택 값
def optional_key(request, name, default_value=''):
    try:
        if request.method == 'GET':
            data = request.GET[name]
        else:
            data = request.POST[name]
        if data in ["", None, 'null', 'undefined']:
            data = default_value
    except:
        try:
            json_body = request.data
            data = json_body[name]
            if data in ["", None, 'null', 'undefined']:
                data = default_value
        except:
            data = default_value
    return data

