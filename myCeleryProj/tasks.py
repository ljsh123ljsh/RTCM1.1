from myCeleryProj import *
from myCeleryProj.app import app
from RTCM_ANALYSE.Analyse import analyseWholeFrame


@app.task
def task1(content):
    analyseWholeFrame(content)

@app.task
def task2(content):
    analyseWholeFrame(content)


