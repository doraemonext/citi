# -*- coding: utf-8 -*-

from django.db import DatabaseError

from .models import Settings


def get_setting_dict(name=None):
    """
    获取设置列表

    每个设置项为一个dict, 多个设置项组成了一个list返回
    当指定了name参数, 返回该设置项的value, 为str类型
    :param name: 当name为None的时候, 返回全部设置项组成的list, 否则返回指定的设置项的value
    :return: dict or str
    """
    if name:
        result = Settings.objects.filter(name=name)

        if result.count() == 0:
            raise DatabaseError('Cannot find matching setting object.')
        elif result.count() > 1:
            raise DatabaseError('Multi setting objects are found.')

        return result.values()[0]['value']
    else:
        result = Settings.objects.all()
        return result.values()