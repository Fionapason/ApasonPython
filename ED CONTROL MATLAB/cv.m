classdef cv < handle 
    %UNTITLED5 Summary of this class goes here
    %   Detailed explanation goes here
    
    % this file was copied from PCV by Yannik on 18.04.22
    
    properties (GetAccess = public, SetAccess = protected)
        
        name
        
        commandopen = ['F' 'G' 'H' 'I' 'J']; % D38 - D41
        
        commandclose = ['L' 'M' 'N' 'O' 'P']; % D38 - D41
        
        arduinoObj
        
    end
    
    properties
        
        data = 0; % to store
        
        time = 0; %to store

        controlTime = 0;
        
        value = 0;
        
        setValue = 0; %in the beginning
        
        count
        
    end
    
    methods
        
        function O = cv(arduinoObj, identifier, name)
            
            if ~isa(arduinoObj,'talkToArduino')
                error('Input argument 1 has to be talkToArduino class object');
            elseif identifier > 4 || identifier < 1
                error('Input argument 2 has to be a number between 1 and 4');
            elseif ~isstring(name)
                error('Input argument 3 has to be a string for the name');
            end
            
            O.commandopen = O.commandopen(identifier);
            O.commandclose = O.commandclose(identifier);
            O.arduinoObj = arduinoObj;
            O.name = name;
            
        end %end constructor
        
        function open(O) %change the position of the valve
            
            O.arduinoObj.valveSendCommand(O.commandopen);
            
            O.value = 5;
            
        end %end open
        
        function close(O)
            
            O.arduinoObj.valveSendCommand(O.commandclose);
            
            O.value = 0;
            
        end %end close
            
     
    end %methods
end
