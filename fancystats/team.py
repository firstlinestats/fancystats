import corsi
import shot
import toi


def init_team():
    ts = {}
    numberkeys = ["gf", "sf", "msf", "bsf", "bsa", "cf", "scf", "hscf", "zso", "hit", "pn", "fo_w", "toi"]
    stringkeys = ["team", ]
    for n in numberkeys:
        ts[n] = 0
    for s in stringkeys:
        ts[s] = ""
    return ts


def check_play(play, teamStrengths, scoreSituation, period, hsc, asc, homeTeam, awayTeam, p2t):
    hb = False
    ab = False

    hp = 0
    ap = 0
    hg = 0
    ag = 0

    for player in play["players"]:
        pinfo = p2t[player["player_id"]]
        if pinfo[1] == homeTeam:
            if pinfo[2] == 0:
                hp += 1
            else:
                hg += 1
        else:
            if pinfo[2] == 0:
                ap += 1
            else:
                ag += 1
    if teamStrengths is None or teamStrengths == "all":
        hb, ab = True, True
    elif teamStrengths == "4v4" and hp == 4 and ap == 4:
        hb, ab = True, True
    elif teamStrengths == "even" and hp == ap and hp == 5:
        hb, ab = True, True
    elif teamStrengths == "pp":
        if hp == ap + 1:
            hb, ab = True, False
        elif hp + 1 == ap:
            hb, ab = False, True
    elif teamStrengths == "pk":
        if hp == ap + 1:
            hb, ab = False, True
        elif hp + 1 == ap:
            hb, ab = True, False
    elif teamStrengths == "3v3" and hp == 3 and ap == 3:
        hb, ab = True, True
    elif teamStrengths == "og":
        if hg is True and ag is False:
            hb, ab = False, True
        elif hg is False and ag is True:
            hb, ab = True, False
        elif hg is True and ag is True:
            hb, ab = True, True
    elif teamStrengths == "tg":
        if hg is True and ag is False:
            hb, ab = True, False
        elif hg is False and ag is True:
            hb, ab = False, True
        elif hg is True and ag is True:
            hb, ab = True, True
    if scoreSituation is not None and scoreSituation != "all":
        # Only account for removing the play!
        if scoreSituation == "t3+":
            if hsc <= asc + 3:
                hb = False
            if asc <= hsc + 3:
                ab = False
        elif scoreSituation == "t2":
            if hsc != asc - 2:
                hb = False
            if asc != hsc - 2:
                ab = False
        elif scoreSituation == "t1":
            if hsc != asc - 1:
                hb = False
            if asc != hsc - 1:
                ab = False
        elif scoreSituation == "t":
            if hsc != asc:
                hb, ab = False, False
        elif scoreSituation == "l3+":
            if hsc < asc + 3:
                hb = False
            if asc < hsc + 3:
                ab = False
        elif scoreSituation == "l2":
            if hsc != asc + 2:
                hb = False
            if asc != hsc + 2:
                ab = False
        elif scoreSituation == "l1":
            if hsc != asc + 1:
                hb = False
            if asc != hsc + 1:
                ab = False
        elif scoreSituation == "w1":
            if hsc > asc + 1 or hsc < asc - 1:
                hb, ab = False, False
    if period is not None and period != "all":
        if period == "OT":
            if play["period"] < 4:
                hb, ab = False, False
        elif play["period"] != int(period):
            hb, ab = False, False
    return hb, ab


def get_stats(pbp, homeTeam, awayTeam, p2t, teamStrengths=None, scoreSituation=None, period=None):
    stats = {}
    prev_shot = None
    prev_play = None
    stats[homeTeam] = init_team()
    stats[awayTeam] = init_team()

    for play in pbp:
        if prev_play is not None and prev_play["period"] != play["period"]:
            prev_play = None
        hsc = play["homeScore"]
        asc = play["awayScore"]
        homeinclude, awayinclude = check_play(play, teamStrengths, scoreSituation, period, hsc, asc, homeTeam, awayTeam, p2t)
        include = (play["team_id"] == homeTeam and homeinclude) or (play["team_id"] == awayTeam and awayinclude)
        oinclude = (play["team_id"] == homeTeam and awayinclude) or (play["team_id"] == awayTeam and homeinclude)

        # Check for datetime for times
        if type(play["periodTime"]) != type(6):
            play["periodTime"] = play["periodTime"].hour * 60 + play["periodTime"].minute  # Thanks, NHL
        if play["playType"] in ["SHOT", "GOAL", "MISSED_SHOT", "BLOCKED_SHOT"] and include:
            zone, danger = shot.scoring_chance_standard(play, prev_shot, prev_play)
            if danger < 3: 
                stats[play["team_id"]]["scf"] += 1
            else:
                stats[play["team_id"]]["hscf"] += 1

        playTime = 0
        if prev_play is not None:
            playTime = play["periodTime"] - prev_play["periodTime"]
        else:
            playTime = play["periodTime"]

        if homeinclude:
            stats[homeTeam]["toi"] += playTime
        if awayinclude:
            stats[awayTeam]["toi"] += playTime

        if play["playType"] == "GOAL":
            if include:
                stats[play["team_id"]]["gf"] += 1
                stats[play["team_id"]]["sf"] += 1
        elif play["playType"] == "SHOT":
            if include:
                stats[play["team_id"]]["sf"] += 1
        elif play["playType"] == "MISSED_SHOT":
            if include:
                stats[play["team_id"]]["msf"] += 1
        elif play["playType"] == "BLOCKED_SHOT":
            if homeTeam == play["team_id"]:
                oteam = awayTeam
            else:
                oteam = homeTeam
            if include:
                stats[play["team_id"]]["bsf"] += 1
            if oinclude:
                stats[oteam]["bsa"] += 1
        elif play["playType"] == "FACEOFF":
            if play["period"] % 2 == 0:
                play["xcoord"] = -play["xcoord"]
            if play["xcoord"] < -25.00 and awayinclude:
                stats[awayTeam]["zso"] += 1
            elif play["xcoord"] > 25.00 and homeinclude:
                stats[homeTeam]["zso"] += 1
            if include:
                stats[play["team_id"]]["fo_w"] += 1
        elif play["playType"] == "HIT":
            if include:
                stats[play["team_id"]]["hit"] += 1
        elif play["playType"] == "PENALTY":
            if include:
                stats[play["team_id"]]["pn"] += 1

        if play["playType"] in ["SHOT", "GOAL", "MISSED_SHOT", "BLOCKED_SHOT"]:
            prev_shot = play
        prev_play = play

    for team in stats:
        td = stats[team]
        if team == homeTeam:
            bsf = stats[awayTeam]["bsf"]
        else:
            bsf = stats[homeTeam]["bsf"]
        td["cf"] = corsi.calc_corsi(td["sf"], td["msf"], td["bsa"], "team.get_stats")
        td["toi"] = toi.format_minutes(td["toi"])

    return stats
            
