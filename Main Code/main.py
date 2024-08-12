# MODULES
import serial, json, time

from datetime import datetime as dt
import csv

import eeg as eg

# SETTIGNS
treshold = 73.2

# COMMANDS
def commandFunction(eeg):

    while eeg != None:

        if eeg.attention >= treshold:
            direction = 'Forward'
            command = 1
        else:
            direction = 'Stop'
            command = 0
                
        return command, direction

def mapValues(val):
    return int(
        max(0, min(100, (int(val))) / 100 * 255
        )
    )

#MAIN
if __name__ == '__main__':
    start＿time = dt.now().strftime('%Y-%m-%d_%H:%M:%S')

    with open(f'BioPin-v3 {start_time}.csv', 'w+') as f:
        header = ['TIME','ATTENTION','POOR SIGNAL','OUTPUT COMMAND','DIRECTION']
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(header)

    is_connected = 0
    while True:

        with open('UI/bt.json', 'w+') as f:
            json.dump({'is_connected': is_connected}, f)

        if is_connected == 0:
            try:
                eeg = eg.Headwear('/dev/rfcomm1')
                mtr = serial.Serial('/dev/ttyACM0', 9600)
                print('Devices Connected')
                is_connected = 1
                time.sleep(1)
            except:
                is_connected = 0
                print('Devices not Connected')
                time.sleep(1)

        elif is_connected == 1:
            try:
                command, direction = commandFunction(eeg)
            except:
                is_connected = 0
                break

            with open('UI/eeg.json', 'w+') as f:
                json.dump({'value': eeg.attention}, f)

            with open('UI/direction.json', 'w+') as f:
                json.dump({'direction': direction}, f)

            with open('UI/data.json') as f:
                data = json.load(f)
                speed = data['combinedValues']

            command_new = str(command) + ':' + str(mapValues(speed))

            print(f'TIME: {dt.now().strftime('%H:%M:%S')} |'
                  f'ATTENTION: {eeg.attention:2d} |', 
                  f'POOR_SIGNAL: {eeg.poor_signal} ||',
                  f'COMMANND: {command_new}',
                  f'|| {direction}')

            data = []
            with open(f'BioPin-v3_{start_time}.csv', 'a+') as f:
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                data.append(dt.now().strftime('%H:%M:%S'))
                data.append(eeg.attention)
                data.append(eeg.poor_signal)
                data.append(command_new)
                data.append(direction)
                writer.writerow(data)
                data = []

            time.sleep(1)
            try:
                if command != 0:
                    mtr.write(str(command_new).encode('utf-8'))
            except KeyboardInterrupt:
                mtr.write('0'.encode('utf-8'))
