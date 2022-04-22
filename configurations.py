
sensor_configurations = {
    "pressure": [  {"name": "UF Feed Pressure", "unit": "bar", "in_use": True,
                    "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7},

                  {"name": "UF Retentate Pressure", "unit": "bar","in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7},

                  {"name": "UF Permeate Pressure", "unit": "bar",  "in_use": True,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7},

                  {"name": "odle", "unit": "bar",  "in_use": False,
                   "max_pressure": 6.0, "critical_pressure": 5.0, "warning_pressure": 4.7}

                   ],

    "pressure_gems": [{"name": "ED Feed", "unit": "bar", "in_use": False,
                       "max_pressure": 5.0, "critical_pressure": 5.0, "warning_pressure": 4.7}
                      ],

    "massflow": [ {"name": "UF Feed Flow", "unit": "l/min", "in_use": True,
                   "max_flow": 20.0},

                  {"name": "UF Retentate Flow", "unit": "l/min", "in_use": True,
                   "max_flow": 10.0},

                  {"name": "UF Permeate Flow", "unit": "l/min", "in_use": True,
                   "max_flow": 5.0},

                  {"name": "idle", "unit": "l/min", "in_use": False,
                   "max_flow": 0}
                  ],

    "conductivity": [ {"name": "ED Feed Cond", "unit": "mS/cm", "in_use": False,
                       "max_Cond": 50.0},

                      {"name": "ED Diluate Cond", "unit": "mS/cm", "in_use": False,
                       "max_Cond": 50.0},

                      {"name": "ED Concentrate Cond", "unit": "mS/cm", "in_use": False,
                       "max_Cond": 50.0}

                      ],

    "temperature": [ {"name": "ED Feed Temp", "unit": "ºC",  "in_use": False,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0},

                     {"name": "ED Diluate Temp", "unit": "ºC", "in_use": False,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0},

                     {"name": "ED Concentrate Temp", "unit": "ºC", "in_use": False,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0},

                     {"name": "AC Tank Temp", "unit": "ºC", "in_use": False,
                      "max_Temp": 50.0, "critical_temp": 40.0, "warning_temp": 38.0} ],

    "level": [ {"name": "ED Feed Temp", "in_use":False}
              ]
}

control_instrument_configurations = {
    "pump": [ {"name": "UF Feed Pump", "unit": "RPM", "in_use": True,
               "max_RPM": 9000.0, "starting_RPM": 0.0},

              {"name": "UF Backwash Pump", "unit": "RPM", "in_use": True,
               "max_RPM": 9000.0, "starting_RPM": 0.0}
            ],
    "PCV": [ {"name": "UF PCV", "unit": "%", "in_use": False,
              "start_opening": 100.0},

             {"name": "ED PCV", "unit": "%", "in_use": False,
              "start_opening": 40.0}
             ]
}

control_system_configurations = {
    "UF Massflow Control": {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                            "control_value_sensor_name": "UF Permeate Flow", "in_use": True,
                            "desired_flow": 5.0, "K_p": 0.7, "K_i": 0.2}
}