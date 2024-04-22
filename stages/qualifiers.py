from confederations.afc import afc
from confederations.caf import caf
from confederations.concacaf import concacaf
from confederations.conmebol import conmebol
from confederations.ofc import ofc
from confederations.uefa import uefa
from functions.knockout import knockout
from stages.inter_continental_playoff import icp
import pandas as pd


def complete_qualifiers(data, settings):
    afc_qual, afc_icp = afc(data, settings)
    caf_qual, caf_icp = caf(data, settings)
    conc_qual, conc_icp = concacaf(data, settings)
    conm_qual, conm_icp = conmebol(data, settings)
    ofc_qual, ofc_icp = ofc(data, settings)
    uefa_qual = uefa(data, settings)

    qualified = afc_qual + caf_qual + conc_qual + conm_qual + ofc_qual + uefa_qual
    qualified_icp = afc_icp + caf_icp + conc_icp + conm_icp + ofc_icp

    icp_winners = icp(data, qualified_icp, settings)

    wc_teams = ['USA', 'Mexico', 'Canada'] + qualified + icp_winners
    print(f"\nQualified for the World Cup: {', '.join(wc_teams)}")
    print(len(wc_teams))

    return data, wc_teams
