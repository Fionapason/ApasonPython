classdef ConductivitySensor < handle
    properties (GetAccess = public, SetAccess = protected)
        
        name
        
        maxCond

        command = ['j' 'k' 'l'];

        arduinoObj

        minCond

        minVoltage = 1; % check if the 250 Ohm resistor is attached!!

        maxVoltage = 5;

        setCond = 0.9; % mS/cm

        Kp

        Ki

        minFlow = 0.25; %l/min -- 15l/h this is the lowest possible flow measurement we can read accurately

    end

    properties

        data % to store

        time

        maxFlow = 1.67; %l/min -- 100 l/h

        concControl

        Interface

        nonSatFlow

        count

        controlTime

        integral

        pumpObj

        setFlow

    end

    properties (Dependent)

        value

    end


    methods

        % command = ['j' 'k' 'l'];

        function O = ConductivitySensor(arduinoObj, maxCond, minCond, Kp, Ki, identifier, name, Interface)

            if ~isa(arduinoObj,'talkToArduino')
                error('Input argument 1 has to be talkToArduino class object');
            elseif ~isnumeric(maxCond)
                error('Input argument 2 has to be a double for the maxValue');
            elseif identifier > 4 || identifier < 1
                error('Input argument 3 has to be a number between 1 and 4');
            elseif ~isstring(name)
                error('Input argument 4 has to be a string for the name');
            end

            O.arduinoObj = arduinoObj;
            O.maxCond = maxCond;
            O.minCond = minCond;
            O.command = O.command(identifier);
            O.name = name;
            O.data = 0;
            O.time = 0;
            O.Kp = Kp;
            O.Ki = Ki;
            O.integral = 0;
            O.Interface = Interface;
            O.nonSatFlow = O.minFlow;
            O.setFlow = O.minFlow;
            O.controlTime = 0;
            O.count = 0;


            O.concControl = timer('ExecutionMode', 'fixedSpacing','Period', 5);

            O.concControl.StartFcn = @(~,~)disp('Concentration Controller started');

            O.concControl.StopFcn = @(~,~)disp('Concentration Controller is finished');

            O.concControl.TimerFcn = @(~,~)controlSystemConcentration(O);
        end % end constructor

        function f = get.value(O)

            % get the value from the arduino
            raw_conductivity_measurement = O.arduinoObj.sendCommand(O.command);

            graphConstant = O.maxCond - ((O.maxCond - O.minCond) / (O.maxVoltage - O.minVoltage))*O.maxVoltage;

            %calculate the data into l/min
            f = raw_conductivity_measurement * (O.arduinoObj.analogReference / 1023) * ((O.maxCond - O.minCond) / (O.maxVoltage - O.minVoltage)) + graphConstant;

        end %end get the value

        function controlSystemConcentration(O)

            O.controlTime(end+1) = (now - O.Interface.sensor.pressure(O.Interface.sensor.beginTimeIdentifier).time(2))*24*3600;

            if O.count == 0
                elapsedTime = (O.controlTime(end)-O.time(end));
            else
                elapsedTime = (O.controlTime(end)-O.controlTime(end-1));
            end

            actualValue = O.value; % the conductivity that we actually have now

            while isnan(actualValue)
                actualValue = O.value;
            end

            error = O.setCond - actualValue;

            %Proportional Controller
            P_out = O.Kp*error;

            %Integrative Controller
            if O.nonSatFlow ~= O.setFlow
                I_out = 0;
            else
                O.integral = O.integral + elapsedTime*error;
                I_out = O.Ki*O.integral;
            end

            out = P_out + I_out;

            O.setFlow = O.setFlow + out;


            O.nonSatFlow = O.setFlow;

            if O.setFlow > O.maxFlow
                O.setFlow = O.maxFlow;
            elseif O.setFlow < O.minFlow
                O.setFlow = O.minFlow;
            end

            for identifier = [1 3 4] % all but the rinse
                O.Interface.sensor.pump(identifier).setFlow.value(end) = O.setFlow;
                O.Interface.sensor.pump(identifier).setFlow.t(end) = (now - O.Interface.sensor.pressure(O.Interface.sensor.beginTimeIdentifier).time(2))*24*3600;
            end

            if actualValue > 1 && O.Interface.sensor.cv(5).value == 0
                O.Interface.sensor.cv(5).open % value = 5 -- change sucht that it goes into the concentrate tank
            elseif actualValue < 1 && O.Interface.sensor.cv(5).value == 5
                O.Interface.sensor.cv(5).close % value = 0 -- normal
            end

            O.count = O.count + 1;

        end %controlSystemConcentration
        
         
    end %end methods
       
    
end