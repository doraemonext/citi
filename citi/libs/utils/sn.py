# -*- coding: utf-8 -*-

import base64
import uuid


def make_sn():
    """
    生成一个订单SN编号
    :return: uuid str
    """
    return uuid.uuid4().get_hex().replace('-', '')