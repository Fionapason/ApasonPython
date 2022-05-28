"""
This file is used to configure the control systems of Apāson

All starting states of control instruments will be set here
"""

# MAKE SURE THE SENSORS AND PUMP NAMES ARE CONGRUOUS WITH THE NAMES IN CONF 1 + 2!!!!

control_configurations = {

    "uf_feed_flow":     {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                         "control_value_sensor_name": "UF Permeate Flow", "control_instrument_name": "UF Feed Pump", "in_use": True,
                         "desired_value": 1.5, "K_p": 0.5, "K_i": 0.01},

    "uf_backwash_flow": {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                         "control_value_sensor_name": "UF Backwash Flow", "control_instrument_name": "UF Backwash Pump",
                         "in_use": True,
                         "desired_value": 1.0, "K_p": 0.5, "K_i": 0},

    "uf_tmp": {"control_value_sensor_type": "pressure", "control_value_sensor_unit": "bar",
                     "feed_pressure_sensor_name": "UF Feed Pressure", "permeate_pressure_sensor_name": "UF Permeate Pressure",
                     "in_use": True,
                     "switch_value": 1.0}, # bar

    "uf_general": {"uf_backwash_valve_name": "UF Backwash Valve", "uf_feed_valve_name": "UF Feed Valve",
                   "uf_switch_valve_name": "UF Switch",
                   "uf_tank_high_ls_name": "UF Tank High", "uf_tank_middle_ls_name": "UF Tank Middle",
                   "uf_tank_low_ls_name": "UF Tank Low",
                   "backwash_time": 90.0},  # Seconds


    "ed_pt_flow":           {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                            "control_value_sensor_normal_name": "Posttreatment Flow", "control_value_sensor_reversal_name": "Posttreatment Flow",
                             "control_instrument_name": "Posttreatment Pump", "in_use": True,
                            "desired_value": 0.25, "K_p": 0.7, "K_i": 0.01, "pressure_dependent": False},

    "ed_rinse_flow":        {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                            "control_value_sensor_normal_name": "ED Rinse Flow", "control_value_sensor_reversal_name": "ED Rinse Flow",
                             "control_instrument_name": "Rinse Pump", "in_use": True,
                            "desired_value": 2.5, "K_p": 0.7, "K_i": 0.0, "pressure_dependent": False},

    "ed_concentrate_flow":  {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                            "control_value_sensor_normal_name": "Concentrate Flow", "control_value_sensor_reversal_name": "ED Diluate Flow",
                             "control_instrument_name": "Concentrate Pump", "in_use": True,
                            "desired_value": 0.25, "K_p": 1.0, "K_i": 0.0, "pressure_dependent": True},

    "ed_diluate_flow":     {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                            "control_value_sensor_normal_name": "ED Diluate Flow", "control_value_sensor_reversal_name": "Concentrate Flow",
                            "control_instrument_name": "Diluate Pump", "in_use": True,
                            "desired_value": 0.25, "K_p": 1.0, "K_i": 0.0, "pressure_dependent": True},


    "ed_pressures": {"diluate_pressure_sensor_name": "Diluate In Pressure",
                     "concentrate_pressure_sensor_name": "Concentrate In Pressure",
                     "rinse_pressure_sensor_name" :"Rinse Pressure",
                     "in_use": True,
                     "critical_value_DC": 0.1, "critical_value_RD": 0.2},

    "ed_conductivity": {"conductivity_sensor_name": "ED Diluate Out Cond", "control_cv3": "ED Second-Pre-Diluate",
                        "desired_value": 0.9, "minimum_flow": 0.25, "maximum_flow": 1.67,
                        "K_p": 0.8, "K_i": 0.0}, # TODO ADJUST

    "ed_general": {"ed_pre_diluate_valve_name": "ED Pre-Diluate", "ed_pre_concentrate_valve_name": "ED Pre-Concentrate",
                   "ed_post_diluate_valve_name": "ED Post-Diluate", "ed_post_concentrate_valve_name": "ED Post-Concentrate",
                   "ed_second_pre_diluate_valve_name": "ED Second-Pre-Diluate", "ed_concentrate_dilute_valve_name": "ED Dilute Concentrate",


                   "ed_con_tank_high_ls_name": "ED-Con Tank High", "ed_con_tank_middle_ls_name": "ED-Con Tank Middle",
                   "ed_split_tank_middle_ls_name": "ED-Split Tank Middle", "ed_split_tank_low_ls_name": "ED-Split Tank Low",
                   "ed_rinse_tank_ls_name": "ED-Rinse Tank", "uf_tank_low_ls_name": "UF Tank Low",

                   "ed_concentrate_conductivity_name": "ED Concentrate Cond",
                   "reversal_time": 20.0},

    "overall_control": {"overall_feed_tank_high_ls_name": "Feed Tank High", "overall_feed_tank_middle_ls_name": "Feed Tank Middle",
                        "overall_feed_tank_low_ls_name": "Feed Tank Low",

                        "overall_purge_tank_middle_ls_name": "Purge Tank Middle", "overall_purge_tank_high_ls_name": "Purge Tank High",
                        "overall_rinse_tank_ls_name": "ED-Rinse Tank"

                       }

}