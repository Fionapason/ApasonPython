classdef Polarity < handle
    %UNTITLED5 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties (GetAccess = public, SetAccess = protected)
        
        name
        
        arduinoObj
        
    end
    
    properties
        
        data = 0; % to store
        
        time = 0;
        
        value
        
    end
    
    
    methods
        function O = Polarity(arduinoObj, name, initialState)
            
            if ~isa(arduinoObj,'talkToArduino')
                error('Input argument 1 has to be talkToArduino class object');
            elseif ~isstring(name)
                error('Input argument 2 has to be a string for the name');
            end
            
            O.arduinoObj = arduinoObj;
            O.name = name;
            O.value = initialState;
            
            O.arduinoObj.sendCommand('(');
        end % constructor
        
        function changeSetting(O)
            
            if O.value == 1
               O.arduinoObj.sendCommand('('); %normal polarity

            elseif O.value == -1
               O.arduinoObj.sendCommand(')'); %negative

            elseif O.value == 0
                O.arduinoObj.sendCommand('*'); %off

            else
                error('Changing ED polarity to undefined state')
            end

        end %changeSetting
        
     
    end %methods
end

