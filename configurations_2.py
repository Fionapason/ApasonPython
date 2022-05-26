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
                    "name": "theoretical gems", "unit": "bar", "in_use": True,
                    "max_pressure": 5.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A0

                  {"id": 6, "arduino_id": 2,
                    "name": "Diluate In Pressure", "unit": "bar", "in_use": True,
                    "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A1

                  {"id": 7, "arduino_id": 2,
                   "name": "Concentrate In Pressure", "unit": "bar","in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A2

                  {"id": 8, "arduino_id": 2,
                   "name": "Rinse Pressure", "unit": "bar",  "in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A3

                  {"id": 9, "arduino_id": 2,
                   "name": "idle", "unit": "bar",  "in_use": False,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7} #A4

                   ],

    "massflow": [ {"id": 2, "arduino_id": 2,
                   "name": "Concentrate Flow", "unit": "l/min", "in_use": True, #A5
                   "max_flow": 5.0},

                  {"id": 3, "arduino_id": 2,
                   "name": "ED Diluate Flow", "unit": "l/min", "in_use": True, #A6
                   "max_flow": 5.0},

                  {"id": 4, "arduino_id": 2,
                   "name": "ED Rinse Flow", "unit": "l/min", "in_use": True, #A7
                   "max_flow": 5.0},

                  {"id": 5, "arduino_id": 2,
                   "name": "Posttreatment Flow", "unit": "l/min", "in_use": True  , #A8
                   "max_flow": 5.0}
                  ],

    "conductivity": [ {"id": 4, "arduino_id": 2,
                       "name": "ED Diluate Out Cond", "unit": "mS/cm", "in_use": True, #A9
                       "max_Cond": 10.0, "min_Cond": 0.2},

                      {"id": 5, "arduino_id": 2,
                       "name": "ED Concentrate Cond", "unit": "mS/cm", "in_use": True, #A10
                       "max_Cond": 60.0, "min_Cond": 50.0},

                      {"id": 3, "arduino_id": 2,
                       "name": "ED Diluate In Cond", "unit": "mS/cm", "in_use": True, #A11
                       "max_Cond": 12, "min_Cond": 1},


                      ],


    "level": [ {"id": 15, "arduino_id": 2,
                "name": "ED-Split Tank High", "in_use": True}, #D22
               {"id": 16, "arduino_id": 2,
                "name": "ED-Split Tank Low", "in_use": True}, #D23
               {"id": 17, "arduino_id": 2,
                "name": "ED-Split Tank Middle", "in_use": True}, #D24
               {"id": 18, "arduino_id": 2,
                "name": "ED-Con Tank Middle", "in_use": True}, #D25
               {"id": 19, "arduino_id": 2,
                "name": "NO", "in_use": True}, #D26
               {"id": 20, "arduino_id": 2,
                "name": "ED-Rinse Tank", "in_use": True}, #D27
               {"id": 21, "arduino_id": 2,
                "name": "UF Tank Low", "in_use": True}, #D28
               {"id": 22, "arduino_id": 2,
                "name": "idle", "in_use": False}, #D29
               {"id": 23, "arduino_id": 2,
                "name": "idle", "in_use": False}, #D30
               {"id": 24, "arduino_id": 2,
                "name": "idle", "in_use": False}, #D31
               {"id": 25, "arduino_id": 2,
                "name": "idle", "in_use": False}, #D32
               {"id": 26, "arduino_id": 2,
                "name": "idle", "in_use": False}, #D33
               {"id": 27, "arduino_id": 2,
                "name": "idle", "in_use": False}, #D34
               {"id": 28, "arduino_id": 2,
                "name": "idle", "in_use": False}, #D35
               {"id": 29, "arduino_id": 2,
                "name": "idle", "in_use": False}  #D36
              ]
}

control_instrument_configurations_2 = {

    "cv3": [ {"id": 6, "arduino_id": 2,
              "name": "ED Pre-Diluate", "in_use": True, #D38
             "start_state": "LOW"}, # or "RIGHT"

             {"id": 7, "arduino_id": 2,
              "name": "ED Pre-Concentrate", "in_use": True, #D39
             "start_state": "LOW"},

             {"id": 8, "arduino_id": 2,
              "name": "ED Post-Diluate", "in_use": True, #D40
              "start_state": "LOW"},

             {"id": 9, "arduino_id": 2,
              "name": "ED Post-Concentrate", "in_use": True, #D41
              "start_state": "LOW"},

             {"id": 10, "arduino_id": 2,
              "name": "ED Second-Pre-Diluate", "in_use": True, #D42
              "start_state": "LOW"},

             {"id": 11, "arduino_id": 2,
              "name": "idle", "in_use": False, #D43
              "start_state": "LOW"},
            ],

    "ocv_normally_closed": [{"id": 3, "arduino_id": 2,
                          "name": "ED Dilute Concentrate", "in_use": True, #D44
                          "start_state": "LOW"},  # 'LOW' == open, 'HIGH' == closed

                         ],

    "ocv_normally_open": [{"id": 0, "arduino_id": 2,
                            "name": "UF OCV", "in_use": False, #D45
                            "start_state": "LOW"}  # 'HIGH' == open, 'LOW' == closed
                           ],


    "pump": [ {"id": 2,  "DAC_output": 'A', "arduino_id": 2,
               "name": "Posttreatment Pump", "unit": "RPM", "in_use": True,  #D48 ON/OFF, DAC A
               "max_RPM": 9000.0, "starting_RPM": 0.0},

              {"id": 3, "DAC_output": 'B', "arduino_id": 2,
               "name": "Rinse Pump", "unit": "RPM", "in_use": True,  #D49 ON/OFF, DAC B
               "max_RPM": 9000.0, "starting_RPM": 0.0},

              {"id": 4, "DAC_output": 'C', "arduino_id": 2,
               "name": "Concentrate Pump", "unit": "RPM", "in_use": True,  #D49 ON/OFF, DAC C
               "max_RPM": 9000.0, "starting_RPM": 0.0},

              {"id": 5, "DAC_output": 'D', "arduino_id": 2,
               "name": "Diluate Pump", "unit": "RPM", "in_use": True,  #D49 ON/OFF, DAC B
               "max_RPM": 9000.0, "starting_RPM": 0.0}
            ],


    "polarity": [ {"id": 0, "arduino_id": 2,
                   "name": "ED Polarity", "in_use": True, #D50
                   "start_state": "OFF"} # 'LOW' == positive, 'HIGH' == negative, "OFF" == no voltage
                  ]
}

if __name__ == '__main__':
    pass

