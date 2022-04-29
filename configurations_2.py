"""
This file is used to configure the sensors and control instruments on the FIRST arduino (ID = 2)

Each sensor/instrument belongs to a type (i.e. "pressure", "pump", "pcv") and contains a for that type unique ID,
which will be used to easily find the corresponding sensor between the arduino class and the update list/command center class.
The ID must be UNIQUE across all configuration files.

Also given is which the arduino ID of the corresponding sensor, a name, and the bool "in_use",
which represent whether the sensor/instrument is plugged into the arduino

Various other sensor/instrument-type dependent parameters are given

The comment next to each sensor/instrument object is the equivalent arduino output
"""

sensor_configurations_2 = {

    "pressure": [  {"id": 5, "arduino_id": 2,
                    "name": "GEMS", "unit": "bar", "in_use": True,
                    "max_pressure": 5.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A0

                   {"id": 6, "arduino_id": 2,
                    "name": "UF Feed Pressure", "unit": "bar", "in_use": True,
                    "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A1

                  {"id": 7, "arduino_id": 2,
                   "name": "UF Retentate Pressure", "unit": "bar","in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A2

                  {"id": 8, "arduino_id": 2,
                   "name": "UF Permeate Pressure", "unit": "bar",  "in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A3

                  {"id": 9, "arduino_id": 2,
                   "name": "idle", "unit": "bar",  "in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7} #A4

                   ],

    "massflow": [ {"id": 4, "arduino_id": 2,
                   "name": "UF Feed Flow", "unit": "l/min", "in_use": True, #A5
                   "max_flow": 20.0},

                  {"id": 5, "arduino_id": 2,
                   "name": "UF Retentate Flow", "unit": "l/min", "in_use": True, #A6
                   "max_flow": 10.0},

                  {"id": 6, "arduino_id": 2,
                   "name": "UF Permeate Flow", "unit": "l/min", "in_use": True, #A7
                   "max_flow": 5.0},

                  {"id": 7, "arduino_id": 2,
                   "name": "idle", "unit": "l/min", "in_use": True, #A8
                   "max_flow": 0}
                  ],

    "conductivity": [ {"id": 3, "arduino_id": 2,
                       "name": "ED Feed Cond", "unit": "mS/cm", "in_use": True, #A9
                       "max_Cond": 50.0, "min_Cond": 0.1},

                      {"id": 4, "arduino_id": 2,
                       "name": "ED Diluate Cond", "unit": "mS/cm", "in_use": True, #A10
                       "max_Cond": 50.0, "min_Cond": 0.1},

                      {"id": 5, "arduino_id": 2,
                       "name": "ED Concentrate Cond", "unit": "mS/cm", "in_use": True, #A11
                       "max_Cond": 50.0, "min_Cond": 0.1}

                      ],

    "temperature": [ {"id": 3, "arduino_id": 2,
                      "name": "ED Feed Temp", "unit": "ºC",  "in_use": True,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}, #A12

                     {"id": 4, "arduino_id": 2,
                      "name": "ED Diluate Temp", "unit": "ºC", "in_use": True,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}, #A13

                     {"id": 5, "arduino_id": 2,
                      "name": "ED Concentrate Temp", "unit": "ºC", "in_use": True,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0} #A14

                    # ,
                    #  {"id": 6, "arduino_id": 2,
                    #   "name": "AC Tank Temp", "unit": "ºC", "in_use": True,
                    #   "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}  #A15
                     ],


    "level": [ {"id": 15, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D22
               {"id": 16, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D23
               {"id": 17, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D24
               {"id": 18, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D25
               {"id": 19, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D26
               {"id": 20, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D27
               {"id": 21, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D28
               {"id": 22, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D29
               {"id": 23, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D30
               {"id": 24, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D31
               {"id": 25, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D32
               {"id": 26, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D33
               {"id": 27, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D34
               {"id": 28, "arduino_id": 2,
                "name": "idle", "in_use": True}, #D35
               {"id": 29, "arduino_id": 2,
                "name": "idle", "in_use": True}  #D36
              ]
}

control_instrument_configurations_2 = {

    "cv3": [ {"id": 6, "arduino_id": 2,
              "name": "idle", "in_use": False, #D38
             "start_state": "LEFT"}, # or "RIGHT"

             {"id": 7, "arduino_id": 2,
              "name": "idle", "in_use": False, #D39
             "start_state": "LEFT"},

             {"id": 8, "arduino_id": 2,
              "name": "idle", "in_use": False, #D40
              "start_state": "LEFT"},

             {"id": 9, "arduino_id": 2,
              "name": "idle", "in_use": False, #D41
              "start_state": "LEFT"},

             {"id": 10, "arduino_id": 2,
              "name": "idle", "in_use": False, #D42
              "start_state": "LEFT"},

             {"id": 11, "arduino_id": 2,
              "name": "idle", "in_use": False, #D43
              "start_state": "LEFT"},
            ],

    "ocv_normally_open": [{"id": 3, "arduino_id": 2,
                          "name": "UF OCV", "in_use": True, #D44
                          "start_state": "OPEN"},  # or "CLOSED"

                         {"id": 4, "arduino_id": 2,
                          "name": "UF OCV", "in_use": True, #D45
                          "start_state": "OPEN"},

                         {"id": 5, "arduino_id": 2,
                          "name": "UF OCV", "in_use": False, #D46
                          "start_state": "OPEN"},

                         ],

    "ocv_normally_closed": [{"id": 1, "arduino_id": 2,
                            "name": "UF OCV", "in_use": True, #D47
                            "start_state": "OPEN"}  # or "CLOSED"
                           ],

    #PUMP AND PCV SHARE THEIR IDS BECAUSE OF THE DAC

    "pump": [ {"id": 2,  "DAC_output": 'A',"arduino_id": 2,
               "name": "UF Feed Pump", "unit": "RPM", "in_use": True,  #D48 ON/OFF, DAC A
               "max_RPM": 9000.0, "starting_RPM": 0.0},

              {"id": 3, "DAC_output": 'B', "arduino_id": 2,
               "name": "UF Backwash Pump", "unit": "RPM", "in_use": True,  #D49 ON/OFF, DAC B
               "max_RPM": 9000.0, "starting_RPM": 0.0}
            ],

    "pcv": [ {"id": 2, "DAC_output": 'C', "arduino_id": 2,
              "name": "UF PCV", "unit": "%", "in_use": True, #DAC C
              "start_opening": 100.0},

             {"id": 3, "DAC_output": 'D', "arduino_id": 2,
              "name": "ED PCV", "unit": "%", "in_use": True, #DAC D
              "start_opening": 40.0}
             ],

    "polarity": [ {"id": 0, "arduino_id": 2,
                   "name": "ED Polarity", "in_use": False, #D50
                   "start_state": "POSITIVE"} #or "NEGATIVE"
                  ]
}

if __name__ == '__main__':

    for sensor in sensor_configurations["pressure"]:
        print(sensor["name"])
