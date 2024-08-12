import serial, threading

BYTE_CODES = {
    'SYNC': b'\xaa',
    'EXCODE': b'\x55',
    'POOR_SIGNAL': b'\x02',
    'ATTENTION': b'\x04',
    'MEDITATION': b'\x05',
    'BLINK': b'\x16',
    'RAW_VALUE': b'\x80',
    'ASIC_EEG_POWER': b'\x83',
    'CONNECT': b'\xc0',
    'DISCONNECT': b'\xc1',
    'HEADWEAR_CONNECT': b'\xd0',
}


class Headwear:
    """
    A Professor X headwear
    """

    class DongleListener(threading.Thread):
        """
        Serial listener for USB Dongle
        """

        def __init__(self, headwear, *args, **kwargs):
            """
            Set up the listener device
            """
            self.headwear = headwear
            super(Headwear.DongleListener, self).__init__(*args, **kwargs)

        def run(self):
            """
            Run the listener thread
            """
            s = self.headwear.dongle
            self.headwear.running = True
            s.write(BYTE_CODES['DISCONNECT'])
            curr_settings = s.getSettingsDict()
            for _ in range(2):
                curr_settings['rtscts'] = not curr_settings['rtscts']
                s.applySettingsDict(curr_settings)

            while self.headwear.running:
                # Keep reading bytes till HEADER packet found
                if s.read() == BYTE_CODES['SYNC'] and s.read() == BYTE_CODES['SYNC']:
                    while True:
                        # Getting PLENGTH byte of the HEADER
                        plength = ord(s.read())
                        if plength != ord(BYTE_CODES['SYNC']):
                            # If PLENGTH is SYNC byte, repeat getting PLENGTH byte
                            break
                    if plength > 170:
                        # If PLENGTH is bigger than SYNC byte, find new DATA packet
                        continue
                    # Get the PAYLOAD bytes using PLENGTH byte
                    payload = s.read(plength)
                    # Sum up each byte found in the PAYLOAD bytes
                    chksum_acc = sum([byte for byte in payload])
                    # Take lowest 8 bits and invert them
                    chksum_acc &= 0xff
                    chksum_acc = ~chksum_acc & 0xff
                    # Get CHKSUM byte for validation
                    chksum = ord(s.read())
                    if chksum_acc == chksum:
                        # Check if PAYLOAD is valid
                        self.parse_payload(payload)

            if s and s.isOpen():
                s.close()

        def parse_payload(self, payload):
            """
            Parse the payload
            """
            while payload:
                code, payload = payload[0], payload[1:]
                if code < ord(BYTE_CODES['RAW_VALUE']):
                    # Single-Byte CODES
                    try:
                        val, payload = payload[0], payload[1:]
                    except Exception:
                        pass
                    if code == ord(BYTE_CODES['POOR_SIGNAL']):
                        old_poor_signal = self.headwear.poor_signal
                        self.headwear.poor_signal = val
                        if self.headwear.poor_signal > 0:
                            if old_poor_signal == 0:
                                for handler in self.headwear.poor_signal_handlers:
                                    handler(self.headwear, self.headwear.poor_signal)
                        else:
                            if old_poor_signal > 0:
                                for handler in self.headwear.good_signal_handlers:
                                    handler(self.headwear, self.headwear.poor_signal)
                    elif code == ord(BYTE_CODES['ATTENTION']):
                        self.headwear.attention = val
                        for handler in self.headwear.attention_handlers:
                            handler(self.headwear, self.headwear.attention)
                    elif code == ord(BYTE_CODES['MEDITATION']):
                        self.headwear.meditation = val
                        for handler in self.headwear.meditation_handlers:
                            handler(self.headwear, self.headwear.meditation)
                    elif code == ord(BYTE_CODES['BLINK']):
                    # elif code == '16':
                        self.headwear.blink = val
                        for handler in self.headwear.blink_handlers:
                            handler(self.headwear, self.headwear.blink)
                else:
                    # Multi-Byte CODES
                    try:
                        vlength, payload = payload[0], payload[1:]
                    except Exception:
                        continue
                    val, payload = payload[:vlength], payload[vlength:]
                    if code == ord(BYTE_CODES['RAW_VALUE']):
                        raw = val[0] * 256 + val[1]
                        if (raw := val[0] * 256 + val[1]) >= 32768:
                            raw -= 65536
                        self.headwear.raw_value = raw
                        self.headwear.raw_value_voltage = ((raw * (1.8 / 4096)) / 2000)
                        for handler in self.headwear.raw_value_handlers:
                            handler(self.headwear, self.headwear.raw_value)
                    elif code == ord(BYTE_CODES['ASIC_EEG_POWER']):
                        j = 0
                        for i in ['delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']:
                            self.headwear.waves[i] = (val[j] * 255 * 255) + (val[j + 1] * 255) + val[j + 2]
                            j += 3
                        for handler in self.headwear.waves_handlers:
                            handler(self.headwear, self.headset.waves)
                    elif code == ord(BYTE_CODES['HEADWEAR_CONNECT']):
                        run_handlers = self.headwear.status != 'connected'
                        self.headwear.status = 'connected'

    def __init__(self, device, open_serial=True):
        """
        Initialize the headwear
        """
        self.dongle = None
        self.listener = None
        self.device = device
        self.poor_signal = 255
        self.attention = 0
        self.meditation = 0
        self.blink = 0
        self.raw_value = 0
        self.raw_value_voltage = 0
        self.waves = {}
        self.status = None
        self.running = False
        self.poor_signal_handlers = []
        self.good_signal_handlers = []
        self.attention_handlers = []
        self.meditation_handlers = []
        self.blink_handlers = []
        self.raw_value_handlers = []
        self.waves_handlers = []

        if open_serial:
            self.serial_open()

    def serial_open(self):
        if not self.dongle or not self.dongle.isOpen():
            self.dongle = serial.Serial(self.device, 9600)
        if not self.listener or not self.listener.isAlive():
            self.listener = self.DongleListener(self)
            self.listener.daemon = True
            self.listener.start()

    def serial_close(self):
        self.dongle.close()

    def stop(self):
        self.running = False
