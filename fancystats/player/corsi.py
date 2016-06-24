

class CorsiException(Exception):
    def __init__(self, arg):
        self.msg = arg


def corsi_for(sf, msf, bsf, *args, **kwargs):
    """Return corsi for
    sf = Shots On Goal For
    msf = Shots Missed For
    bsf = Blocked Shots For
    """
    try:
        return sf + msf + bsf
    except:
        print "Corsi Exception: sf, msf, and bsf must all be integers"
        raise Exception


def corsi_against(sa, msa, bsa, *args, **kwargs):
    """Return corsi for
    sa = Shots On Goal Against
    msa = Shots Missed Against
    bsa = Blocked Shots Against
    """
    try:
        return sa + msa + bsa
    except:
        print "Corsi Exception: sa, msa, and bsa must all be integers"
        raise Exception


def corsi(saf, saa, *args, **kwargs):
    """Return calculated corsi
    saf = shot attempts for (CF)
    saa = shot attempts against (CA)
    """
    try:
        return saf - saa
    except:
        print "Corsi Exception: saf and saa must both be integers"
        raise Exception


def corsi_percent(saf, saa, *args, **kwargs):
    """Return calculated Corsi %
    saf = shot attempts for (CF)
    saa = shot attempts against (CA)
    """
    if saf + saa == 0:
        return 0
    try:
        return (saf / (saf + saa)) * 100
    except:
        print "Corsi Exception: saf and saa must both be integers and saf + saa cannot equal 0"
        raise Exception


def corsi_on(toi, cor, *args, **kwargs):
    """Return calculated Corsi ON
    toi = Time On Ice, in seconds
    cor = Corsi
    """
    try:
        if toi > 0:
            return (cor * 60 * 60) / toi
        elif toi == 0:
            return 0
        else:
            raise CorsiException("corsi_on requires the player to have been on the ice (toi value greater than 0).")
    except CorsiException, arg:
        print "Corsi Exception: ", arg.msg


def corsi_off(toi, seconds, icor, cor):
    """Return calculated Corsi OFF
    toi = Player's Time On Ice, in seconds
    seconds = Game Time, in seconds
    icor = Individual Corsi
    cor = Team Corsi
    """
    offcor = cor - icor
    offtime = seconds - toi
    return corsi_on(offtime, offcor)


def corsi_rel(coron, coroff):
    """Return calcualted Corsi REL
    coron = Corsi ON
    coroff = Corsi OFF
    """
    try:
        return coron - coroff
    except:
        print "Corsi Exception: Corsi ON and Corsi OFF must both be integers"
        raise Exception

    