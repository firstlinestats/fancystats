import constants
import team
import shot


def get_player_type(given):
    for option in constants.playerTypes:
        if option[1] == given:
            return option[0]
    return 0


def get_player_position(given):
    for option in constants.playerPositions:
        if option[1] == given:
            return option[0]
    return 0


def init_player(name="", position="", team=""):
    numberkeys = ["g", "a1", "a2", "p", "cf", "ca", "ff", "fa", "gplusminus", "fo_w", "fo_l",
    "hitplus", "hitminus", "pnplus", "pnminus", "gf", "ga", "sf", "sa", "msf", "msa", "bsf", "bsa",
    "icf", "save", "ab", "bk", "ihsc", "isc", "zso", "zsd", "scf", "sca", "sh", "ms", "toi"]
    strkeys = []
    player = {}
    for n in numberkeys:
        player[n] = 0
    for n in strkeys:
        player[n] = ""
    player["name"] = name
    player["position"] = position
    player["team"] = team
    return player


def init_goalie():
    numberkeys = ["gu", "su", "gl", "sl", "gm", "sm", "gh", "sh", "toi"]
    strkeys = ["name", "position", "team", "teamAbbr"]
    player = {}
    for n in numberkeys:
        player[n] = 0
    for n in strkeys:
        player[n] = ""
    return player


def calc_sa(sas, seconds):
    sas.append({"seconds": seconds, "value": len(sas) + 1})


def findPPGoal(eventcount, teampp, teamgoal):
    for pp in eventcount[teampp]:
        start = pp["seconds"]
        end = pp["seconds"] + pp["length"]
        for goal in eventcount[teamgoal]:
            if goal["seconds"] > start and goal["seconds"] < end:
                pp["length"] = goal["seconds"] - start
    return eventcount


def get_stats(pbp, homeTeam, awayTeam, p2t, teamStrengths=None, scoreSituation=None, hsc=None, asc=None):
    stats = {homeTeam: {}, awayTeam:{}}
    prev_shot = None
    prev_play = None

    for pid in p2t:
        player = p2t[pid]
        if player[2] != 1:
            stats[player[1]][pid] = init_player(name=player[3], position=player[4], team=player[1])

    for play in pbp:
        if prev_play is not None and prev_play["period"] != play["period"]:
            prev_play = None

        # Check for datetime for times
        if type(play["periodTime"]) != type(6):
            play["periodTime"] = play["periodTime"].hour * 60 + play["periodTime"].minute  # Thanks, NHL

        homeinclude, awayinclude = team.check_play(play, teamStrengths, scoreSituation, hsc, asc, homeTeam, awayTeam, p2t)
        playTime = 0
        if prev_play is not None:
            playTime = play["periodTime"] - prev_play["periodTime"]
        else:
            playTime = play["periodTime"]

    return stats
