# Convert Input values to SI's (Standard units)
#
import math
# Other Functions for this Module
def KTS_to_MS(x): return x * .514447
def MPH_to_MS(x): return x * .44704
def KPH_to_MS(x): return x * .2777778
def FT_to_M(x): return x * .3048
def FAT_to_M(x): return x * 1.829
def MTR_to_M(x): return x * 1
def NMI_to_M(x): return x * 1852
def MI_to_M(x): return x * 1609.344
def KM_to_M(x): return x * 1000
def DEG_to_RAD(x): return math.radians(x)
def DegF_to_Kelvin(x): return ((x - 32) * 5 / 9) + 273.15
def DegC_to_Kelvin(x): return (x + 273.15)
def HrMin_to_Sec(time_str):
    h, m = time_str.split(':')
    return int(h) * 3600 + int(m) * 60
def MinSec_to_Sec(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

#
newValue = ""
# now to the main code
class sigUnits:
    def __init__(self, dataValue, dataUnits):
        sigUnits.newValue = dataValue
    # Convert Knots _to_ m/s
        if dataUnits == "KTS":
            sigUnits.newValue = KTS_to_MS(dataValue)
    # Convert MPH _to_ m/s
        elif dataUnits == "MPH":
            sigUnits.newValue = MPH_to_MS(dataValue)
    # Convert KPH _to_ m/s
        elif dataUnits == "KPH":
            sigUnits.newValue = KPH_to_MS(dataValue)
    # Convert Feet _to_ Meters
        elif dataUnits == "FT":
            sigUnits.newValue = FT_to_M(dataValue)
    # Convert Fathom _to_ Meters
        elif dataUnits == "FAT":
            sigUnits.newValue = FAT_to_M(dataValue)
    # Convert Nautical miles to Meters
        elif dataUnits == "NMI":
            sigUnits.newValue = NMI_to_M(dataValue)
    # Convert Staute Miles _to_ Meters
        elif dataUnits == "MI":
            sigUnits.newValue = MI_to_M(dataValue)
    # Convert Kilometers _to_ Meters
        elif dataUnits == "KM":
            sigUnits.newValue = KM_to_M(dataValue)
    # Convert Degrees _to_ Radians
        elif dataUnits == "DEG":
            sigUnits.newValue = DEG_to_RAD(dataValue)
    # Convert Deg F _to_ Kelvin
        elif dataUnits == "`F":
            sigUnits.newValue = DegF_to_Kelvin(dataValue)
    # Convert Deg C _to_ Kelvin
        elif dataUnits == "`C":
            sigUnits.newValue = DegC_to_Kelvin(dataValue)
    # Convert Meter to Meter
        elif dataUnits == "MTR":
            sigUnits.newValue = MTR_to_M(dataValue)
    # Convert Hours:Minutes to Seconds
        elif dataUnits == "H:M":
            sigUnits.newValue = HrMin_to_Sec(dataValue)
    # Convert Minute:Seconds to Seconds
        elif dataUnits == "M:S":
            sigUnits.newValue = MinSec_to_Sec(dataValue)
        else:
            sigUnits.newValue = dataValue
            # print("Conversion Not Found for:", dataUnits)
# and return the adjusted values