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


def check_play(self, home, away, play_id, teamStrengths, scoreSituation, hsc, asc):
    hb = False
    ab = False
    if play_id in home:
        hp = home[play_id]["count"]
        ap = away[play_id]["count"]
        hg = home[play_id]["goalie"]
        ag = away[play_id]["goalie"]
        if teamStrengths is None or teamStrengths == "all":
            hb, ab = True, True
        elif teamStrengths == "4v4" and hp == 5 and ap == 5:
            hb, ab = True, True
        elif teamStrengths == "even" and hp == ap and hp == 6:
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
        elif teamStrengths == "3v3" and hp == 4 and ap == 4:
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
    return hb, ab


def get_stats(pbp, homeTeam, awayTeam):
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
            if danger < 3:
                stats[play["team_id"]]["scf"] += 1
            else:
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
        elif play["playType"] == "FACEOFF":
            if play["period"] % 2 == 0:
                play["xcoord"] = -play["xcoord"]
            if play["xcoord"] < -25.00:
                stats[awayTeam]["zso"] += 1
            elif play["xcoord"] > 25.00:
                stats[homeTeam]["zso"] += 1
            stats[play["team_id"]]["fo_w"] += 1
        elif play["playType"] == "HIT":
            stats[play["team_id"]]["hit"] += 1
        elif play["playType"] == "PENALTY":
            stats[play["team_id"]]["pn"] += 1
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
            
