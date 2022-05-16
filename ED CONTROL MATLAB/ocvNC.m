classdef ocvNC < handle % ED General Code
    
    properties (GetAccess = public, SetAccess = protected)
        
        name
        
        commandopen = ['R' 'S' 'T']; %D44 - D46
        
        commandclose = ['V' 'W' 'X']; %D44
        
        arduinoObj
        
    end
    
    properties
        
        data = 0; % to store
        
        time = 0; %to store

        controlTime = 0;
        
        value;
        
        setValue = 0; %in the beginning
        
        count
        
    end
    
    methods
        function O = ocvNC(arduinoObj, identifier, name)
            
            if ~isa(arduinoObj,'talkToArduino')
                error('Input argument 1 has to be talkToArduino class object');
            elseif identifier > 3 || identifier < 1
                error('Input argument 2 has to be a number between 1 and 3');
            elseif ~isstring(name)
                error('Input argument 3 has to be a string for the name');
            end
            
            O.commandopen = O.commandopen(identifier);
            O.commandclose = O.commandclose(identifier);
            O.arduinoObj = arduinoObj;
            O.name = name;
            O.value = 5; %in the beginning it is closed
            
        end %end constructor
        
        function open(O) %change the position of the valve
            
            O.arduinoObj.valveSendCommand(O.commandopen);
            
            O.value = 0;
            
        end %end open
        
        function close(O)
            
            O.arduinoObj.valveSendCommand(O.commandclose);
            
            O.value = 5;
            
        end %end close
     
    end %methods
end
