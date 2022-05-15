# 필수 값
from django.db.models import QuerySet, Max, F
from rest_framework.exceptions import APIException
from rest_framework_jwt.settings import api_settings
from typing import Optional

from config.common.response_code import STATUS_RSP_MISSING_MANDATORY_PARAM

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

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
        if data in ["", None]:
            data = default_value
    except:
        try:
            json_body = request.data
            data = json_body[name]
            if data in ["", None]:
                data = default_value
        except:
            data = default_value
    return data


def get_max_int_from_queryset(qs: QuerySet, field_name: str) -> Optional[int]:
    return qs.aggregate(_max=Max(field_name)).get('_max')


def make_space_ordering_from_queryset(qs: QuerySet, current_order_number: int, target_order_number: int, field_name: str) -> None:
    """
    make space to set ordering.
    if `target_order_number` is lower than `current_order_number` get lower orderNumbers then make space by adding 1 orderNumber
    else `current_order_number` is lower than `target_order_number` get upper orderNumbers then make space by subtract 1 orderNumber
    """

    get_lower_order_number_option = {
        f'{field_name}__lt': current_order_number,
        f'{field_name}__gte': target_order_number,
    }
    get_upper_order_number_option = {
        f'{field_name}__lte': target_order_number,
        f'{field_name}__gt': current_order_number,
    }

    if target_order_number < current_order_number:
        need_to_modify_ordering_qs = qs.filter(
            **get_lower_order_number_option
        )
        need_to_modify_ordering_qs.update(orderNumber=F('orderNumber') + 1)
    elif target_order_number > current_order_number:
        need_to_modify_ordering_qs = qs.filter(
            **get_upper_order_number_option
        )
        need_to_modify_ordering_qs.update(orderNumber=F('orderNumber') - 1)


def get_login_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token
