#TODO also clarify which arduino it's on

sensor_configurations = {

    "pressure_gems": [{"name": "ED Feed", "unit": "bar", "in_use": False,
                       "max_pressure": 5.0, "critical_pressure": 5.0, "warning_pressure": 4.7}  # A0
                      ],

    "pressure": [  {"name": "UF Feed Pressure", "unit": "bar", "in_use": True,
                    "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A1

                  {"name": "UF Retentate Pressure", "unit": "bar","in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A2

                  {"name": "UF Permeate Pressure", "unit": "bar",  "in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A3

                  {"name": "idle", "unit": "bar",  "in_use": False,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7} #A4

                   ],

    "massflow": [ {"name": "UF Feed Flow", "unit": "l/min", "in_use": True, #A5
                   "max_flow": 20.0},

                  {"name": "UF Retentate Flow", "unit": "l/min", "in_use": True, #A6
                   "max_flow": 10.0},

                  {"name": "UF Permeate Flow", "unit": "l/min", "in_use": True, #A7
                   "max_flow": 5.0},

                  {"name": "idle", "unit": "l/min", "in_use": False, #A8
                   "max_flow": 0}
                  ],

    "conductivity": [ {"name": "ED Feed Cond", "unit": "mS/cm", "in_use": False, #A9
                       "max_Cond": 50.0},

                      {"name": "ED Diluate Cond", "unit": "mS/cm", "in_use": False, #A10
                       "max_Cond": 50.0},

                      {"name": "ED Concentrate Cond", "unit": "mS/cm", "in_use": False, #A11
                       "max_Cond": 50.0}

                      ],

    "temperature": [ {"name": "ED Feed Temp", "unit": "ºC",  "in_use": False,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}, #A12

                     {"name": "ED Diluate Temp", "unit": "ºC", "in_use": False,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}, #A13

                     {"name": "ED Concentrate Temp", "unit": "ºC", "in_use": False,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}, #A14

                     {"name": "AC Tank Temp", "unit": "ºC", "in_use": False,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0} ], #A15

    "level": [ {"name": "idle", "in_use":False}, #D22
               {"name": "idle", "in_use":False}, #D23
               {"name": "idle", "in_use":False}, #D24
               {"name": "idle", "in_use":False}, #D25
               {"name": "idle", "in_use":False}, #D26
               {"name": "idle", "in_use":False}, #D27
               {"name": "idle", "in_use":False}, #D28
               {"name": "idle", "in_use":False}, #D29
               {"name": "idle", "in_use":False}, #D30
               {"name": "idle", "in_use":False}, #D31
               {"name": "idle", "in_use":False}, #D32
               {"name": "idle", "in_use":False}, #D33
               {"name": "idle", "in_use":False}, #D34
               {"name": "idle", "in_use":False}, #D35
               {"name": "idle", "in_use":False}  #D36
              ]
}

control_instrument_configurations = {

    "CV3": [ {"name": "idle", "in_use": False, #D38
             "start_state": "LEFT"}, # or "RIGHT"

             {"name": "idle", "in_use": False, #D39
             "start_state": "LEFT"},

             {"name": "idle", "in_use": False, #D40
              "start_state": "LEFT"},

             {"name": "idle", "in_use": False, #D41
              "start_state": "LEFT"},

             {"name": "idle", "in_use": False, #D42
              "start_state": "LEFT"},

             {"name": "idle", "in_use": False, #D43
              "start_state": "LEFT"},
            ],

    "OCV_normallyOpen": [{"name": "UF OCV", "in_use": False, #D44
                          "start_state": "OPEN"},  # or "CLOSED"

                         {"name": "UF OCV", "in_use": False, #D45
                          "start_state": "OPEN"},

                         {"name": "UF OCV", "in_use": False, #D46
                          "start_state": "OPEN"},

                         ],

    "OCV_normallyClosed": [{"name": "UF OCV", "in_use": False, #D47
                            "start_state": "OPEN"}  # or "CLOSED"
                           ],

    "pump": [ {"name": "UF Feed Pump", "unit": "RPM", "in_use": True,  #D48 ON/OFF, DAC A
               "max_RPM": 9000.0, "starting_RPM": 0.0},

              {"name": "UF Backwash Pump", "unit": "RPM", "in_use": True,  #D49 ON/OFF, DAC B
               "max_RPM": 9000.0, "starting_RPM": 0.0}
            ],

    "PCV": [ {"name": "UF PCV", "unit": "%", "in_use": False, #DAC C
              "start_opening": 100.0},

             {"name": "ED PCV", "unit": "%", "in_use": False, #DAC D
              "start_opening": 40.0}
             ],

    "polarity": [ {"name": "ED Polarity", "in_use": False, #D50
                   "start_state": "POSITIVE"} #or "NEGATIVE"
                  ]
}

control_system_configurations = {
    "UF Massflow Control": {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                            "control_value_sensor_name": "UF Permeate Flow", "in_use": True,
                            "desired_flow": 5.0, "K_p": 0.7, "K_i": 0.2}
}

if __name__ == '__main__':

    for sensor in sensor_configurations["pressure"]:
        print(sensor["name"])
