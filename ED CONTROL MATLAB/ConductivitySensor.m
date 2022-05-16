classdef ConductivitySensor < handle
    properties (GetAccess = public, SetAccess = protected)
        
        name
        
        maxValue
        
        command = ['j' 'k' 'l'];
        
        arduinoObj
        
        minConductivity;
        
        minVoltage = 1; % check if the 250 Ohm resistor is attached!!
        
        maxVoltage = 5;
        
    end
    
    properties
        
        data % to store
        
        time

    end
    
    properties (Dependent)
        
        value
        
    end
    
    
    methods
        
        % command = ['j' 'k' 'l'];
        
        function O = ConductivitySensor(arduinoObj, maxValue, minValue, identifier, name)
            
            if ~isa(arduinoObj,'talkToArduino')
                error('Input argument 1 has to be talkToArduino class object');
            elseif ~isnumeric(maxValue)
                error('Input argument 2 has to be a double for the maxValue');
            elseif identifier > 4 || identifier < 1
                error('Input argument 3 has to be a number between 1 and 4');
            elseif ~isstring(name)
                error('Input argument 4 has to be a string for the name');
            end
            
            O.arduinoObj = arduinoObj;
            O.maxValue = maxValue;
            O.minConductivity = minValue;
            O.command = O.command(identifier);
            O.name = name;
            O.data = 0;
            O.time = 0;
        end % end constructor
        
        function f = get.value(O)
            
            % get the value from the arduino
            raw_conductivity_measurement = O.arduinoObj.sendCommand(O.command);
            
            graphConstant = O.maxValue - ((O.maxValue - O.minConductivity) / (O.maxVoltage - O.minVoltage))*O.maxVoltage;
            
            %calculate the data into l/min
            f = raw_conductivity_measurement * (O.arduinoObj.analogReference / 1023) * ((O.maxValue - O.minConductivity) / (O.maxVoltage - O.minVoltage)) + graphConstant;

        end %end get the value
        
         
    end %end methods
       
    
end