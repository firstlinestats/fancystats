SHOT_TYPES = ["GOAL", "SHOT", "MISSED_SHOT", "BLOCKED_SHOT"]


def in_other_end(xcoord, prev_xcoord):
    """Calculate is the previous x coordinate is in a different zone
    TODO: Change from 0 to -25/25?
    xcoord = X coordinate of current play
    prev_xcoord = X coordinate of previous play
    """
    if (xcoord > 0 and prev_xcoord <= 0) or (xcoord < 0 and prev_xcoord >= 0):
        return True
    return False


def rebound(period, team, period_time,
    prev_period=None, prev_team=None, prev_shot_type=None, prev_period_time=None):
    """Calculates if a shot was a rebound, based on it and the last shot
    period = Period for the current shot
    team = Unique identifier for the team who shot
    period_time = Time, in seconds, of the play
    prev_period = Period of the previous shot, if applicable
    prev_team = Unique identifier for the previous team who shot, if applicable
    prev_shot_type = Type of the previous shot, makes sure it wasn't "GOAL"
    prev_period_time = Time, in seconds, of the previous shot
    """
    if prev_shot_type is not None and period == prev_period:
        if team == prev_team and prev_shot_type != "GOAL":
            diff = period_time - prev_period_time
            if diff <= 3:
                return True
    return False


def rush(period, period_time, play_type, xcoord,
    prev_period=None, prev_period_time=None, prev_xcoord=None):
    """Calculates if a shot is a rush shot, as defined by David Johnson and later modified by WAR-On-Ice
    period = Period for the current shot
    period_time = Time, in seconds, of the play
    play_type = Unique identifier for the play type, following general hockey standards (see SHOT_TYPES above)
    xcoord = X coordinate of the shot, follows general principles of x coordinates provided by the league
    prev_period = Period for the last event
    prev_period_time = Time, in seconds, of the previous play
    prev_xcoord = X coordinate of the last event
    """
    if play_type in SHOT_TYPES and period == prev_period and period_time - prev_period_time <= 4 \
            and in_other_end(xcoord, prev_xcoord):
        return True
    return False


def point_inside_polygon(x, y, poly):
    """Determines if the point is inside the given polygon
    x = x coordinate of point
    y = y coordinate of point
    poly = polygon, given in a list of lists format
    """
    # check if point is a vertex
    inside = False
    if x is not None and y is not None:
        x = float(x)
        y = float(y)
        if x < 0:
            x = abs(x)
            y = -y
        if (x,y) in poly: return True

        # check if point is on a boundary
        for i in range(len(poly)):
            p1 = None
            p2 = None
            if i==0:
                p1 = poly[0]
                p2 = poly[1]
            else:
                p1 = poly[i-1]
                p2 = poly[i]
            if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
                return True
          
        n = len(poly)

        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

    if inside:
        return True
    else:
        return False


def danger_zone(xcoord, ycoord):
    """Determine the danger zone of the given shot
    xcoord = x coordinate of the shot, as given by the league
    ycoord = y coordinate of the shot, as given by the league
    """
    poly = [(89, -9),
        (69, -22), (54, -22),
        (54, -9), (44, -9),
        (44, 9), (54, 9),
        (54, 22), (69, 22),
        (89, 9), (89, -9)]
    highpoly = [(89, -9)
,        (69, -9), (69, 9),
        (89, 9), (89, -9)]    
    if point_inside_polygon(xcoord, ycoord, highpoly) is True:
        return "HIGH"
    elif point_inside_polygon(xcoord, ycoord, poly) is True:
        return "MEDIUM"
    return "LOW"


def scoring_chance_standard(play, prev_shot, prev_play):
    if prev_shot is not None and prev_play is not None:
        return scoring_chance(play["period"], play["team_id"], play["periodTime"], play["xcoord"], play["ycoord"],
            play["playType"], prev_shot["period"], prev_shot["team_id"], prev_shot["playType"],
            prev_shot["periodTime"], prev_play["period"], prev_play["periodTime"], prev_play["xcoord"])
    elif prev_shot is None and prev_play is not None:
        return scoring_chance(play["period"], play["team_id"], play["periodTime"], play["xcoord"], play["ycoord"],
            play["playType"], pp_period=prev_play["period"], pp_period_time=prev_play["periodTime"], pp_xcoord=prev_play["xcoord"])
    elif prev_shot is not None and prev_play is None:
        return scoring_chance(play["period"], play["team_id"], play["periodTime"], play["xcoord"], play["ycoord"],
            play["playType"], prev_shot["period"], prev_shot["team_id"], prev_shot["playType"],
            prev_shot["periodTime"])
    else:
        return scoring_chance(play["period"], play["team_id"], play["periodTime"], play["xcoord"], play["ycoord"], play["playType"])


def scoring_chance(period, team, period_time, xcoord, ycoord, play_type,
        ps_period=None, ps_team=None, ps_type=None, ps_period_time=None,
        pp_period=None, pp_period_time=None, pp_xcoord=None):
    """Determines the zone and the scoring chance of a given shot given the previous shot and previous play,
    both are defined by WAR-On-Ice here http://blog.war-on-ice.com/new-defining-scoring-chances/
    period = Period of the current shot
    team = Unique identifier of the current team
    period_time = Time, in seconds, of the shot
    xcoord = X coordinate of the shot, as given by the league
    ycoord = Y coordinate of the shot, as given by the league
    play_type = the Type of shot
    ps_period = Previous shot's period
    ps_team = Previous shot's team
    ps_type = Previous shot's type
    ps_period_time = Previous shot's time, in seconds
    pp_period = Previous play's period
    pp_period_time = Previous play's time, in seconds
    pp_xcoord = Previous play's X coordinate
    """
    is_rebound = rebound(period, team, period_time, ps_period, ps_team, ps_type, ps_period_time)
    is_rush = rush(period, period_time, play_type, xcoord, pp_period, pp_period_time, pp_xcoord)
    zone = danger_zone(xcoord, ycoord)
    if zone == "HIGH":
        danger = 3
    elif zone == "MEDIUM":
        danger = 2
    else:
        danger = 1
    if is_rebound or is_rush:
        danger += 1
    if play_type == "BLOCKED_SHOT":
        danger -= 1
    if danger == 0:
        danger = 1
    return zone, danger
    