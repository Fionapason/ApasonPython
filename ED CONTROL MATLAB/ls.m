classdef ls < handle %UF General Code -- level switch

    properties (GetAccess = public, SetAccess = protected)

        name

        on = 1;

        closed = 0;

        command = ['q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A']; %D22 - D32

        arduinoObj

    end

    properties

        data = 0; % to store

        time = 0; %to store

    end

    properties (Dependent)

        value

    end

    methods
        function O = ls(arduinoObj, identifier, name)

            if ~isa(arduinoObj,'talkToArduino')
                error('Input argument 1 has to be talkToArduino class object');
            elseif identifier > 8 || identifier < 1
                error('Input argument 2 has to be a number between 1 and 8');
            elseif ~isstring(name)
                error('Input argument 3 has to be a string for the name');
            end

            O.arduinoObj = arduinoObj;
            O.command = O.command(identifier);
            O.name = name;
            O.data = O.value;


        end % constructor

        function f = get.value(O)

            f = O.arduinoObj.sendCommand(O.command);

        end %end get the value


    end %methods
end
