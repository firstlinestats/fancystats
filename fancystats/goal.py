from corsi import calc_60


def percent(above, below):
    if below != 0:
        return above / below * 100
    else:
        return 0


def goals_for_60(toi, gf):
    """Calculate GF60
    toi - Time On Ice, in seconds
    gf - goals for
    """
    return calc_60(toi, gf, "goals_for_60")


def goals_against_60(toi, ga):
    """Calculate GA60
    toi - Time On Ice, in seconds
    ga - Goals Against
    """
    return calc_60(toi, ga, "goals_against_60")


def goals_for_percent(gf, ga):
    """Calculate GF%
    gf - Goals for
    ga - Goals against
    """
    return percent(gf, gf + ga)


def personal_shot_percent(goals, shots):
    """Calculate PSh%
    goals - Player's Goals
    shots - Individual Shots on Goal
    """
    return percent(goals, shots)


def onice_shot_percent(goals, shots):
    """Calculate OSh%
    goals - On-ice goals for
    shots - On-ice shots on goal
    """
    return percent(goals, shots)


def onice_save_percent(goals, shots):
    """Calculate OSv%
    goals - On-ice goals against
    shots - On-ice shots against
    """
    return percent (goals, shots)
