# Mini-Rover Project

## Overview
This project is a **mini-rover** built on a **Raspberry Pi 5**, using the **CoKoino chassis** and the **CoKoino Pi Power 4WD Hat**. The rover is controlled remotely via an **Android gamepad app** over a **TCP socket connection**. Additionally, it is equipped with a **PiCamera**, enabling **real-time video streaming** over a **UDP socket**.

## Features
- **Remote control** using an Android gamepad app
- **Real-time video streaming** from the PiCamera over UDP
- **4WD motor control** via the CoKoino Pi Power 4WD Hat
- **Bidirectional communication** using **TCP and UDP sockets**
- **Python-based implementation** with modular and scalable design

## Hardware Components
- **Raspberry Pi 5**
- **CoKoino Chassis**
- **CoKoino Pi Power 4WD Hat**
- **PiCamera (Raspberry Pi Camera Module)**
- **Android device** (for gamepad app control)
- **Power supply and battery pack**

## Software Components
- **Python** for the rover control logic
- **Sockets (TCP & UDP)** for communication
- **OpenCV & libcamera** for video streaming
- **PyBluez** for Bluetooth functionalities (work in progress)

## System Architecture
1. **Gamepad App (Android Device)**:
   - Sends control commands over a **TCP socket** to the rover
2. **Raspberry Pi (Rover Controller)**:
   - Receives commands and translates them into motor actions
   - Streams video from the PiCamera over **UDP socket**
3. **Communication**:
   - **TCP Socket**: Used for receiving control inputs
   - **UDP Socket**: Used for low-latency video streaming

## Installation
### 1. Set up the Raspberry Pi
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip
```

### 2. Clone the Repository
```sh
git clone https://github.com/Cyrus243/PathFinder.git
cd pathFinder
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the Rover Control Server
```sh
python3 main.py
```

## Usage
1. **Start the rover server** to accept control commands.
2. **Start the video stream** for real-time monitoring.
3. **Connect the Android gamepad app** to the Raspberry Pi's IP over TCP.
4. **Control the rover remotely** and view the live camera feed.

## Future Improvements
- Introduce **BLE control configuration as an alternative communication method**
- Improve **video streaming performance** using optimized encoding
- Implement **computer vision-based obstacle avoidance**
- Add **autonomous navigation modes**

## License
This project is licensed under the **MIT License**.

## Author
Aaron Mbala

