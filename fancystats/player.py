import constants
import team
import shot
import toi


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

        for player in play["onice"]:
            pid, pteam = get_info(player, stats, homeTeam, awayTeam)
            if pteam == homeTeam and homeinclude:
                stats[homeTeam][pid]["toi"] += playTime
            elif pteam == awayTeam and awayinclude:
                stats[awayTeam][pid]["toi"] += playTime

        if play["playType"] == "GOAL":
            # Individual stats
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                if pteam is not None:
                    ptype = player["player_type"]
                    if ptype == 5:
                        stats[pteam][pid]["g"] += 1
                        stats[pteam][pid]["sf"] += 1
                    elif ptype == 6:
                        stats[pteam][pid]["a1"] += 1
                    elif ptype == 16:
                        stats[pteam][pid]["a2"] += 1

            # On-Ice stats
            play_corsi(stats, play, homeTeam, awayTeam, True)

        elif play["playType"] == "SHOT":
            # Individual Stats
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                if player["player_type"] == 7:
                    stats[pteam][pid]["sf"] += 1

            # On-Ice stats
            play_fenwick(stats, play, homeTeam, awayTeam, False)
            play_corsi(stats, play, homeTeam, awayTeam, False)

        elif play["playType"] == "MISSED_SHOT":
            # Individual Stats
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                if player["player_type"] == 7:
                    stats[pteam][pid]["sf"] += 1

            # On-Ice stats
            play_fenwick(stats, play, homeTeam, awayTeam, False)
            play_corsi(stats, play, homeTeam, awayTeam, False)

        elif play["playType"] == "BLOCKED_SHOT":
            # Individual Stats
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                if player["player_type"] == 7:
                    stats[pteam][pid]["sf"] += 1

            # On-Ice stats
            play_corsi(stats, play, awayTeam, homeTeam, False) # Swap for blocked shots

        elif play["playType"] == "FACEOFF":
            # Individual Stats
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                if player["player_type"] == 1:
                    stats[pteam][pid]["fo_w"] += 1
                elif player["player_type"] == 2:
                    stats[pteam][pid]["fo_l"] += 1
        elif play["playType"] == "HIT":
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                if player["player_type"] == 3:
                    stats[pteam][pid]["hitplus"] += 1
                elif player["player_type"] == 4:
                    stats[pteam][pid]["hitminus"] += 1
        elif play["playType"] == "PENALTY":
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                if player["player_type"] == 10:
                    stats[pteam][pid]["pnplus"] += 1
                elif player["player_type"] == 11:
                    stats[pteam][pid]["pnminus"] += 1

        if play["playType"] in ["SHOT", "GOAL", "MISSED_SHOT", "BLOCKED_SHOT"]:
            prev_shot = play
        prev_play = play

    for pteam in stats:
        for pid in stats[pteam]:
            player = stats[pteam][pid]
            player["p"] = player["g"] + player["a1"] + player["a2"]
            player["toi"] = toi.format_minutes(player["toi"])

    return stats


def play_fenwick(stats, play, homeTeam, awayTeam, isGoal):
    play_stat(stats, play, homeTeam, awayTeam, "ff", "fa", isGoal)


def play_corsi(stats, play, homeTeam, awayTeam, isGoal):
    play_stat(stats, play, homeTeam, awayTeam, "cf", "ca", isGoal)


def play_stat(stats, play, homeTeam, awayTeam, vf, va, isGoal):
    for player in play["onice"]:
        pid, pteam = get_info(player, stats, homeTeam, awayTeam)
        if pteam is not None and pid in stats[pteam]:
            if pteam == play["team_id"]:
                stats[pteam][pid][vf] += 1
                if isGoal:
                    stats[pteam][pid]["gf"] += 1
                    stats[pteam][pid]["gplusminus"] += 1
            else:
                stats[pteam][pid][va] += 1
                if isGoal:
                    stats[pteam][pid]["ga"] += 1
                    stats[pteam][pid]["gplusminus"] -= 1


def get_info(player, stats, homeTeam, awayTeam):
    pid = player["player_id"]
    pteam = None
    if pid in stats[homeTeam]:
        pteam = homeTeam
    elif pid in stats[awayTeam]:
        pteam = awayTeam
    return pid, pteam
