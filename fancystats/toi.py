from __future__ import division


def format_minutes(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return "%d:%02d:%02d" % (h, m, s)
    else:
        return "%d:%02d" % (m, s)


def time_report(toi, seconds, games=1, format="seconds"):
    """Generates a report of all relevant TOI data
    toi = Time On Ice, in seconds
    seconds = Total Time Elapsed, in seconds
    games = Number of games data is from
    format = Format of time to be returned (supported: seconds, minutes)
    """
    time_data = {}
    time_data["toioff"] = toi_off(toi, seconds)
    time_data["toi%"] = toi_percent(toi, seconds)
    time_data["toi60"] = toi_60(toi, seconds)
    time_data["toi_game"] = toi_game(toi, games)
    if format == "seconds":
        for key in time_data:
            time_data[key] = round(time_data[key], 2)
    elif format == "minutes":
        for key in time_data:
            time_data[key] = format_minutes(time_data[key])
    else:
        print "Time Format not currently supported!"
        raise Exception
    return time_data


def toi_off(toi, seconds):
    """Calculates TOIoff, the time when a player is off the ice, but in a game in which they played
    toi = Time On Ice, in seconds
    seconds = Total Time Elapsed, in seconds
    """
    try:
        return seconds - toi
    except:
        print "TOI Exception: Both seconds and toi must be integers"
        raise Exception


def toi_percent(toi, seconds):
    """Calculates TOI%, the percentage of time a player spends on the ice
    toi = Time On Ice, in seconds
    seconds = Total Time Elapsed, in seconds
    """
    try:
        if seconds > 0:
            return toi / seconds * 100
        else:
            return 0
    except:
        print "TOI Exception: Both seconds and toi must be positive integers"


def toi_60(toi, seconds):
    """Calculates TOI60, the amount of minutes out of 60 that the player was on the ice
    toi = Time On Ice, in seconds
    seconds = Total Time Elapsed, in seconds
    """
    try:
        if seconds > 0:
            return (toi * 60 * 60) / seconds
        else:
            return 0
    except:
        print "TOI Exception: Both seconds and toi must be positive integers"


def toi_game(toi, games):
    """Calculates TOI/Gm, the amount of time spent on the ice per game
    toi = Time On Ice, in seconds
    games = Total Number of Games
    """
    try:
        if games > 0:
            return toi / games
        else:
            return 0
    except:
        print "TOI Exception: Both games and toi must be >= 0"
