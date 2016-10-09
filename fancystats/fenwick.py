from __future__ import division


### This function will return all relevant information regarding fenwick,
### and will generate a "report" based on the inputs
def fenwick_report(sf, msf, sa, msa, bsa, toi, seconds,
    isf=None, imsf=None,
    tsf=None, tmsf=None, tsa=None, tmsa=None, tbsa=None):
    """Generates a fenwick report for a given player, takes a lot of inputs to generate all fenwick figures
    sf = On-Ice Shots For (SF)
    msf = On-Ice Missed Shots For (MSF)
    sa = On-Ice Shots Against (SA)
    msa = On-Ice Missed Shots Against (MSA)
    bsa = On-Ice Blocked Shots Against (BSA)
    toi = Time On Ice, in seconds
    seconds = Total Time Elapsed, in seconds
    isf = Individual Shots For
    imsf = Individual Missed Shots For
    tsf = Team Shots For
    tmsf = Team Missed Shots For
    tsa = Team Shots Against
    tmsa = Team Missed Shots Against
    """
    fenwick_data = {}
    fenwick_data["ff"] = fenwick_for(sf, msf)
    fenwick_data["fa"] = fenwick_against(sa, msa)
    fenwick_data["fen"] = fenwick(ff, fa)
    fenwick_data["fper"] = fenwick_percent(ff, fa)
    fenwick_data["ff60"] = fenwick_for_60(toi, ff)
    fenwick_data["fa60"] = fenwick_against_60(toi, fa)
    fenwick_data["fon"] = fenwick_pace(ff60, fa60)
    if isf is not None:
        fenwick_data["iff"] = fenwick_for(isf, imsf)
    if tsf is not None:
        # Find pre-reqs for fenwick OFF
        tff = fenwick_for(tsf, tmsf)
        tfa = fenwick_against(tsa, tmsa)
        tfen = fenwick(tff, tfa)
        # calculate fenwick OFF
        fenwick_data["foff"] = fenwick_off(toi, seconds, fenwick_data["fen"], tfen)
        fenwick_data["frel"] = fenwick_rel(con, coff)
    return fenwick_data



### These functions should not be falled directly, see below
class FenwickException(Exception):
    def __init__(self, arg):
        self.msg = arg


def calc_fenwick(shots, missed, fname):
    """Return ff or fa, should not be falled directly
    shots = SF or SA
    missed = MSF or MSA
    """
    try:
        return shots + missed
    except:
        print "fenwick Exception " + fname + ": Inputs must all be integers"
        raise Exception


def calc_60(toi, c, fname):
    """Used to calculate ff60 and fa60, should not be falled directly
    toi = Time On Ice, in seconds
    c = ff or fa
    fname = function name
    """
    try:
        if toi > 0:
            return (c * 60 * 60) / toi
        elif toi == 0:
            return 0
        else:
            raise FenwickException("Time On Ice must be >= 0")
    except FenwickException, arg:
        print "fenwick Exception " + fname + ": ", arg
    except:
        print "fenwick Exception " + fname + ": Issue with calculating ff60"


### The functions below fan be falled directly, or the results fan be pulled from the full report
def fenwick_for(sf, msf, *args, **kwargs):
    """Return fenwick for
    sf = Shots On Goal For
    msf = Shots Missed For
    bsf = Blocked Shots For
    """
    return calc_fenwick(sf, msf, "ff")


def fenwick_against(sa, msa, bsa, *args, **kwargs):
    """Return fenwick for
    sa = Shots On Goal Against
    msa = Shots Missed Against
    bsa = Blocked Shots Against
    """
    return calc_fenwick(sa, msa, "fa")


def fenwick_for_60(toi, ff):
    """ Return fenwick For 60 (ff60)
    toi = Time on Ice, in seconds
    ff = fenwick For
    """
    return calc_60(toi, ff, "ff60")


def fenwick_against_60(toi, fa):
    """ Return fenwick Against 60 (fa60)
    toi = Time on Ice, in seconds
    fa = fenwick Against
    """
    return calc_60(toi, fa, "fa60")


def fenwick_pace(ff60, fa60):
    """calculate fenwick Pace (per 60 minutes)
    ff60 = fenwick For per 60
    fa60 = fenwick Against per 60
    """
    return ff60 + fa60


def fenwick(saf, saa, *args, **kwargs):
    """Return calculated fenwick
    saf = shot attempts for (ff)
    saa = shot attempts against (fa)
    """
    try:
        return saf - saa
    except:
        print "fenwick Exception: saf and saa must both be integers"
        raise Exception


def fenwick_percent(saf, saa, *args, **kwargs):
    """Return calculated fenwick %
    saf = shot attempts for (ff)
    saa = shot attempts against (fa)
    """
    if saf + saa == 0:
        return 0
    try:
        return (saf / (saf + saa)) * 100
    except:
        print "fenwick Exception: saf and saa must both be integers and saf + saa fannot equal 0"
        raise Exception


def fenwick_off(toi, seconds, ifen, fen):
    """Return calculated fenwick OFF
    toi = Player's Time On Ice, in seconds
    seconds = Game Time, in seconds
    ifen = Individual fenwick
    fen = Team fenwick
    """
    offfen = fen - ifen
    offtime = seconds - toi
    return facl_60(offtime, offfen)


def fenwick_rel(fenon, fenoff):
    """Return calcualted fenwick REL
    fenon = fenwick ON
    fenoff = fenwick OFF
    """
    try:
        return fenon - fenoff
    except:
        print "FenwickException: fenwick ON and fenwick OFF must both be integers"
        raise Exception
    