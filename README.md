# FabGL

>[!WARNING]
>### This specific branch contains a patched version of the FabGL library specifically for use with nTerm2-S/SporosTerm. These patches are not contained in the library that you download via Library >Manager of the Arduino environment. ###

>[!IMPORTANT]
>### Find the original information about the FabGL library here: https://github.com/fdivitto/FabGL ###

>[!WARNING]
>The latest version of the Espressif ESP32 library that FabGL runs on is *2.0.17* (or even earlier). Unfortunately, the latest versions of Espressif leave too little memory free for applications, and a project the size of FabGL can no longer function as intended.

### How to use this library for SporosTerm ([http://github](https://github.com/RetepV/SporosTerm)) ###

1. Make sure to be on the latest Arduino development environment.
2. Follow the instructions at https://github.com/espressif/arduino-esp32 to install the ESP32 board support.
3. After having installed the ESP32 board support, you will have to open the Arduino Boards Manager and find the entry 'esp32 by Espressif Systems'. Here, you will have to switch your installed version (probably 3.3.2 or later) to version 2.0.17. It is absolutely necessary to downgrade to 2.0.17, in order to compile the FabGL library.
4. Download the patched FabGL library's source code from here: https://github.com/RetepV/FabGL/tree/FabGL-nTerm2-S. Doublecheck if you have the FabGL-nTerm2-S branch selected. Download the source code as a .zip file, it will probably be named FabGL-FabGL-nTerm2-S.zip.
5. Download the SporosTerm source code and then open SporosTerm.ino in the Arduino development environment.
6. In the Arduino development environment, go to Sketch->Include Library->Add .ZIP Library. Select the FabGL-FabGL-nTerm2-S.zip file, wait until Arduino finishes processing and tells that the library was installed successfully.

In order to build SporosTerm, you will also need to include the OneWire library.

7. In the Arduino development environment, now go to Sketch->Include Library->Manage Libraries and filter on onewire. Install the 'Onewire' library version 2.3.8 (by Jim Studt, Tom Pollard, Robin James and Paul Stoffregen.

Now you can open the SporosTerm .ino, connect the nTerm2-S board to USB, choose 'ESP32 Dev Module' and the correct serial port (e.g. in my case /dev/cu.usbserial-DN01JQWK), choose a Partition Scheme that has a larger-than 1.5MB partition for the app (e.g. 'NO OTA (2MB APP/2MB SPIFFS)'), upload speed can be 921600 but depends on the quality of your cable, and now you should be able to compile and upload the sketch.

>[!NOTE]
>The app is about 1.32MB in size. The default Partition Scheme only allocates 1.2MB for the app, so the app won't fit. Therefore, in Tools->Partition Scheme you will need to choose a partition scheme with at least 1.5MB for the app. The exact scheme is up to you and your ESP32 type, but it needs storage for the app and some extra storage for the settings, which can be either SPIFFS (recommended) or FATFS. If your ESP32 has 4MB (which is quite usual), you can choose NO OTA (2MB APP/2MB SPIFFS). I personally use ESP32-WROOM-32E MGN16 modules with 16MB flash, but also choose the NO OTA (2MB APP/2MB SPIFFS) scheme for release. For development use, I use 16M Flash (3M APP/9.9M FATFS).

