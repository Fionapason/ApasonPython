

check_configurations = {
    "pressure": [[1, 6, 5, 4.7], [1, 6, 5, 4.7], [1, 6, 5, 4.7]], # [ Pressure 1 : [in use 1/0,  max pressure, critical value, warning value], Pressure 2: [...], Pressure 3: [...]]
    "massflow": [[1, 20], [1, 10], [1, 5], [1, 2]], #[ Massflow 1: [in use 1/0, max massflow], Massflow 2: [1/0, max mf], MF 3: [...], MF 4: [...]]
    "conductivity": [[1, 50], [1, 50], [1, 50]], # [Conductivity 1: [in use 1/0, max conductivity] Cond 2 : [...] Cond 3: [...] ]
    "temperature": [[1, 50, 40, 38], [1, 50, 40, 38], [1, 50, 40, 38], [1, 50, 40, 38]], # [Temp 1 : [in use 1/0, max ºC, critical ºC, warning ºC], Temp 2 : [1/0, max ºC, crit. ºC, warn. ºC], ... ]
    "level": [[1, 1]] # [Levelswitch 1 : [in use 1/0, max: 1/min: 0] ]
}

set_configurations = {
    "pump": [[1, 9000, 0], [1, 9000, 0]], # [ Pump 1: [ in use 1/0, max rpm, starting rpm ], Pump 2 : [1/0, max rpm, start rpm] ]
    "PCV": [[1, 5, 5, 0.7, 0.2, 1], [1, 2, 0, 0, 0, 2]], # [ PCV 1: [in use 1/0, start input voltage, desired massflow, Kp, Ki, mf control value], PCV 2: [...] ]
    #"CV3": [],
    #"OCV": []
}