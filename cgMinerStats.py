import socket
import json
import sys
import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from time import strftime

class CgminerAPI(object):
    """ Cgminer RPC API wrapper. """
    def __init__(self, host='localhost', port=4028):
        self.data = {}
        self.host = host
        self.port = port

    def command(self, command, arg=None):
        """ Initialize a socket connection,
        send a command (a json encoded dict) and
        receive the response (and decode it).
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self.host, self.port))
            payload = {"command": command}
            if arg is not None:
                # Parameter must be converted to basestring (no int)
                payload.update({'parameter': arg})

            sock.send(json.dumps(payload).encode())
            received = self._receive(sock)
        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

        return json.loads(received[:-1])

    def _receive(self, sock, size=4096):
        msg = ''
        while 1:
            chunk = sock.recv(size).decode()
            if chunk:
                msg += chunk
            else:
                break
        return msg

    def __getattr__(self, attr):
        """ Allow us to make command calling methods.
        >>> cgminer = CgminerAPI()
        >>> cgminer.summary()
        """
        def out(arg=None):
            return self.command(attr, arg)
        return out

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height. 
# Change these to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

#CGMiner API
cgminer = CgminerAPI()

#Load Image
withImage = True
try:
    btcLogo = Image.open('btc_logo.png').resize((20, 25), Image.ANTIALIAS)
except:
    withImage = False

while True:
    # Get System Infos
    DateTime = strftime("%d.%m.%Y %H:%M:%S")
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True)
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True)
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell = True)

    summary = cgminer.summary()
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    #Write System Infos
    draw.text((x, top), DateTime, font=font, fill=255)
    draw.text((x, top+10),  "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((x, top+20), str(CPU,'utf-8') + " " + str(temp,'utf-8') , font=font, fill=255)
    draw.text((x, top+30), str(MemUsage,'utf-8'), font=font, fill=255)

    #Write BTC Infos
    if withImage:
        draw.bitmap((x, top+45), btcLogo, fill=1)
        draw.text((x+25, top+40), "GH/s av: " + '%.2f' % (summary['SUMMARY'][0]['MHS av'] / 1000), font=font, fill=255)
        draw.text((x+25, top+50), "BEST: " + str(summary['SUMMARY'][0]['Best Share']), font=font, fill=255)
        draw.text((x+25, top+60), "BLK: " + str(summary['SUMMARY'][0]['Found Blocks']), font=font, fill=255)
    else: #if btcLogo is not available
        draw.text((x, top+40), "GH/s av: " + '%.2f' % (summary['SUMMARY'][0]['MHS av'] / 1000), font=font, fill=255)
        draw.text((x, top+50), "BEST: " + str(summary['SUMMARY'][0]['Best Share']), font=font, fill=255)
        draw.text((x, top+60), "BLK: " + str(summary['SUMMARY'][0]['Found Blocks']), font=font, fill=255)

    disp.image(image)
    disp.show()
    time.sleep(0.1)
