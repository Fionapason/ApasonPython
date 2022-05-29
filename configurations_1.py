"""
This file is used to configure the sensors and control instruments on the FIRST arduino (ID = 1)

Each sensor/instrument belongs to a type (i.e. "pressure", "pump", "pcv") and contains a for that type unique ID,
which will be used to easily find the corresponding sensor between the arduino class and the update list/command center class.
The ID must be UNIQUE across all configuration files.

Also given is which the arduino ID of the corresponding sensor, a name, and the bool "in_use",
which represent whether the sensor/instrument is plugged into the arduino

Various other sensor/instrument-type dependent parameters are given

The comment next to each sensor/instrument object is the equivalent arduino output
"""


sensor_configurations_1 = {

    "pressure": [  {"id": 0, "arduino_id": 1,
                    "name": "GEMS", "unit": "bar", "in_use": True,
                    "max_pressure": 5.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A0

                   {"id": 1, "arduino_id": 1,
                    "name": "UF Feed Pressure", "unit": "bar", "in_use": True,
                    "max_pressure": 6.0, "critical_pressure": 3.0, "warning_pressure": 2.5}, #A1

                  {"id": 2, "arduino_id": 1,
                   "name": "UF Retentate Pressure", "unit": "bar","in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 3.0, "warning_pressure": 2.5}, #A2

                  {"id": 3, "arduino_id": 1,
                   "name": "UF Permeate Pressure", "unit": "bar",  "in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A3

                  {"id": 4, "arduino_id": 1,
                   "name": "idle", "unit": "bar",  "in_use": False,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7} #A4

                   ],

    "massflow": [{"id": 0, "arduino_id": 1,
                   "name": "UF Backwash Flow", "unit": "l/min", "in_use": True, #A5
                   "max_flow": 10.0}, # TODO IS THIS CORRECT??

                  {"id": 1, "arduino_id": 1,
                   "name": "UF Permeate Flow", "unit": "l/min", "in_use": True, #A6
                   "max_flow": 5.0}

                  ],

    "conductivity": [ {"id": 0, "arduino_id": 1,
                       "name": "ED Feed Cond", "unit": "mS/cm", "in_use": False, #A9
                       "max_Cond": 50.0, "min_Cond": 0.1},

                      {"id": 1, "arduino_id": 1,
                       "name": "ED Diluate Cond", "unit": "mS/cm", "in_use": False, #A10
                       "max_Cond": 50.0, "min_Cond": 0.1},

                      {"id": 2, "arduino_id": 1,
                       "name": "ED Concentrate Cond", "unit": "mS/cm", "in_use": False, #A11
                       "max_Cond": 50.0, "min_Cond": 0.1}

                      ],

    "level": [ {"id": 0, "arduino_id": 1,
                "name": "Feed Tank High", "in_use": True}, #D22
               {"id": 1, "arduino_id": 1,
                "name": "Feed Tank Middle", "in_use": True}, #D23
               {"id": 2, "arduino_id": 1,
                "name": "Feed Tank Low", "in_use": True}, #D24
               {"id": 3, "arduino_id": 1,
                "name": "UF Tank High", "in_use": True}, #D25
               {"id": 4, "arduino_id": 1,
                "name": "UF Tank Middle", "in_use": True}, #D26
               {"id": 5, "arduino_id": 1,
                "name": "Purge Tank Middle", "in_use": True}, #D27
               {"id": 6, "arduino_id": 1,
                "name": "Purge Tank High", "in_use": True}, #D28
               {"id": 7, "arduino_id": 1,
                "name": "idle", "in_use": False}, #D29
               {"id": 8, "arduino_id": 1,
                "name": "idle", "in_use": False}, #D30
               {"id": 9, "arduino_id": 1,
                "name": "idle", "in_use": False}, #D31
               {"id": 10, "arduino_id": 1,
                "name": "idle", "in_use": False}, #D32
               {"id": 11, "arduino_id": 1,
                "name": "idle", "in_use": False}, #D33
               {"id": 12, "arduino_id": 1,
                "name": "idle", "in_use": False}, #D34
               {"id": 13, "arduino_id": 1,
                "name": "idle", "in_use": False}, #D35
               {"id": 14, "arduino_id": 1,
                "name": "idle", "in_use": False}  #D36
              ]
}

control_instrument_configurations_1 = {

    "cv3": [ {"id": 0, "arduino_id": 1,
              "name": "UF Switch", "in_use": True, #D38
             "start_state": "LOW"}, # or "HIGH"
            ],

    "ocv_normally_closed": [{"id": 0, "arduino_id": 1,
                          "name": "UF Backwash Valve", "in_use": True, #D44
                          "start_state": "LOW"} # 'LOW' == open, 'HIGH' == closed

                         ],

    "ocv_normally_open": [{"id": 0, "arduino_id": 1,
                            "name": "UF Feed Valve", "in_use": True, #D45
                            "start_state": "LOW"}  # 'HIGH' == open, 'LOW' == closed
                           ],

    #PUMP AND PCV SHARE THEIR IDS BECAUSE OF THE DAC

    "pump": [ {"id": 0,  "DAC_output": 'A',"arduino_id": 1,
               "name": "UF Backwash Pump", "unit": "RPM", "in_use": True,  #ON/OFF, DAC A
               "max_RPM": 9000.0, "starting_RPM": 0.0},

              {"id": 1, "DAC_output": 'B', "arduino_id": 1,
               "name": "UF Feed Pump", "unit": "RPM", "in_use": True,  #ON/OFF, DAC B
               "max_RPM": 9000.0, "starting_RPM": 0.0}

            ]

}

if __name__ == '__main__':

    for sensor in sensor_configurations_1["pressure"]:
        print(sensor["name"])
