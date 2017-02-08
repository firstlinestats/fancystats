import corsi
import shot
import toi


def init_team():
    ts = {}
    numberkeys = ["give", "take", "gf", "sf", "msf", "bsf", "bsa", "cf", "scf",
        "hscf", "zso", "hit", "pn", "fo_w", "toi"]
    stringkeys = ["team", ]
    for n in numberkeys:
        ts[n] = 0
    for s in stringkeys:
        ts[s] = ""
    return ts


def check_play(play, teamStrengths, scoreSituation, period, hsc, asc, homeTeam, awayTeam, p2t):
    hb = True
    ab = True

    hp = 0
    ap = 0
    hg = 0
    ag = 0

    try:
        period = int(period)
    except:
        pass
    teamStrengths = str(teamStrengths)
    scoreSituation = str(scoreSituation)

    if "onice" in play:
        for player in play["onice"]:
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
        allh = hp + hg
        alla = ap + ag
    else:
        hp = play["homeSkaters"]
        ap = play["awaySkaters"]
        hg = play["homeGoalie"]
        ag = play["awayGoalie"]
        allh = hp + play["homeGoalie"]
        alla = ap + play["awayGoalie"]

    # Find situations where play should not be included
    ## Team Strengths
    if teamStrengths == "even":
        # home and away skaters must be 5, each team must have a goalie
        if hp != 5 or ap != 5 or ag != 1 or hg != 1:
            hb, ab = False, False
    elif teamStrengths == "pp":
        # a team is said to be on a power play when at least one opposing player is serving a
        # penalty, and the team has a numerical advantage on the ice (whenever both teams have
        # the same number of players on the ice, there is no power play)
        if allh > alla:
            ab = False  # Home is on the power play
        elif alla > allh:
            hb = False  # Away is on the power play
        elif alla == allh:
            hb, ab = False, False  # Teams have even number of players on ice
    elif teamStrengths == "pk":
        # a team is said to be on a power play when at least one opposing player is serving a
        # penalty, and the team has a numerical advantage on the ice (whenever both teams have
        # the same number of players on the ice, there is no power play)
        if allh > alla:
            hb = False  # Home is on the power play
        elif alla > allh:
            ab = False  # Away is on the power play
        elif alla == allh:
            hb, ab = False, False  # Teams have even number of players on ice
    elif teamStrengths == "4v4":
        # teams must have 4 skaters and 1 goalie
        if hp != 4 or ap != 4 or ag != 1 or hg != 1:
            hb, ab = False, False
    elif teamStrengths == "og":
        if ag != 0:
            hb = False
        if hg != 0:
            ab = False
    elif teamStrengths == "tg":
        if ag != 0:
            ab = False
        if hg != 0:
            hb = False
    elif teamStrengths == "3v3":
        if hp != 3 or ap != 3 or ag != 1 or hg != 1:
            hb, ab = False, False

    ## Score Situations
    if scoreSituation == "t3+":
        if hsc - asc < 3:
            ab = False  # Not currently trailing by 3 or more
        if asc - hsc < 3:
            hb = False
    elif scoreSituation == "t2":
        # Check to see if the team is trailing by 2
        if hsc - asc != 2:
            ab = False
        if asc - hsc != 2:
            hb = False
    elif scoreSituation == "t1":
        # Check to see if the team is trailing by 2
        if hsc - asc != 1:
            ab = False
        if asc - hsc != 1:
            hb = False
    elif scoreSituation == "t":
        if hsc != asc:
            hb, ab = False, False
    elif scoreSituation == "l1":
        # Check to see if the team is winning by 1
        if hsc - asc != 1:
            hb = False
        if asc - hsc != 1:
            ab = False
    elif scoreSituation == "l2":
        # Check to see if the team is winning by 2
        if hsc - asc != 2:
            hb = False
        if asc - hsc != 2:
            ab = False
    elif scoreSituation == "l3+":
        # Check to see if the team is winning by 3+
        if hsc - asc < 3:
            hb = False
        if asc - hsc < 3:
            ab = False
    elif scoreSituation == "w1":
        diff = abs(hsc - asc)
        if diff > 1:
            hb, ab = False, False

    ## Periods
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
        elif play["playType"] == "GIVEAWAY":
            if include:
                stats[play["team_id"]]["give"] += 1
        elif play["playType"] == "TAKEAWAY":
            if include:
                stats[play["team_id"]]["take"] += 1

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
        td["toiseconds"] = td["toi"]
        td["toi"] = toi.format_minutes(td["toi"])

    return stats

