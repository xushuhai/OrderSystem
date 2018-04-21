#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/17 10:03
# @Author  : Xsh
# @File    : line_volume.py
# @Software: PyCharm

import traceback

from config.order_app import db
from model.line_volume import LineVolume
from log.info import logger

from tools import constant as cs


def line_volume_set(line_code, cargos_volume, cargos_weight, id):
    """

    :param line_code:
    :param cargos_volume:
    :param cargos_weight:
    :param id:
    :return:
    """
    try:
        line_volume_obj = LineVolume.query.filter_by(line_code=line_code).first()
        if line_volume_obj:
            line_volume_obj.pending_volume += int(cargos_volume)
            line_volume_obj.pending_weight += int(cargos_weight)
            line_volume_obj.id = id
        else:
            line_volume = LineVolume(line_code, cargos_volume, cargos_weight, id)
            db.session.add(line_volume)
        db.session.commit()
        logger.debug(
            'insert line_volume type 【line_code:{}; cargos_volume:{}; cargos_weight:{}; operator_id:{}】'.format(
                line_code, cargos_volume, cargos_weight, id))
        return cs.OK
    except:
        logger.error('insert line_volume err : {}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def line_volume_get(line_code, cargos_volume, cargos_weight, id):
    """

    :param line_code:
    :param cargos_volume:
    :param cargos_weight:
    :param id:
    :return:
    """
    try:
        line_volume_obj = LineVolume.query.filter_by(line_code=line_code).first()
        if not line_volume_obj:
            return cs.NO_LINE_VOLUME, {'line_code': line_code}
        if line_volume_obj.pending_weight == 0 or line_volume_obj.pending_volume == 0:
            return None, None
        else:
            line_volume_obj.pending_volume -= int(cargos_volume)
            line_volume_obj.pending_weight -= int(cargos_weight)
            line_volume_obj.processed_volume += int(cargos_volume)
            line_volume_obj.processed_weight += int(cargos_weight)
            line_volume_obj.id = id
            db.session.commit()
            logger.debug(
                'modify line_volume type 【line_code:{}; cargos_volume:{}; cargos_weight:{}; operator_id:{}】'.format(
                    line_code, cargos_volume, cargos_weight, id))
            return None,None
    except:
        raise
    finally:
        db.session.rollback()


