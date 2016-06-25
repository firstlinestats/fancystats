

### This function will return all relevant information regarding corsi,
### and will generate a "report" based on the inputs
def corsi_report(sf, msf, bsf, sa, msa, bsa, toi, seconds,
    tsf=None, tmsf=None, tbsf=None, tsa=None, tmsa=None, tbsa=None):
    """Generates a corsi report for a given player, takes a lot of inputs to generate all corsi figures
    sf = On-Ice Shots For (SF)
    msf = On-Ice Missed Shots For (MSF)
    bsf = On-Ice Blocked Shots For (BSF) ((Shots This Team took that were blocked!))
    sa = On-Ice Shots Against (SA)
    msa = On-Ice Missed Shots Against (MSA)
    bsa = On-Ice Blocked Shots Against (BSA)
    toi = Time On Ice, in seconds
    seconds = Total Time Elapsed, in seconds
    tsf = Team Shots For
    tmsf = Team Missed Shots For
    tbsf = Team Blocked Shots For
    tsa = Team Shots Against
    tmsa = Team Missed Shots Against
    tbsa = Team Blocked Shots Against
    """
    corsi_data = {}
    corsi_data["cf"] = corsi_for(sf, msf, bsf)
    corsi_data["ca"] = corsi_against(sa, msa, bsa)
    corsi_data["cor"] = corsi(cf, ca)
    corsi_data["cper"] = corsi_percent(cf, ca)
    corsi_data["cf60"] = corsi_for_60(toi, cf)
    corsi_data["ca60"] = corsi_against_60(toi, ca)
    corsi_data["con"] = corsi_pace(cf60, ca60)
    if tsf is not None:
        # Find pre-reqs for Corsi OFF
        tcf = corsi_for(tsf, tmsf, tbsf)
        tca = corsi_against(tsa, tmsa, tbsa)
        tcor = corsi(tcf, tca)
        # Calculate Corsi OFF
        corsi_data["coff"] = corsi_off(toi, seconds, cor, tcor)
        corsi_data["crel"] = corsi_rel(con, coff)
    return corsi_data



### These functions should not be called directly, see below
class CorsiException(Exception):
    def __init__(self, arg):
        self.msg = arg


def calc_corsi(shots, missed, blocked, fname):
    """Return CF or CA, should not be called directly
    shots = SF or SA
    missed = MSF or MSA
    blocked = BSF or BSA
    """
    try:
        return shots + missed + blocked
    except:
        print "Corsi Exception " + fname + ": Inputs must all be integers"
        raise Exception


def calc_60(toi, c, fname):
    """Used to calculate CF60 and CA60, should not be called directly
    toi = Time On Ice, in seconds
    c = CF or CA
    fname = function name
    """
    try:
        if toi > 0:
            return (c * 60 * 60) / toi
        elif toi == 0:
            return 0
        else:
            raise CorsiException("Time On Ice must be >= 0")
    except CorsiException, arg:
        print "Corsi Exception " + fname + ": ", arg
    except:
        print "Corsi Exception " + fname + ": Issue with calculating CF60"


### The functions below can be called directly, or the results can be pulled from the full report
def corsi_for(sf, msf, bsf, *args, **kwargs):
    """Return corsi for
    sf = Shots On Goal For
    msf = Shots Missed For
    bsf = Blocked Shots For
    """
    return calc_corsi(sf, msf, bsf, "CF")


def corsi_against(sa, msa, bsa, *args, **kwargs):
    """Return corsi for
    sa = Shots On Goal Against
    msa = Shots Missed Against
    bsa = Blocked Shots Against
    """
    return calc_corsi(sa, msa, bsa, "CA")


def corsi_for_60(toi, cf):
    """ Return Corsi For 60 (CF60)
    toi = Time on Ice, in seconds
    cf = Corsi For
    """
    return calc_60(toi, cf, "CF60")


def corsi_against_60(toi, ca):
    """ Return Corsi Against 60 (CA60)
    toi = Time on Ice, in seconds
    ca = Corsi Against
    """
    return calc_60(toi, ca, "CA60")


def corsi_pace(cf60, ca60):
    """Calculate Corsi Pace (per 60 minutes)
    cf60 = Corsi For per 60
    ca60 = Corsi Against per 60
    """
    return cf60 + ca60


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


def corsi_off(toi, seconds, icor, cor):
    """Return calculated Corsi OFF
    toi = Player's Time On Ice, in seconds
    seconds = Game Time, in seconds
    icor = Individual Corsi
    cor = Team Corsi
    """
    offcor = cor - icor
    offtime = seconds - toi
    return cacl_60(offtime, offcor)


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
    