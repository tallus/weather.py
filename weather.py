#! /usr/bin/env python
"""Downloads NOAA weather reports and outputs them to  a file.

Text based reports are designated by a six letter code

The first three letters designates the report type:

e.g. AFD = Area Forecast Discussion

The last 3 designate the node, roughly corrsponding to location (presumably it
refers to an NOAA weather station) note these are actually designated by a four
letter code, but the first letter is dropped. This is typically K (as in US
call signs*) so it not needed. Thus Portland, Oregon is KPQR but uses PQR in
reports so AFDPQR is the Area Forecast Discussion from the Portland, OR
weather station, and can be found at http://www.nws.noaa.gov/data/PQR/AFDPQR

N.B.
1. Not all reports exists at all nodes
2. When a report does exist it is not always issued/there, eg Alerts etc
3. Some reports have different nodes, PQR offten contains reports for all
of Oregon, but climate data for the city of Portland is at CLIPDX (presumably
data from the Weather Station at PDX airport where actual weather observations
for Portland are taken AFAIK.

* Not an actual callsign. KPQR is a real call sign (for a radio station based
in Portland -- its not the weather station, its an LBTQ community radio
station, Wild Planet Radio KPQR 99.1FM)

Most text reports are found at http://www.nws.noaa.gov/data/[NODE]/[REPORT]
but there are also reports elsewhere, e.g. Space Weather Reports (really)
at http://services.swpc.noaa.gov/text

A list of the major nodes can be derived from e.g.
http://www.nws.noaa.gov/view/validProds.php?prod=AFD

Valid report types:
(not all may have have corresponding text reports"

    Rawinsonde Data above 100 milibars (ABV)
    Administrative Message (ADM)
    Area Forecast Discussion (AFD)
    Area Forecast Matrices (AFM)
    Area Forecast (AFP)
    Agricultural Observations (AGO)
    Space Weather Alert (ALT)
    Air Quality Statement (AQI)
    Avalanche Warning (AVW)
    Airport Weather Warning (AWW)
    Buoy Reports (BOY)
    Broadcast Text (BRT)
    Child Abduction Emergency (CAE)
    Coded Cities Forecast (CCF)
    Preliminary Monthly Climate (CF6)
    Coastal Hazard Message (CFW)
    Coast Guard Surface Report (CGR)
    Climatological Report (Daily) (CLI)
    Climate Summary (CLM)
    Climatological Report (Seasonal) (meteorologically based) (CLS)
    Coastal Waters Forecast (CWF)
    Daily Dispersion Outlook (DDO)
    3 to 5 Day Extended Forecast (EFP)
    Enhanced Forecast/Outlook (EOL)
    Seismic Information (EQI)
    Hydrologic Outlook (ESF)
    Extended Streamflow Prediction (ESP)
    Aviation Area Forecast (FA0)
    Fire Danger Indices (FDI)
    Flood Watch (FFA)
    Flash Flood Guidance (FFG)
    Headwater Guidance (FFH)
    Flash Flood Statement (FFS)
    Flash Flood Warning (FFW)
    Flood Statement (FLS)
    Flood Warning (FLW)
    Free Text Message (FTM)
    Fire Weather Forecast (FWF)
    Miscellaneous Fire Weather Product (FWM)
    Fire Weather Notification (FWN)
    Fire Weather Observation (FWO)
    Fire Weather Spot Forecast (FWS)
    Rawinsonde Freezing Level Data (FZL)
    Great Lakes Forecast (GLF)
    Hydrometeorological Discussion (HMD)
    Hourly Roundup (HRR)
    High Seas Forecast (HSF)
    Hazardous Weather Outlook (HWO)
    Hourly Weather Roundup (HWR)
    Supplementary Temperature & Precipitation Table (HYD)
    Monthly Hydrometeorogical Product (HYM)
    Ice Forecast (ICE)
    Local Climatological Data (LCD)
    Local Cooperative Observation (LCO)
    Local Storm Report (LSR)
    Rawinsonde Observation Mandatory Levels (MAN)
    Mean Areal Precipitation (MAP) (MAP)
    Marine Interpretation Message (MIM)
    Miscellaneous Local Product (MIS)
    METAR Observations (MTR)
    Marine Weather Statement (MWS)
    Marine Weather Message (MWW)
    Short Term Forecast (NOW)
    Non-Precipitation Watch/Warning/Advisory (NPW)
    Nearshore Marine Forecast (NSH)
    Offshore/NAVTEX Forecast (OFF)
    Other Marine Reports (OMR)
    Other Public Products (OPU)
    Daily Cooperative Observer and Automated Station Reports (OSO)
    Point Forecast Matrices (PFM)
    Fire Weather Point Forecast Matrices (PFW)
    HPC Short Range Forecast Discussion (PMD)
    Public Information Statement (PNS)
    Convective Outlook Areal Outline (PTS)
    Recreational Report (REC)
    Record Report (RER)
    Rangeland Fire Danger Forecast (RFD)
    Route Forecast (RFR)
    Red Flag Warning (RFW)
    Hydrometeorological Data Report Part 1 (RR1)
    Hydrometeorological Data Report Part 2 (RR2)
    Hydrometeorological Data Report Part 3 (RR3)
    Hydrometeorological Data Report Part 4 (RR4)
    Hydrometeorological Data Report Part 5 (RR5)
    Hydrometeorological Data Report Part 9 (RR9)
    Supplementary Rainfall Reports (RRM)
    Hydrometeorological Automated Data System Report (RRS)
    Regional Temperature and Precipitation Table (RTP)
    Hydrologic Summary (RVA)
    Daily River and Lake Summary (RVD)
    River Forecast Product (RVF)
    Miscellaneous River Product (RVM)
    River Lake Stages and Forecasts (RVR)
    Hydrologic Statement (RVS)
    Regional Hourly Weather (RWR)
    Regional Weather Summary (RWS)
    Supplementary Climatological Data (SCD)
    State Forecast Product (SFP)
    Tabluar State Forecast (SFT)
    Rawinsonde Observation Significant Levels (SGL)
    Turbulence SIGMET (SIG)
    Satellite Interpretation Message (SIM)
    Smoke Management Weather Forecast (SMF)
    Special Marine Warning (SMW)
    Selected Cities Weather Summary (SCS)
    Special Weather Statement (SPS)
    Surf Forecast (SRF)
    Synoptic Hour Surface Observation (SSM)
    Road Condition Reports (STO)
    State Temperature and Precipitation Table (STP)
    Spot Forecast Request (STQ)
    Severe Thunderstorm Warning (SVR)
    Severe Weather Statement (SVS)
    Severe Weather Outlook (SWO)
    Regional Synopsis (SYN)
    Terminal Aerodrome Forecast (TAF)
    Terminal Alerting Products (TAP)
    Tide Report (TID)
    Tornado Warning (TOR)
    AirMET (WA0)
    Space Weather Warning (WAR)
    Space Weather Watch (WAT)
    Watch County Notification Message (WCN)
    Watch Outline Update (WOU)
    Winter Storm Watch/Warning/Advisory (WSW)
    Watch Status Report (WWA)
    Forecasts in XML (XF0)
    Temperature Extremes in XML (XTE)
    Observations in XML (XOB)
    Zone Forecast (ZFP)

Copyright (C) 2016, Paul Munday.

PO Box 28228, Portland, OR, USA 97228
paul at paulmunday.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
from datetime import datetime
import sys

from pytz import timezone
import requests


def config():
    global OUTPUT, TIMEZONE, VERBOSE
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--output-file', help="Name of output file",
    )
    parser.add_argument(
        '-t', '--timezone', help='timezone', default='America/Los_Angeles'
    )
    parser.add_argument('-v', '--verbose', action="store_true", help='verbose')
    args = parser.parse_args()
    OUTPUT = args.output_file
    TIMEZONE = args.timezone
    VERBOSE = True if args.verbose or not args.output_file else False


def get_urls():
    base_url = "http://www.nws.noaa.gov/data/PQR/"
    forecasts = [
        # "STQPQX", # 404  unknown
        "HWOPQR",
        "WSWPQR",      # winter storm warning
        "SFPOR",
        "AFDPQR",
        "RFWPQR",
        "ZFPPQR",
        "CLIPDX",
        "CF6PDX",
        "LCOPQR",
        "OSOPQR",
        "RRMPDX",
        "RTPPQR",
        "RVSPQR",
        "CWFPQR",
        "FWFPQR",
        "RVMPQR",
        "STQPQR"
    ]

    extra_urls = [
        # space weather
        "http://services.swpc.noaa.gov/text/advisory-outlook.txt",
    ]
    return [base_url + forecast for forecast in forecasts] + extra_urls


def main():
    report = []
    now = datetime.now(timezone(TIMEZONE))
    report.append(now.ctime())
    for url in get_urls():
        if VERBOSE:
            print "fetching {}...".format(url)
        req = requests.get(url)
        data = req.text
        # report not present, doesn't 404
        if not data.startswith('<b>Cannot') or req.status_code != 200:
            report.append(data)
            if VERBOSE:
                print data
        elif VERBOSE:
            print "No report at {}".format(url)
    if OUTPUT:
        try:
            with open(OUTPUT, 'w') as weather:
                for forecast in report:
                    weather.write(forecast)
        except IOError:
            print "Unable to write to file {}".format(OUTPUT)


if __name__ == "__main__":
    config()
    main()
