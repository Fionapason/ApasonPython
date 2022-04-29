sensor_configurations = {

    "pressure": [  {"id": 0, "arduino_id": 1,
                    "name": "GEMS", "unit": "bar", "in_use": True,
                    "max_pressure": 5.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A0

                   {"id": 1, "arduino_id": 1,
                    "name": "UF Feed Pressure", "unit": "bar", "in_use": True,
                    "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A1

                  {"id": 2, "arduino_id": 1,
                   "name": "UF Retentate Pressure", "unit": "bar","in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A2

                  {"id": 3, "arduino_id": 1,
                   "name": "UF Permeate Pressure", "unit": "bar",  "in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}, #A3

                  {"id": 4, "arduino_id": 1,
                   "name": "idle", "unit": "bar",  "in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7} #A4

                   ],

    "massflow": [ {"id": 0, "arduino_id": 1,
                   "name": "UF Feed Flow", "unit": "l/min", "in_use": True, #A5
                   "max_flow": 20.0},

                  {"id": 1, "arduino_id": 1,
                   "name": "UF Retentate Flow", "unit": "l/min", "in_use": True, #A6
                   "max_flow": 10.0},

                  {"id": 2, "arduino_id": 1,
                   "name": "UF Permeate Flow", "unit": "l/min", "in_use": True, #A7
                   "max_flow": 5.0},

                  {"id": 3, "arduino_id": 1,
                   "name": "idle", "unit": "l/min", "in_use": True, #A8
                   "max_flow": 0}
                  ],

    "conductivity": [ {"id": 0, "arduino_id": 1,
                       "name": "ED Feed Cond", "unit": "mS/cm", "in_use": True, #A9
                       "max_Cond": 50.0, "min_Cond": 0.1},

                      {"id": 1, "arduino_id": 1,
                       "name": "ED Diluate Cond", "unit": "mS/cm", "in_use": True, #A10
                       "max_Cond": 50.0, "min_Cond": 0.1},

                      {"id": 2, "arduino_id": 1,
                       "name": "ED Concentrate Cond", "unit": "mS/cm", "in_use": True, #A11
                       "max_Cond": 50.0, "min_Cond": 0.1}

                      ],

    "temperature": [ {"id": 0, "arduino_id": 1,
                      "name": "ED Feed Temp", "unit": "ºC",  "in_use": True,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}, #A12

                     {"id": 1, "arduino_id": 1,
                      "name": "ED Diluate Temp", "unit": "ºC", "in_use": True,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}, #A13

                     {"id": 2, "arduino_id": 1,
                      "name": "ED Concentrate Temp", "unit": "ºC", "in_use": True,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0} #A14

                    # ,
                    #  {"id": 3, "arduino_id": 1,
                    #   "name": "AC Tank Temp", "unit": "ºC", "in_use": True,
                    #   "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0}  #A15
                     ],


    "level": [ {"id": 0, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D22
               {"id": 1, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D23
               {"id": 2, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D24
               {"id": 3, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D25
               {"id": 4, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D26
               {"id": 5, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D27
               {"id": 6, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D28
               {"id": 7, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D29
               {"id": 8, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D30
               {"id": 9, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D31
               {"id": 10, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D32
               {"id": 11, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D33
               {"id": 12, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D34
               {"id": 13, "arduino_id": 1,
                "name": "idle", "in_use": True}, #D35
               {"id": 14, "arduino_id": 1,
                "name": "idle", "in_use": True}  #D36
              ]
}

control_instrument_configurations = {

    "CV3": [ {"id": 0, "arduino_id": 1,
              "name": "idle", "in_use": False, #D38
             "start_state": "LEFT"}, # or "RIGHT"

             {"id": 1, "arduino_id": 1,
              "name": "idle", "in_use": False, #D39
             "start_state": "LEFT"},

             {"id": 2, "arduino_id": 1,
              "name": "idle", "in_use": False, #D40
              "start_state": "LEFT"},

             {"id": 3, "arduino_id": 1,
              "name": "idle", "in_use": False, #D41
              "start_state": "LEFT"},

             {"id": 4, "arduino_id": 1,
              "name": "idle", "in_use": False, #D42
              "start_state": "LEFT"},

             {"id": 5, "arduino_id": 1,
              "name": "idle", "in_use": False, #D43
              "start_state": "LEFT"},
            ],

    "OCV_normallyOpen": [{"id": 0, "arduino_id": 1,
                          "name": "UF OCV", "in_use": False, #D44
                          "start_state": "OPEN"},  # or "CLOSED"

                         {"id": 1, "arduino_id": 1,
                          "name": "UF OCV", "in_use": False, #D45
                          "start_state": "OPEN"},

                         {"id": 2, "arduino_id": 1,
                          "name": "UF OCV", "in_use": False, #D46
                          "start_state": "OPEN"},

                         ],

    "OCV_normallyClosed": [{"id": 0, "arduino_id": 1,
                            "name": "UF OCV", "in_use": False, #D47
                            "start_state": "OPEN"}  # or "CLOSED"
                           ],

    #PUMP AND PCV SHARE THEIR IDS BECAUSE OF THE DAC

    "pump": [ {"id": 0,  "DAC_output": 'A',"arduino_id": 1,
               "name": "UF Feed Pump", "unit": "RPM", "in_use": True,  #D48 ON/OFF, DAC A
               "max_RPM": 9000.0, "starting_RPM": 0.0},

              {"id": 1, "DAC_output": 'B', "arduino_id": 1,
               "name": "UF Backwash Pump", "unit": "RPM", "in_use": True,  #D49 ON/OFF, DAC B
               "max_RPM": 9000.0, "starting_RPM": 0.0}
            ],

    "PCV": [ {"id": 0, "DAC_output": 'C', "arduino_id": 1,
              "name": "UF PCV", "unit": "%", "in_use": False, #DAC C
              "start_opening": 100.0},

             {"id": 1, "DAC_output": 'D', "arduino_id": 1,
              "name": "ED PCV", "unit": "%", "in_use": False, #DAC D
              "start_opening": 40.0}
             ],

    "polarity": [ {"id": 0, "arduino_id": 1,
                   "name": "ED Polarity", "in_use": False, #D50
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
