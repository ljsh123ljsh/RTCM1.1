from __future__ import absolute_import
from celery import Celery
from RTCM_ANALYSE.Analyse import analyse
from stable.Tool import segment_d30
from threading import Thread