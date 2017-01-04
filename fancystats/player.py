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
    numberkeys = ["g", "a1", "a2", "p", "cf", "ca", "ff",
    "fa", "gplusminus", "fo_w", "fo_l",
    "hitplus", "hitminus", "pnplus", "pnminus", "gf", "ga",
    "sf", "sa", "msf", "msa", "bsf", "bsa",
    "icf", "save", "bk", "ihsc", "isc", "zso", "zsd", "zsn",
    "scf", "sca", "sh", "ms", "toi",
    "onsf", "onsa", "onmsf", "onmsa", "onbsf", "onbsa",
    "hscf", "hsca"]
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


def init_goalie(name="", position="", team="", teamname=""):
    numberkeys = ["gu", "su", "gl", "sl", "gm", "sm", "gh", "sh", "toi"]
    strkeys = ["teamAbbr"]
    player = {}
    for n in numberkeys:
        player[n] = 0
    for n in strkeys:
        player[n] = ""
    player["name"] = name
    player["position"] = position
    player["team"] = team
    player["teamname"] = teamname
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


def get_goalie_stats(pbp, homeTeam, awayTeam, p2t, teamStrengths=None, scoreSituation=None, period=None):
    stats = {}
    prev_shot = None
    prev_play = None

    for play in pbp:
        if prev_play is not None and prev_play["period"] != play["period"]:
            prev_play = None
        hsc = play["homeScore"]
        asc = play["awayScore"]
        homeinclude, awayinclude = team.check_play(play, teamStrengths, scoreSituation, period, hsc, asc, homeTeam, awayTeam, p2t)
        include = (play["team_id"] == homeTeam and homeinclude) or (play["team_id"] == awayTeam and awayinclude)

        # Check for datetime for times
        if type(play["periodTime"]) != type(6):
            play["periodTime"] = play["periodTime"].hour * 60 + play["periodTime"].minute  # Thanks, NHL

        playTime = 0
        if prev_play is not None:
            playTime = play["periodTime"] - prev_play["periodTime"]
        else:
            playTime = play["periodTime"]

        for player in play["onice"]:
            pid = player["player_id"]
            pinfo = p2t[pid]
            pteam = pinfo[1]
            if pinfo[2] == 1:
                if pteam == homeTeam and homeinclude:
                    if pid not in stats:
                        stats[pid] = init_goalie(name=pinfo[3], position=pinfo[4], team=pinfo[1], teamname=pinfo[0])
                    stats[pid]["toi"] += playTime
                elif pteam == awayTeam and awayinclude:
                    if pid not in stats:
                        stats[pid] = init_goalie(name=pinfo[3], position=pinfo[4], team=pinfo[1], teamname=pinfo[0])
                    stats[pid]["toi"] += playTime

        if play["playType"] == "GOAL":
            zone, danger = shot.scoring_chance_standard(play, prev_shot, prev_play)
            # Individual stats
            scoreteam = play["team_id"]
            for player in play["onice"]:
                pid = player["player_id"]
                pinfo = p2t[pid]
                pteam = pinfo[1]
                pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                if pin and player["team_id"] != scoreteam and player["player__primaryPositionCode"] == "G":
                    field = "gu"
                    if zone == "LOW":
                        field = "gl"
                    elif zone == "MEDIUM":
                        field = "gm"
                    elif zone == "HIGH":
                        field = "gh"
                    stats[pid][field] += 1
        elif play["playType"] == "SHOT":
            zone, danger = shot.scoring_chance_standard(play, prev_shot, prev_play)
            shotteam = play["team_id"]
            for player in play["players"]:
                if player["player_type"] == 8:
                    pid = player["player_id"]
                    pinfo = p2t[pid]
                    pteam = pinfo[1]
                    pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                    if pin and pteam != shotteam and player["player__primaryPositionCode"] == "G":
                        field = "su"
                        if zone == "LOW":
                            field = "sl"
                        elif zone == "MEDIUM":
                            field = "sm"
                        elif zone == "HIGH":
                            field = "sh"
                        stats[pid][field] += 1


        if play["playType"] in ["SHOT", "GOAL", "MISSED_SHOT", "BLOCKED_SHOT"]:
            prev_shot = play
        prev_play = play

    for pid in stats:
        player = stats[pid]
        player["toiseconds"] = player["toi"]
        player["toi"] = toi.format_minutes(player["toi"])

    return stats


def get_stats(pbp, homeTeam, awayTeam, p2t, teamStrengths=None, scoreSituation=None, period=None):
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
        hsc = play["homeScore"]
        asc = play["awayScore"]
        homeinclude, awayinclude = team.check_play(play, teamStrengths, scoreSituation, period, hsc, asc, homeTeam, awayTeam, p2t)
        include = (play["team_id"] == homeTeam and homeinclude) or (play["team_id"] == awayTeam and awayinclude)

        # Check for datetime for times
        if type(play["periodTime"]) != type(6):
            play["periodTime"] = play["periodTime"].hour * 60 + play["periodTime"].minute  # Thanks, NHL

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
            zone, danger = shot.scoring_chance_standard(play, prev_shot, prev_play)
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                if pteam is not None and pin:
                    ptype = player["player_type"]
                    if ptype == 5:
                        stats[pteam][pid]["g"] += 1
                        stats[pteam][pid]["sf"] += 1
                        if danger < 3:
                            stats[pteam][pid]["isc"] += 1
                        else:
                            stats[pteam][pid]["ihsc"] += 1
                    elif ptype == 6:
                        stats[pteam][pid]["a1"] += 1
                    elif ptype == 16:
                        stats[pteam][pid]["a2"] += 1

            # On-Ice stats
            stats = play_corsi(stats, play, homeTeam, awayTeam, True, homeinclude, awayinclude)
            stats = play_oniceshot(stats, play, homeTeam, awayTeam, False, homeinclude, awayinclude)
            stats = play_sc(stats, play, homeTeam, awayTeam, homeinclude, awayinclude, danger)

        elif play["playType"] == "SHOT":
            # Individual Stats
            zone, danger = shot.scoring_chance_standard(play, prev_shot, prev_play)
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                if player["player_type"] == 7 and pin:
                    stats[pteam][pid]["sf"] += 1
                    if danger < 3:
                        stats[pteam][pid]["isc"] += 1
                    else:
                        stats[pteam][pid]["ihsc"] += 1

            # On-Ice stats
            stats = play_fenwick(stats, play, homeTeam, awayTeam, False, homeinclude, awayinclude)
            stats = play_corsi(stats, play, homeTeam, awayTeam, False, homeinclude, awayinclude)
            stats = play_oniceshot(stats, play, homeTeam, awayTeam, False, homeinclude, awayinclude)
            stats = play_sc(stats, play, homeTeam, awayTeam, homeinclude, awayinclude, danger)

        elif play["playType"] == "MISSED_SHOT":
            # Individual Stats
            zone, danger = shot.scoring_chance_standard(play, prev_shot, prev_play)
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                if player["player_type"] == 7 and pin:
                    stats[pteam][pid]["msf"] += 1
                    if danger < 3:
                        stats[pteam][pid]["isc"] += 1
                    else:
                        stats[pteam][pid]["ihsc"] += 1

            # On-Ice stats
            stats = play_fenwick(stats, play, homeTeam, awayTeam, False, homeinclude, awayinclude)
            stats = play_corsi(stats, play, homeTeam, awayTeam, False, homeinclude, awayinclude)
            stats = play_onicemissedshot(stats, play, homeTeam, awayTeam, False, homeinclude, awayinclude)
            stats = play_sc(stats, play, homeTeam, awayTeam, homeinclude, awayinclude, danger)

        elif play["playType"] == "BLOCKED_SHOT" :
            # Individual Stats
            zone, danger = shot.scoring_chance_standard(play, prev_shot, prev_play)
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                if player["player_type"] == 7 and pin:
                    stats[pteam][pid]["bsf"] += 1
                    if danger < 3:
                        stats[pteam][pid]["isc"] += 1
                    else:
                        stats[pteam][pid]["ihsc"] += 1
                elif player["player_type"] == 9 and pin:
                    stats[pteam][pid]["bk"] += 1

            # On-Ice stats

            oawayinclude = play["team_id"] == homeTeam and awayinclude
            ohomeinclude = play["team_id"] == awayTeam and homeinclude
            stats = play_corsi(stats, play, homeTeam, awayTeam, False, ohomeinclude, oawayinclude)
            stats = play_oniceblockedshot(stats, play, homeTeam, awayTeam, False, homeinclude, awayinclude)
            stats = play_sc(stats, play, homeTeam, awayTeam, homeinclude, awayinclude, danger)

        elif play["playType"] == "FACEOFF":
            # Individual Stats
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                if player["player_type"] == 1 and pin:
                    stats[pteam][pid]["fo_w"] += 1
                elif player["player_type"] == 2 and pin:
                    stats[pteam][pid]["fo_l"] += 1
            if play["period"] == 2 or play["period"] == 4:
                xcoord = -play["xcoord"]
            else:
                xcoord = play["xcoord"]
            if xcoord < -25.00 and awayinclude:
                for player in play["onice"]:
                    pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                    pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                    if pin and "zso" in stats[pteam][pid]:
                        if pteam == awayTeam:
                            stats[pteam][pid]["zso"] += 1
                        else:
                            stats[pteam][pid]["zsd"] += 1
            elif xcoord > 25.00 and homeinclude:
                for player in play["onice"]:
                    pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                    pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                    if pin and "zso" in stats[pteam][pid]:
                        if pteam == homeTeam:
                            stats[pteam][pid]["zso"] += 1
                        else:
                            stats[pteam][pid]["zsd"] += 1
            else:
                for player in play["onice"]:
                    pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                    pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                    if pin and "zsn" in stats[pteam][pid]:
                        stats[pteam][pid]["zsn"] += 1

        elif play["playType"] == "HIT":
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                if player["player_type"] == 3 and pin:
                    stats[pteam][pid]["hitplus"] += 1
                elif player["player_type"] == 4 and pin:
                    stats[pteam][pid]["hitminus"] += 1
        elif play["playType"] == "PENALTY":
            for player in play["players"]:
                pid, pteam = get_info(player, stats, homeTeam, awayTeam)
                pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
                if player["player_type"] == 10 and pin:
                    stats[pteam][pid]["pnplus"] += 1
                elif player["player_type"] == 11 and pin:
                    stats[pteam][pid]["pnminus"] += 1

        if play["playType"] in ["SHOT", "GOAL", "MISSED_SHOT", "BLOCKED_SHOT"]:
            prev_shot = play
        prev_play = play

    for pteam in stats:
        for pid in stats[pteam]:
            player = stats[pteam][pid]
            player["p"] = player["g"] + player["a1"] + player["a2"]
            player["toiseconds"] = player["toi"]
            player["toi"] = toi.format_minutes(player["toi"])

    return stats


def play_fenwick(stats, play, homeTeam, awayTeam, isGoal, homeinclude, awayinclude):
    return play_stat(stats, play, homeTeam, awayTeam, "ff", "fa", isGoal, homeinclude, awayinclude)


def play_corsi(stats, play, homeTeam, awayTeam, isGoal, homeinclude, awayinclude):
    return play_stat(stats, play, homeTeam, awayTeam, "cf", "ca", isGoal, homeinclude, awayinclude)


def play_oniceshot(stats, play, homeTeam, awayTeam, isGoal, homeinclude, awayinclude):
    return play_stat(stats, play, homeTeam, awayTeam, "onsf", "onsa", isGoal, homeinclude, awayinclude)


def play_onicemissedshot(stats, play, homeTeam, awayTeam, isGoal, homeinclude, awayinclude):
    return play_stat(stats, play, homeTeam, awayTeam, "onmsf", "onmsa", isGoal, homeinclude, awayinclude)


def play_oniceblockedshot(stats, play, homeTeam, awayTeam, isGoal, homeinclude, awayinclude):
    return play_stat(stats, play, homeTeam, awayTeam, "onbsf", "onbsa", isGoal, homeinclude, awayinclude)


def play_sc(stats, play, homeTeam, awayTeam, homeinclude, awayinclude, danger):
    for player in play["onice"]:
        pid, pteam = get_info(player, stats, homeTeam, awayTeam)
        pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
        if pin and pteam is not None and pid in stats[pteam]:
            if pteam == play["team_id"]:
                if danger < 3:
                    stats[pteam][pid]["scf"] += 1
                else:
                    stats[pteam][pid]["hscf"] += 1
            else:
                if danger < 3:
                    stats[pteam][pid]["sca"] += 1
                else:
                    stats[pteam][pid]["hsca"] += 1
    return stats


def play_stat(stats, play, homeTeam, awayTeam, vf, va, isGoal, homeinclude, awayinclude):
    for player in play["onice"]:
        pid, pteam = get_info(player, stats, homeTeam, awayTeam)
        pin = (pteam == homeTeam and homeinclude) or (pteam == awayTeam and awayinclude)
        if pin and pteam is not None and pid in stats[pteam]:
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
    return stats


def get_info(player, stats, homeTeam, awayTeam):
    pid = player["player_id"]
    pteam = None
    if pid in stats[homeTeam]:
        pteam = homeTeam
    elif pid in stats[awayTeam]:
        pteam = awayTeam
    return pid, pteam
