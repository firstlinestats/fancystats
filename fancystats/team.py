import corsi
import shot


def init_team():
    ts = {}
    numberkeys = ["gf", "sf", "msf", "bsf", "cf", "scf", "hscf", "zso", "hit", "pn", "fo_w", "toi"]
    stringkeys = ["team", ]
    for n in numberkeys:
        ts[n] = 0
    for s in stringkeys:
        ts[s] = ""
    return ts


def get_stats(pbp):
    stats = {}
    missing = set()
    prev_shot = None
    prev_play = None
    for play in pbp:
        # Check for datetime for times
        if type(play["periodTime"]) != type(6):
            play["periodTime"] = play["periodTime"].hour * 60 + play["periodTime"].minute * 60  # Thanks, NHL
        if play["playType"] in ["SHOT", "GOAL", "MISSED_SHOT", "BLOCKED_SHOT"]:
            zone, danger = shot.scoring_chance_standard(play, prev_shot, prev_play)
            if danger == 1:
                stats[play["team_id"]]["scf"] += 1
            elif danger == 2:
                stats[play["team_id"]]["hscf"] += 1


        if play["team_id"] is not None and play["team_id"] not in stats:
            stats[play["team_id"]] = init_team()
        if play["playType"] == "GOAL":
            stats[play["team_id"]]["gf"] += 1
            stats[play["team_id"]]["sf"] += 1
        elif play["playType"] == "SHOT":
            stats[play["team_id"]]["sf"] += 1
        elif play["playType"] == "MISSED_SHOT":
            stats[play["team_id"]]["msf"] += 1
        elif play["playType"] == "BLOCKED_SHOT":
            stats[play["team_id"]]["bsf"] += 1
        else:
            missing.add(play["playType"])


        if play["playType"] in ["SHOT", "GOAL", "MISSED_SHOT", "BLOCKED_SHOT"]:
            prev_shot = play
        prev_play = play

    print missing

    for team in stats:
        td = stats[team]
        td["cf"] = corsi.calc_corsi(td["sf"], td["msf"], td["bsf"], "team.get_stats")

    return stats
            
