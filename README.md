# Mediapipe for hand gestures recognition
Inspired by the YouTube lesson "Control of Real-World Objects with Gesture Recognition in Mediapipe" of Paul McWhorter.

* AI for Everyone LESSON 29: Control of Real-World Objects with Gesture Recognition in Mediapipe:

  <https://youtu.be/OgiYbcGaDEI?si=hR3IWCkkyGVehwjz>

##

## Setup Environment
* Laptop: Fujitsu Celcius H780
* Operating System: Windows 10 Pro x64
* Software: Python 3.10, 3.11 (virtual env - workspace), 3.12 (Anaconda)
###
* Raspberry Pi 4B (2 GB RAM)
* Operating System: Raspbian GNU/Linux 11 (bullseye)
* Distribution: raspberrypi 6.1.21-v8+
* OS type: 64-bit
* Software: Python 3.9.2

See **_pip_freeze.txt_** (from virtual env) for more details if interested.

Certain refactoring of the code (gestures_recognition.py) was done by me.

## Failed attempts to run Gesture Recognition with Mediapipe only on Raspberry Pi 4
This project aimed to run gesture recognition using MediaPipe directly on Raspberry Pi 4. Initially, in the original course, MediaPipe was running on laptop with Windows 10, and the LED control was managed by Arduino, connected via a USB cable to the laptop.

**Installation Attempts**

I've tried to install and run MediaPipe on my Raspberry Pi 4, but despite successful installations using commands like _**pip install mediapipe**_ or _**pip install mediapipe-rpi4**_, it did not work in the end.

**Issues with aarch64**

I found out that MediaPipe would not work on the aarch64 architecture. To resolve this, I tried to write 32-bit Rasp OS on 2 new SD cards with the following images written using Rasp Pi Imager and balenaEtcher:

2024-10-22-raspios-bullseye-armhf-full.img.xz

2024-03-12-raspios-bookworm-armhf-full.img.xz

However, upon checking, the system always detected aarch64 instead of armhf.

**Virtual Environment and Docker container Attempts**

I also tried running MediaPipe in a virtual environment, in Docker container, and a virtual environment inside Docker container. Unfortunately, after spending 2 days on unsuccessful attempts, it still did not work.

**Final Solution**

Finally, I managed to run the MediaPipe project on my laptop with Windows 10, but now the connection was established using SSH commands to control the LEDs connected to the GPIO pins of my Raspberry Pi 4.

