"""
This file is used to configure the control systems of Apāson

All starting states of control instruments will be set here
"""

# MAKE SURE THE SENSORS AND PUMP NAMES ARE CONGRUOUS WITH THE NAMES IN CONF 1 + 2!!!!

control_configurations = {
    "uf_feed_flow":     {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                         "control_value_sensor_name": "UF Feed Flow", "control_instrument_name": "UF Feed Pump", "in_use": True,
                         "desired_value": 1.0, "K_p": 5, "K_i": 0.01},

    "uf_backwash_flow": {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                         "control_value_sensor_name": "UF Backwash Flow", "control_instrument_name": "UF Backwash Pump",
                         "in_use": True,
                         "desired_value": 1.0, "K_p": 5, "K_i": 0},

    "uf_tmp": {"control_value_sensor_type": "pressure", "control_value_sensor_unit": "bar",
                     "feed_pressure_sensor_name": "UF Feed Pressure", "permeate_pressure_sensor_name": "UF Permeate Pressure",
                     "in_use": True,
                     "switch_value": 0.8}, # Seconds

    "uf_general": {"uf_backwash_valve_name": "UF Backwash Valve", "uf_feed_valve_name": "UF Feed Valve", "uf_switch_valve_name": "UF Switch",
                   "uf_tank_high_ls_name": "UF Tank High", "uf_tank_middle_ls_name": "UF Tank Middle", "uf_tank_low_ls_name": "UF Tank Low",
                    "backwash_time": 90.0},

    "ed_general": {"ed_pre_diluate_valve_name": "ED Pre-Diluate", "ed_pre_concentrate_valve_name": "ED Pre-Concentrate",
                   "ed_post_diluate_valve_name": "ED Post-Diluate", "ed_post_concentrate_valve_name": "ED Post-Concentrate",
                   "ed_second_pre_diluate_valve_name": "ED Second-Pre-Diluate", "ed_concentrate_dilute_valve_name": "ED Dilute Concentrate",


                   "ed_con_tank_high_ls_name": "ED-Con Tank High", "ed_con_tank_middle_ls_name": "ED-Con Tank Middle",
                   "ed_split_tank_middle_ls_name": "ED-Split Tank Middle", "ed_split_tank_low_ls_name": "ED-Split Tank Low",
                   "ed_rinse_tank_ls_name": "ED-Rinse Tank", "uf_tank_low_ls_name": "UF Tank Low",

                   "reversal_time": 20.0}

}