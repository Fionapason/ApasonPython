# Apasōn – A Solar-Powered Water Purification System

## Introduction
***

Apasōn is a water purification device, developed by 8 engineering Bachelor's students at the [Swiss Federal Institute of Technology in Zürich (ETH)][ethz_link]
between September 2021 and June 2022, in the context of the focus project [SOWA][sowa_link] (meaning **So**lar **Wa**ter).


It is built to take contaminated well water and remove micro-particles and bacteria, using an [ultrafiltration membrane][uf_link]; ions, using an [electro-dialysis][ed_link] module; volatile organic compounds, using an [activated carbon filter][ac_link]; as well as neutralize viruses, using a [UV-lamp][uv_link].


Apasōn does this using various tanks to store water in between purification steps and runs entirely on solar power.

This [GIT][git] contains the Python and Arduino Code, on which Apasōn runs.

[sowa_link]: https://sowa.ethz.ch/
[ethz_link]: https://ethz.ch/de.html
[ed_link]: https://en.wikipedia.org/wiki/Electrodialysis
[uf_link]: https://en.wikipedia.org/wiki/Ultrafiltration
[ac_link]: https://en.wikipedia.org/wiki/Carbon_filtering
[uv_link]: https://en.wikipedia.org/wiki/Ultraviolet_germicidal_irradiation
[git]: https://github.com/Fionapason/ApasonPython

## Running Apasōn
***
### Configuring

In order for Apasōn to run correctly, **it is pertinent that the code is configured congruently with the way the hardware is set up**.
As all instruments are connected to Arduinos, and not directly to the Raspberry Pi, on which the Python code runs,
every sensor or instrument is called up via a **unique character command**. (Unique _to the Arduino_; both Arduinos are in fact running on the same code. The Excel table `Apason_Python_Arduino_Sensor_Command_Overview.xlsx` provides an overview of the commands.)
For this reason, sensors and instruments **need** to be plugged into the corresponding Arduino pin, or **both the Python and the Arduino Code** will need to be adapted significantly.

Using **names** for the sensors, and in general making changes **within the configuration file only**, allows for an easy adaptation of the control system, without changing the more primitive serial communication between RPi and Arduino.

### Starting Up The System

In order to start up Apasōn (assuming this repository has been copied onto the [Raspberry Pi Model 4][rpi_link] that the system runs on), all library and package requirements
found in the `requirements.txt` file need to be installed.
Additionally, the Arduino Code needs to be loaded onto the two [Arduino Mega 2560 Rev3 models][arduino_link]. It is identical for both of them. Both Arduinos must be plugged in.

**THE UF ARDUINO _MUST_ BE PLUGGED IN _BEFORE_ THE ED ARDUINO** _because RPis dynamically assign serial portnames._
Additionally, the monitor will not turn on, if the Arduinos are plugged in when the system starts up, because they will be "stealing" the power from the monitor.
Therefore, plug the monitor in, before powering on the RPi and only plug in the Arduinos (UF then ED, as mentioned) once the RPi is running.

Lastly, before running the system, the **Kivy virtual environment needs to be activated.**
For this, one must change into the `kivy_venv` directory and, from the terminal, carry out the command:
`source /bin/activate`.

[rpi_link]: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
[arduino_link]: https://store.arduino.cc/products/arduino-mega-2560-rev3

Then change directory to `apason_python/Python_Code` and run: `python3 Apason_Mission_Control.py` in your terminal.

### Shutting Down The System

The safest way to shut down Apasōn, is to first turn the system off using the 'SYSTEM' switch on the GUI and then to close the application window. Closing the application on its own however, will also shut the entire system off.

Should the RPi be none-responsive, forcing you to quit the programme using `Ctrl+C` **please remember to switch off the electricity for the load** (green button above the monitor, labelled 'LOAD') because this will turn off the 24 Volts provided to all control instruments immediately.

**If you quit the programme improperly but leave the power on, the control instruments will remain in whatever state they were in upon quitting, as they are *set from the Arduinos* and *not* from the RPi directly**

### User Experience

The GUI (**G**raphical **U**ser **I**nterface) is very simple, showing only three measurements: the current output flow rate, so the user may know how much clean water they are currently getting,
and the conductivities at the inlet and outlet of the electro-dialysis module, as these may be of interest.
To turn the system on, the user flicks the 'SYSTEM' switch from 'OFF' to 'ON'.

Once the system is running, the user also has the option to stop the output pump, so that they may switch out their output tank,
while letting the purification process continue. This switch is locked to the user, while the system is shut down.

When tanks approach a critical level, the app will let popup windows appear as a warning to the user. Additionally, if the system is being shut down in an emergency,
there will also be a popup window explaining why this happened.

Moreover, a log of some activities of the programme will be printed in the terminal, so that the user may track what happened just before a system shutdown and better assess the issue.

## Working Principle
***

The code differentiates generally between **sensors** and **control instruments**.
The former consists of all parts of the system, which can be **read**, that is to say pressure sensors, massflow sensors, level-switches, and conductivity sensors.
The latter consists of all parts of the system, which can be **set** electronically, that is to say pumps, electrically controlled valves, and the polarity of the electro-dialysis unit.

The tasks of the code are subdivided into **four concurrently running threads:**
* the Update List, which periodically checks all sensor values, using the commands saved in `Arduino_Sensors` to extract the sensor readings via the `Arduino_Utilities` function `retrieve_measurment()`, or `read_digital()` in the case of the level switches. The measurement is then saved in the `current_value` property of
the sensor in the `Sensor_Update_List` class. If one of the values corresponds to one of the three values that are to be shown in the GUI, this thread manages converting the measurements into legible strings and forwards the string to the GUI thread, so they may be displayed.


* the Command Center, which periodically checks all the instruments in `Apason_System_Instruments`for a change in state and, if there is one, sends the corresponding command from `Arduino_Control_Instruments` using `set_analog()` or `set_digital()` from `Arduino_Utilities`.
This thread also starts the Control System, and is the "first port of call", if the Control System has detected a problem, so that all instruments can be immediately shut off if necessary.
Should a problem in the system arise, the Command Center also informs the GUI Thread, so it may be displayed to the User. It is via the Command Center that the system itself is effectively turned on.


* the Control System Thread, which periodically checks the measured values via the from the Update List and, based on these, decides what new state the different control instruments should adopt. It then sets these in `Apason_System_Instruments`, so that the Command Center can take on these changes and send the commands on.


* the GUI, which runs as an application in a separate window. It is periodically updating its displayed sensor values, according to the set values provided by the Update List, and checking if any problems, which require a popup window, have arisen – the Command Center would have informed the GUI thread about such problems. Additionally it is keeping track of the two switches ('SYSTEM' and 'OUTPUT PUMP') and can communicate to the Control Thread, via the Command Center, that the system/output pump must be turned on/off.
Closing the GUI app is what ends the entire programme. 


## Used Libraries
***

To establish the serial connection with the two Arduinos, the library pyserial is used, [which can be downloaded here.][pyserial_link]


The utilities from the pyserial library were elaborated on in the file `Serial_Utilities`, to facilitate the RPi-Arduino communication.

The GUI application runs using a Kivy framework, which needs to be installed correctly, including the **Kivy Virtual Environment**,
in order for the app to run. [Kivy can be installed here][kivy].


Additionally, in order to make the Digital-Analog-Converters (model: [Adafruit MCP4728][mcp_link]), which are attached to the Arduinos via I2C communication, work, the following libraries need to be included:
* [Adafruit_MCP4728][dac_lib]
* [Adafruit_BusIO][bus_lib]


[pyserial_link]: https://pyserial.readthedocs.io/en/latest/pyserial.html
[kivy]: https://kivy.org/doc/stable/gettingstarted/installation.html
[mcp_link]: https://www.adafruit.com/product/4470
[dac_lib]: https://github.com/adafruit/Adafruit_MCP4728
[bus_lib]: https://github.com/adafruit/Adafruit_BusIO

These libraries can be included **within** the Arduino IDE, which also compiles and uploads the codes onto the Arduinos.
[The IDE is open source and can be downloaded here.][ide]

[ide]: https://www.arduino.cc/en/software

Further libraries necessary for the running of the code can be seen in the `Requirements.txt` file.

## Files and Directories

***

`Apason_Python_Arduino_Sensor_Command_Overview.xlsx` : An Excel table used to keep an overview of the single character commands and corresponding sensors and Arduino pins within the System. 

`Requirements.txt` : A file containing all required libraries and versions. Use the command `pip install -r Requirements.txt` to install all.

`.gitignore` : Specifies intentionally untracked files, mainly the virtual environment.

`readme.md` : The very file you are reading! :-) Meant to provide a basic introduction to this code.

## `Apason_Arduino_Code`:
* `Apason_Arduino_Code.ino`: In order to open the code within the Arduino IDE, it must have the file signature `.ino` and be located in a folder with the same name.
* `Apason_Arduino_Code.c`: For legibility within other IDEs, the Arduino code is included in C as well. The Arduino language is basically C, so it might be easier to look at the code in this file.

## `Python_Code`:

* `Apason_Mission_Control.py`: This file contains the `main` of the entire code. First the serial connection with the Arduinos is established.
Then the Arduino sensor and control instrument lists are initialized, using the configuration files. After this, the Update List thread as well as the Command Center thread are started and then lastly the GUI is set to run.



* `Arduino_Communication`: A directory for all parts of the code, which are directly linked to the Arduino.
  * `Arduino_Control_Instruments.py` : A class that keeps track of all control instruments in the system in relationship to the Arduino. Every control
     instrument instance has an Arduino ID (1 for the UF Arduino, 2 for the ED Arduino) as a member.
    Additionally, it can, if needed, calculate the necessary `int` between 0 and 4095 required to set a specific analog voltage.
  * `Arduino_Sensors.py` : A class that keeps track of all the sensors in the system in relationship to the Arduino. Every sensor instance contains an Arduino ID (1 for the UF Arduino, 2 for the ED Arduino), a specific serial command, and a function that can calculate the true measurement based on the byte value sent from the Arduino and the sensor parameters.
  * `Arduino_Utilities.py` : Contains the handshake function and the function, which initializes all Arduinos,
    as well as the four basic functions for setting digital/analog and reading digital/analog pins.
    Locks() are used to ensure the Command Center thread and the Update List thread don't interrupt the dialogue between the RPi and the Arduino.
  * `Serial_Utilities.py` : Contains functions that facilitate serial-communication with the Arduino.



* `Configurations`: A directory for configuration files, which allow for small changes in the sensor setup, without having to make invasive changes to the code.
  * `Configurations_Arduino_ED.py` : This file is where the Arduino-Pin positioning of the various sensors and control instruments in the ED part of the Apasōn setup are configured, as well as various parameters like unit, minimum and maximum measurements, critical values that demand a system shut-off, etc.
  The file uses the dict() native-Python type, to organize the general types of instruments/sensor (eg. "pressure", "pump", "levelswitch", "polarity"). Each type is then a list, containing every instrument/sensor in dict() form. It is crucial that the instruments are ordered **in the order they are placed on the Arduino.** The corresponding pins are visible in the comments next to each instrument/sensor instance.
  Additionally, the port name of the corresponding Arduino is defined here.
  * `Configurations_Arduino_UF.py` : This file is essentially identical to `Configurations_Arduino_ED.py`, but here the configurations are for the sensors/instruments on the other Arduino.
  * `Configurations_Control_Systems.py` : This file is where the control systems are configured. For PI-controllers, `K_p` and `K_i` values can be set here, as well as things like the amount of time that should pass between or during certain processes within the system.
  Additionally, the names of the relevant sensors/instruments, **which must be identical to those used in the other configurations files**, are recorded here,
  so that the control system can easily find the control instrument/sensor in `Sensor_Instrument_Tracking` .


* `Control_Systems`: A directory containing classes, which implement the specific control systems for our two subsystems.
  * `ED_Control.py` : Contains classes, which track the control of the entire ED system using the `Configurations_Control_Systems.py`file.
                      Control includes monitoring the concentrate tank, ensuring the proper valve configuraton based on whether we are currently running the ED in normal or reversal operation, checking crucial pressure differences,
  and implementing a PI control for the conductivity concentration as well as the flow rate.
  * `UF_Control.py` : Contains classes, which track the control of the entire UF system using the `Configurations_Control_Systems.py`file.
                      Control includes monitoring whether a backwashing cycle is needed, checking crucial pressure differences, and implementing a PI control for the flow rate through the UF.



* `Main_Threads` : A directory containing the four concurrently running threads
  * `GUI`: A directory containing the files related to the **Graphical User Interface** of Apasōn, using the Kivy library. The GUI app itself runs as a thread.
    * `gui.py` : This python file handles the logic of the GUI. It regularly updates its sensor readings and checks if it needs to display a warning or problem message.
    It also handles what happens, when one of the switches of the GUI has been engaged.
    * `apason_gui.kv` : This .kv file handles the visuals of the GUI.
  * `Command_Center_Thread.py` : A file containing the command sending thread, which communicates with the Arduino,
  in case any of the control instruments need to be set differently.
  * `Control_System_Thread.py` : A file containing the overall control system thread,
  which initializes instances of the ED and UF control classes found in the `Control_Systems` directory,
  as well as its own control systems. It continuously runs the control, making adjustments and checking for major problems that would require a system shut down.
  * `Update_List_Thread.py` : A file containing an instance of a `Sensor_Update_List` (see `Sensor_Instrument_Tracking/Sensor_Update_List.py`),
  where all sensor readings are routinely updated via communication with the Arduino.
  

* `Sensor_Instrument_Tracking` : A directory containing classes, which keep track of all sensors and control instruments,
handling their current state and other key attributes, which are not related to the direct Arduino communication.
  * `Apason_System_Instruments.py` : A file where all control instruments are stored as instances of instrument-specific classes
  within an instrument-specific list, where each list is a member of the `Apason_System` class. Each system instrument class contains at least a `set_new_state`function,
  that allows to change the state of the specific instrument. **Setting a new state does not in of itself change the real-life state of the control instrument**.
  Instead, it is the Command Center thread that takes care of sending the command to the Arduino.
  * `Sensor_Update_List.py` : A file where all sensors are stored as instances of sensor-specific classes within an instrument-specific list,
  where each list is a member of the `Sensor_Update_List` class. Each sensor class contains at least an `update_value` function,
  which allows you to change the currently saved value in the Update List.
