"""
This file is used to configure the control systems of Apāson

All starting states of control instruments will be set here
"""

control_system_configurations = {
    "uf_massflow_control": {"control_value_sensor_type": "massflow", "control_value_sensor_unit": "l/min",
                            "control_value_sensor_name": "UF Feed Flow", "control_instrument_name": "UF Feed Pump", "in_use": True,
                            "desired_value": 5.0, "K_p": 5, "K_i": 0.01} #  I think Pump ID would be better
}