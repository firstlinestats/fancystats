

TEAMSTRENGTHS_CHOICES = (
    ("even", "Even Strength 5v5"),
    ("all", "All"),
    ("pp", "Power Play"),
    ("pk", "Short Handed"),
    ("4v4", "4v4"),
    ("og", "Opposing Goalie Pulled"),
    ("tg", "Team Goalie Pulled"),
    ("3v3", "3v3")
)

SCORESITUATION_CHOICES = (
    ("all", "All"),
    ("t3+", "Trailing by 3+"),
    ("t2", "Trailing by 2"),
    ("t1", "Trailing by 1"),
    ("t", "Tied"),
    ("l1", "Leading by 1"),
    ("l2", "Leading by 2"),
    ("l3+", "Leading by 3+"),
    ("w1", "Within 1")
)

PERIOD_CHOICES = (
    ("all", "All"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "OT")
)

gameTypes = (
    ("PR", "Pre-Season"),
    ("R", "Regular Season"),
    ("P", "Playoffs"),
    ("A", "All-Star Game")
)

gameStates = (
    ("1", "Preview (Scheduled)"),
    ("2", "Preview (Pre-Game)"),
    ("3", "Live (In Progress)"),
    ("4", "Live (In Progress - Critical)"),
    ("5", "Final (Game Over)"),
    ("6", "Final"),
    ("7", "Final"),
    ("8", "Preview (Scheduled (Time TBD))"),
    ("9", "Preview (Postponed)")
)

playTypes = (
    ("UNKNOWN", "Unknown"),
    ("FACEOFF", "Faceoff"),
    ("HIT", "Hit"),
    ("GIVEAWAY", "Giveaway"),
    ("GOAL", "Goal"),
    ("SHOT", "Shot"),
    ("MISSED_SHOT", "Missed Shot"),
    ("PENALTY", "Penalty"),
    ("PENALTY_END", "Penalty Ended"),
    ("STOP", "Stoppage"),
    ("SUBSTITUTION", "Substitution"),
    ("FIGHT", "Fight"),
    ("TAKEAWAY", "Takeaway"),
    ("BLOCKED_SHOT", "Blocked Shot"),
    ("PERIOD_START", "Period Start"),
    ("PERIOD_END", "Period End"),
    ("GAME_END", "Game End"),
    ("GAME_SCHEDULED", "Game Scheduled"),
    ("PERIOD_READY", "Period Ready"),
    ("PERIOD_OFFICIAL", "Period Official"),
    ("SHOOTOUT_COMPLETE", "Shootout Complete"),
    ("EARLY_INT_START", "Early Intermission Start"),
    ("EARLY_INT_END", "Early Intermission End"),
    ("GAME_OFFICIAL", "Game Official"),
    ("CHALLENGE", "Official Challenge"),
    ("EMERGENCY_GOALTENDER", "Emergency Goaltender"),
)

shotTypes = (
    ("WRIST", "Wrist"),
    ("SNAP", "Snapshot"),
    ("SLAP", "Slapshot"),
    ("BACK", "Backhand"),
    ("TIP", "Tip-In"),
    ("WRAP", "Wrap"),
    ("DEFLECT", "Deflected"),
    ("UNSPECIFIED", "Unspecified")
)

playerTypes = (
    (0, "Unknown"),
    (1, "Winner"),
    (2, "Loser"),
    (3, "Hitter"),
    (4, "Hittee"),
    (5, "Scorer"),
    (6, "Assist"),
    (7, "Shooter"),
    (8, "Goalie"),
    (9, "Blocker"),
    (10, "PenaltyOn"),
    (11, "DrewBy"),
    (12, "ServedBy"),
    (13, "PlayerID"),
    (14, "Fighter"),
    (15, "OnIce"),
    (16, "Assist 2")
)

playerPositions = (
    ("Center", "C"),
    ("Right Wing", "R"),
    ("Left Wing", "L"),
    ("Defender", "D"),
    ("Goalie", "G"),
)

teamNames = (
    (21, 'Avalanche'),
    (16, 'Blackhawks'),
    (29, 'Blue Jackets'),
    (19, 'Blues'),
    (6, 'Bruins'),
    (8, 'Canadiens'),
    (23, 'Canucks'),
    (15, 'Capitals'),
    (53, 'Coyotes'),
    (1, 'Devils'),
    (24, 'Ducks'),
    (20, 'Flames'),
    (4, 'Flyers'),
    (12, 'Hurricanes'),
    (2, 'Islanders'),
    (52, 'Jets'),
    (26, 'Kings'),
    (14, 'Lightning'),
    (10, 'Maple Leafs'),
    (22, 'Oilers'),
    (13, 'Panthers'),
    (5, 'Penguins'),
    (18, 'Predators'),
    (3, 'Rangers'),
    (17, 'Red Wings'),
    (7, 'Sabres'),
    (9, 'Senators'),
    (28, 'Sharks'),
    (25, 'Stars'),
    (30, 'Wild')
)

homeAway = (
    (0, "Home"),
    (1, "Away"),
    (2, "All")
)

events = {
    "FACEOFF": "FAC",
    "HIT": "HIT",
    "GIVEAWAY": "GIVE",
    "GOAL": "GOAL",
    "SHOT": "SHOT",
    "MISSED_SHOT": "MISS",
    "PENALTY": "PENL",
    "STOP": "STOP",
    "SUB": "SUB",
    "FIGHT": "PENL",
    "TAKEAWAY": "TAKE",
    "BLOCKED_SHOT": "BLOCK",
    "PERIOD_START": "PSTR",
    "PERIOD_END": "PEND",
    "GAME_END": "GEND",
    "GAME_SCHEDULED": "GAME_SCHEDULED",
    "PERIOD_READY": "PERIOD_START",
    "PERIOD_OFFICIAL": "PERIOD_OFFICIAL",
    "SHOOTOUT_COMPLETE": "SOC",
    "EARLY_INT_START": "EISTR",
    "EARLY_INT_END": "EIEND",
    "GAME_OFFICIAL": "GOFF",
    "CHALLENGE": "CHL",
    "EMERGENCY_GOALTENDER": "EMERGENCY_GOALTENDER"
}
