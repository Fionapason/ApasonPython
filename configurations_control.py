"""
This file is used to configure the control systems of Apāson

All starting states of control instruments will be set here
"""

# MAKE SURE THE SENSORS AND PUMP NAMES ARE CONGRUOUS WITH THE NAMES IN CONF 1 + 2!!!!

control_configurations = {
    "uf_massflow_control": {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                            "control_value_sensor_name": "UF Feed Flow", "control_instrument_name": "UF Feed Pump", "in_use": True,
                            "desired_value": 5.0, "K_p": 5, "K_i": 0.01},

    "uf_backflush": {"control_value_sensor_type": "pressure", "control_value_sensor_unit": "bar",
                     "control_value_sensor_name_1": "UF Feed Pressure", "control_instrument_name": "UF Permeate Pressure",
                     "in_use": True,
                     "switch_value": 0.8, "backflush_time": 60.0} # Seconds

}