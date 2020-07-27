# Signal K Plugin to Convert SIGBUS Strings to Signal K Paths
# by Chuck Bowers - Rhumb Runner J/29 - San Diego, CA
#
# Revsion 0.5.0
#
# Module uses a dict created by the SK plugin configuration
# This module only covers the ones I feel are best suited
# for conversion to SK at this time. I might need to handle
# obscure channels with no clear path / data type conversion
#
# See section 3.1.3 of the SL425 Manual for info on parameters
# This module will automatically subscribe to any channels that
# are enabled in the config JSON and will unsubscibe any that
# are disabled.
#
# This plugin expects a serial to USB converter to be used (/dev/ttyUSB0)
# if your setup is different this will need to change.
#
import ConvertToSI
import serial
import json
import sys
from pathlib import Path

data_folder = Path("/home/pi/.signalk/plugin-config-data")
file_to_open = data_folder / "sk-plugin-sigbus-parser.json"

with open(file_to_open, "r") as read_file:
    SK_Plugin_config = json.load(read_file)
# print(json.dumps(SK_Plugin_config, indent=2))

parse_enabled = SK_Plugin_config['enabled']

logging = SK_Plugin_config['enableLogging']
debug = SK_Plugin_config['enableDebug']
configuration = SK_Plugin_config['configuration']
# print('log =', logging,'debug =', debug,'config =', configuration)

config_array = configuration['multipleParametersArray']
sigbusParameterAndSKPath = {}
Subscribe_dict = {}

for channel in config_array:
    if channel["Sigbus"]:
        sigbusParameterAndSKPath[channel["Sigbus"]]= channel["Sk_Path"]
        Subscribe_dict[channel["Sigbus"]] = channel["Subscribe"]

ser = serial.Serial('/dev/ttyUSB0', 9600)

# Verify that the required Sigbus channels are subscribed to...
sWrite = ''
for s_channel, s_state  in Subscribe_dict.items():
    if s_state == True:
        sWrite = ('$$I' + s_channel + '\r').encode()
        ser.write(sWrite)
        # print(bytes.hex(sWrite))
        # print(sWrite)
    if s_state == False:
        sWrite = ('$$R' + s_channel + '\r').encode()
        ser.write(sWrite)
        # print(bytes.hex(sWrite))
        # print(sWrite)

# ##### the original Master list before moving to SK plugin configurable
# sigbusParameterAndSKPath = {
#    'A': 'navigation.speedThroughWater',  # Single Transducer - less accurate
#    'B': 'navigation.speedThroughWater',  # Double Transducer - more accurate
#    'C': 'environment.depth.belowTransducer',
#    'D': 'environment.wind.speedApparent',
#    'E': 'environment.wind.angleApparent',
#    'F': 'navigation.headingMagnetic',
#    'G': 'navigation.attitude',
#    'H': 'environment.water.temperature',
#    'W': 'environment.wind.speedTrue',
#    'X': 'environment.wind.angleTrueWater',
#    'Z': 'environment.wind.directionMagnetic',
#    'S': 'navigation.log',
#    'R': 'performance.polarSpeed',
#    'T': 'performance.targetSpeed',
#    'Y': 'performance.tackMagnetic',
#    'a': 'some.path',  # Signet sytem time would be sent a text unless I decide to treat differntly
#    'b': 'navigation.racing.timeToStart',  # Signet Count down timer converted to Seconds
#    'd': 'some.path',  # Dead Reckoning Distance Since last reset
#    'e': 'some.path',  # Estimated Bearing to return to DR initial position
#    'h': 'navigation.trip.log',
#    'v': 'performance.velocityMadeGood',
#    'y': 'navigation.trip.lastReset',   # best place I found to hold Elapsed Time sent as text
#   '\x01': 'electrical.batteries.house.voltage'  # Change battery bank as appropriate
#    }

skData = ''

# ########## MODULE WILL ONLY READ DATA IF ENABLED IN SK PLUGIN CONFIGURATION #############

while parse_enabled is True:
    serial_line = ser.readline()
    serial_line = serial_line.decode('ascii', errors='ignore')
    if len(serial_line) > 10 and serial_line[2] == 'd':
        # process only SIGBUS data strings leave the rest alone (for now???)
        # A NORMAL SIGBUS data string is like "$Rd 0.00KTS\x0D\x0A\x0A"
        # Set Up the Captured Data
        Signet_Param = serial_line[1]
        if Signet_Param == "E" or Signet_Param == "X" or Signet_Param == "g":
            # these have a P or S to indicate Port or Stbd Angles before the data
            dirPortStbd = serial_line[3]
            Signet_Data = serial_line[4:8].replace(" ", "")
        else:
            Signet_Data = serial_line[3:8].replace(" ", "")
        Signet_Units = serial_line[8:11].replace(" ", "")
        if "?" in Signet_Data:
            # Question marks are sometimes thrown in if Data is questionable or missing sensor data
            Signet_Data = Signet_Data.replace("?", "")
        if ":" in Signet_Data:
            # Handle ':' which indicates time data
            Signet_Data = Signet_Data
        elif "." in Signet_Data:
            # Handle Data with a decimal point
            Signet_Data = float(Signet_Data)
        else:
            # All else should be just integers
            Signet_Data = int(Signet_Data)
# Now with Clean Data Find out where to send it to SK. Ignore anything not in dict.
        for sParam, SKPath in sigbusParameterAndSKPath.items():
            if sParam == Signet_Param:
                ConvertToSI.sigUnits(Signet_Data, Signet_Units)
                if Signet_Param == 'G':
                    # the G parameter is for Heel which has a SK sub-paths
                    skData = '{"updates": [{ "values": [{"path": "' + SKPath + '","value": {"roll":' + str(ConvertToSI.sigUnits.newValue) + '}}]}]}'
                elif Signet_Param.islower() is True:
                    if Signet_Param == 'a' or Signet_Param == 'y':
                        # these Parameter are a time string for the moment
                        skData = '{"updates": [{ "values": [{"path": "' + SKPath + '","value": "' + str(ConvertToSI.sigUnits.newValue) + '"}]}]}'
                else:
                    # the rest convert to straight SK paths
                    skData = '{"updates": [{ "values": [{"path": "' + SKPath + '","value": ' + str(ConvertToSI.sigUnits.newValue) + '}]}]}'
                break
        serial_dict = json.loads(skData.encode('ascii', 'strict'))
        sys.stdout.write(json.dumps(serial_dict))
        sys.stdout.write('\n')
        sys.stdout.flush()
        # sTest = skData.encode('ascii', 'strict')
        # print(sTest)