import datetime
import json
import os
import socket
import subprocess
import sys
import time
from threading import Thread
from time import strftime

import adafruit_ssd1306
import busio
# Web Scraping Prerequisites
import requests
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont

background_task_started = False
line1 = "Fetching"
line2 = "data..."

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

def getCKPoolData(url, bcAdress, workerName, hrOption, draw):
    # Read JSON from URL
    global background_task_started
    global line1
    global line2

    page = requests.get(url)
    data = page.json()

    try:
        if(workerName != ""):
            workerData = [x for x in data["worker"] if x["workername"] == bcAdress + "." + workerName][0]
        else:
            workerData = data

        line1 = str(workerData["hashrate" + hrOption])
        line2 = str(workerData["bestever"])
    except:
        line1 = "Worker"
        line2 = "not found!"
    
    background_task_started = False

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
doCGMinerAPI = True

#Load Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
withImage = True
try:
    btcLogo = Image.open('btc_logo.png').resize((20, 25), Image.ANTIALIAS)
except:
    withImage = False

#Get given Parameters
url = ""
second = 0
if len(sys.argv) > 1:
    doCGMinerAPI = False
    bcAdress = sys.argv[1]
    workerName = ""
    hrOption = "1hr"
    url = "https://solo.ckpool.org/users/" + bcAdress
    if len(sys.argv) > 2:
        hrOption = sys.argv[2]
    if len(sys.argv) > 3:
        workerName = sys.argv[3]


while True:
    # Get System Infos
    DateTime = strftime("%d.%m.%Y %H:%M:%S")
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True)
    cmd = "free -h | awk 'NR==2{printf \"Mem: %s/%s %.1f%%\", $3,$2,($3/($2*1000))*100}'"
    MemUsage = subprocess.check_output(cmd, shell = True)
    MemUsage = str(MemUsage,'utf-8')
    MemUsage = MemUsage.replace("Mi","M")
    MemUsage = MemUsage.replace("Gi","G")
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True)
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell = True)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # Write System Infos
    draw.text((x, top), DateTime, font=font, fill=255)
    draw.text((x, top+8),  "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((x, top+16), str(CPU,'utf-8') + "  " + str(temp,'utf-8') , font=font, fill=255)
    draw.text((x, top+25), MemUsage, font=font, fill=255)

    # Write CGMiner Stats   
    if doCGMinerAPI:     
        try:
            summary = cgminer.summary()

            y = 0
            if(withImage):
                y = 25
                draw.bitmap((x, top+41), btcLogo, fill=1)

            draw.text((x+y, top+38), "GH/s av: " + '%.2f' % (summary['SUMMARY'][0]['MHS av'] / 1000), font=font, fill=255)
            draw.text((x+y, top+47), "BEST: " + str(summary['SUMMARY'][0]['Best Share']), font=font, fill=255)
            draw.text((x+y, top+56), "BLK: " + str(summary['SUMMARY'][0]['Found Blocks']), font=font, fill=255)

        except:
            if withImage:
                draw.bitmap((x, top+41), btcLogo, fill=1)

            draw.text((x+y, top+44), "Check CGMiner", font=font, fill=255)
            draw.text((x+y, top+52), "process !", font=font, fill=255)
    else:
        #Write CKPool Stats
        try:
            if not background_task_started:
                background_task_started = True
                second = datetime.datetime.now().second
                if url != "":
                    t = Thread(target=getCKPoolData, args=(url, bcAdress, workerName, hrOption, draw))
                    t.start()
            
            y = 0
            if(withImage):
                y = 25
                draw.bitmap((x, top+41), btcLogo, fill=1)

            draw.text((x+y, top+38), "HR " + hrOption + ": " + line1.replace("T", " T").replace("G", " G").replace("M", " M"), font=font, fill=255)
            draw.text((x+y, top+47), "BEST: " + line2, font=font, fill=255)
            draw.text((x+y, top+56), "Worker: " + str(workerName), font=font, fill=255)

        except:
            if withImage:
                draw.bitmap((x, top+41), btcLogo, fill=1)

            draw.text((x+y, top+44), "Check", font=font, fill=255)
            draw.text((x+y, top+52), "parameters!", font=font, fill=255)

    disp.image(image)
    disp.show()
    time.sleep(0.1)
