classdef massFlowSensor < handle
    properties (GetAccess = public, SetAccess = protected)
        
        name
        
        maxValue
        
        command = ['f' 'g' 'h' 'i'];
        
        arduinoObj
        
        minMassflow = 0;
        
        minVoltage = 1; % check if the 250 Ohm resistor is attached!!
        
        maxVoltage = 5;
        
        graphConstant
    end

    properties

        data % to store

        time

    end

    properties (Dependent)

        value

    end


    methods

        % command = ['f' 'g' 'h' 'i'];

        function O = massFlowSensor(arduinoObj, maxValue, identifier, name)

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
            O.command = O.command(identifier);
            O.name = name;
            O.data = 0;
            O.time = 0;
            O.graphConstant = O.maxValue - ((O.maxValue - O.minMassflow) / (O.maxVoltage - O.minVoltage))*O.maxVoltage;

        end % end constructor

        function f = get.value(O)

            % get the value from the arduino
            raw_flow_measurement = O.arduinoObj.sendCommand(O.command);

            %calculate the data into l/min
            f = raw_flow_measurement * (O.arduinoObj.analogReference / 1023) * ((O.maxValue - O.minMassflow) / (O.maxVoltage - O.minVoltage)) + O.graphConstant;

        end %end get the value
        
         
    end
    
    
    
    
    
end