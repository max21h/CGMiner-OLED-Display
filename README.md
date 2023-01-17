# CGMiner-OLED-Display
Display Raspberry Pi SystemInfos and CGMiner Info's on OLED-Display.
The cgminer data is fetched via CG-Miner API, add --api-listen to your sudo ./cgminer command! For more details check https://github.com/ckolivas/cgminer/blob/master/API-README.

## Requirements
  - Raspberry Pi
  - [0,96 Zoll OLED Display I2C](https://www.amazon.de/dp/B01L9GC470/)
  - [Jumper Wire/Kabel](https://www.amazon.de/dp/B07KYHBVR7/)
## Software Requirements
  ### Update Raspbian
    sudo apt-get update
    sudo apt-get upgrade
    sudo reboot
   ### Activate I2C
    sudo raspi-config
   1. Use the down arrow to select 3 Interface Options 
   2. Arrow down to I5 I2C 
   3. Select yes when it asks you to enable I2C
   4. Use the right arrow to select the Finish button 
   5. Reboot
   ### Install Drivers & Library
    sudo apt install -y python3-dev
    sudo apt install -y python3-pil
    sudo apt install -y python3-pip
    sudo apt install -y python3-setuptools
    sudo apt install -y python3-rpi.gpio
    sudo apt install -y i2c-tools
    sudo pip3 install adafruit-circuitpython-ssd1306
   ### Connect display
    Ground: PIN6
    VCC:    PIN1
    CL:     PIN5
    SDA:    PIN3
    (But you can freely choose GND and VCC, it doesn't matter whether 3.3V or 5V)
   ![image](https://user-images.githubusercontent.com/116381805/198962440-202eca3c-438c-4762-afd5-c4e9b7b451d7.png)
  ### Check display connection
    i2cdetect -y 1
   If your display is detected, you should get the following output:
   ![image](https://user-images.githubusercontent.com/116381805/198963026-cdee3cd2-0f2f-488d-8c33-f48d462910b2.png)
 ## GIT clone BTC-Info-LEDMatrix
    git clone https://github.com/max21h/CGMiner-OLED-Display.git
 ## Start Script
    Before you start this script make sure your cgminer process is running!
    Option 1 (Direct):
      python3 cgMinerStats.py
    Option 2 (Background):
      nohup python3 cgMinerStats.py &
 ## Autostart with rc.local
    Open rc.local
      sudo nano /etc/rc.local
    Add line to r.local
      sudo nohup python3 /yourPath/CGMiner-OLED-Display/cgMinerStats.py &
  ![rc local](https://user-images.githubusercontent.com/116381805/203770650-6f73edcf-cf39-47b1-b236-5b9cf214e70f.png)
    
  ## Default Output
    # System Infos
    - Date and Time (local machine)
    - IP Adress
    - CPU Load and Temp
    - Memory Usage
    
    # CGMiner API (check wiki to set other data)
    - GH/s av (average GH/s)
    - Best (Best Share)
    - BLK (Found Blocks)
  ![oled_display](https://user-images.githubusercontent.com/116381805/203777160-d7d1c403-b89e-495e-8e95-08e60653e07a.png)
  
  ## Paramters for CKPool Output
    python3 cgMinerStats.py [BTC-Adress] [hashrate Option] [workername]
      
    - [bc-Adress] = Your BTC-Adress from CKPool Website (e.g https://solo.ckpool.org/users/bc1qr0qr3mjlsav66a0twq7qpkr....)
    - [hashrate Option] = which hashrate you want to display (e.g. 1m = hashrate1m; 7d = hashrate7d)
    - [workername] = Data of a specific worker will be shown (without this parameter the summary of your given adress will be shown)

    for example: python3 cgMinerStats.py bc1qr0qr3mjlsav66a0twq7qpkrqmc4vwh7mdsXXXXX 5m max21H
  ![ckpool_output](https://user-images.githubusercontent.com/116381805/210548055-5c5ca8cc-7bfc-4ca8-a862-87898a6346b0.jpg)
  
### Donate
![lnurl](https://user-images.githubusercontent.com/116381805/212836865-b4da6e48-48c9-4efd-9ef1-ccd656a38a28.png)
LNURL1DP68GURN8GHJ7MRW9E6XJURN9UH8WETVDSKKKMN0WAHZ7MRWW4EXCUP0X9URVEPHVSCNSVPEXS6R2ETRXE3X2YS85U9

