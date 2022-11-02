# CGMiner-OLED-Display
Display Raspberry Pi SystemInfos and CGMiner Info's on OLED-Display.
The cgminer data is fetched via CG-Miner API, add --api-listen to your sudo ./cgminer command! For more details check https://github.com/ckolivas/cgminer/blob/master/API-README.

## Requirements
  - Raspberry Pi
  - [0,96 Zoll OLED Display I2C](https://www.amazon.de/dp/B01L9GC470/)
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
  ![example](https://user-images.githubusercontent.com/116381805/198964891-1662f4e6-c638-4b19-9baa-a0cec491e8a3.png)
  

### Donate
<img width="573" alt="image" src="https://user-images.githubusercontent.com/116381805/197489090-9f5e78f4-6c32-43b0-b544-67ccea1c12f3.png">

