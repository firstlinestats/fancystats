from __future__ import division


def adj_save_percent(savesLow, savesMedium, savesHigh, goalsLow, goalsMedium, goalsHigh,
                     shotsLow, shotsMedium, shotsHigh):
    """
    WOI defined adjusted save percentage as:
    AdSv% = (S_l/(S_l + G_l) * AllShots_l + S_m/(S_m + G_m) * AllShots_m + S_h/(S_h + G_h) * AllShots_h ) / (AllShots_l + AllShots_m + AllShots_h)
    """
    lowp = save_percent(savesLow, goalsLow) * shotsLow
    mediump = save_percent(savesMedium, goalsMedium) * shotsMedium
    highp = save_percent(savesHigh, goalsHigh) * shotsHigh
    return '%.2f' % ((lowp + mediump + highp) / (shotsLow + shotsMedium + shotsHigh) * 100)


def save_percent(saves, goals):
    shots = saves + goals
    if shots == 0:
        return 0
    else:
        return saves / shots
