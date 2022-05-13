classdef pcv < handle %UF3
    %UNTITLED5 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties (GetAccess = public, SetAccess = protected)
        
        Ki %Integral Constant
        
        Kp %Proportional Constant
        
        name
        
        maxValue = 5; %Volt
        
        minValue = 0; %Volt
        
        command = ['$', '#']; %D and C - because configuration is wrong
        
        arduinoObj
        
        mfObj %to say which massflowsensor is used for comparison

        pcvTimer
        
    end
    
    properties
        
        data = 0; % to store
        
        time = 0; %to store

        controlTime = 0;
        
        value
        
        setValue
        
        integral
        
        nonSatV
        
        setFlow % A specific flow we want to achieve
        
        count
        
        pressureSensors
        
        beginTimeIdentifier
        
    end
    
    methods
        function O = pcv(arduinoObj, identifier, name, firstValue, setFlow, Kp, Ki, mfObj, pressureSensors)
            
            if ~isa(arduinoObj,'talkToArduino')
                error('Input argument 1 has to be talkToArduino class object');
            elseif identifier > 4 || identifier < 1
                error('Input argument 2 has to be a number between 1 and 4');
            elseif ~isstring(name)
                error('Input argument 3 has to be a string for the name');
            elseif firstValue < O.minValue || firstValue > O.maxValue
                error('Input argument 4 has to be in between 0.5 and 5 Volt');
            end
            
            O.arduinoObj = arduinoObj;
            O.command = O.command(identifier);
            O.name = name;
            O.setFlow.value = setFlow;
            O.setFlow.t = 0;
            O.integral = 0;
            O.Kp = Kp;
            O.Ki = Ki;
            O.mfObj = mfObj;
            O.value = firstValue; %to say to which Voltage it is set in the beginning
            O.setValue = firstValue;
            O.nonSatV = firstValue; % in the beginning they are the same
            O.count = 0;
            O.pressureSensors = pressureSensors;

            O.pcvTimer = timer('ExecutionMode', 'fixedSpacing','Period',1);
            O.pcvTimer.StartFcn = @(~,~)disp('Valve Controller started');
            O.pcvTimer.StopFcn = @(~,~)disp('Valve Controller stopped');
            O.pcvTimer.TimerFcn = @(~,~)controlPermeateFlow(O);

        end % constructor
        
        function changeSetting(O) %change the position of the valve
            
            arduinoValue = (O.value/O.maxValue)*4095;
            
            if arduinoValue > 4095
                error('Input argument 1 has to be smaller or equal to 5 Volt');
            end
            
            O.arduinoObj.writeCommand(O.command, num2str(arduinoValue));
            
        end %changeSetting
        
        function controlPermeateFlow(O) %Controller
            
            O.controlTime(end+1) = (now - O.pressureSensors(O.beginTimeIdentifier).time(2))*24*3600;
            
            if O.count == 0
                elapsedTime = (O.controlTime(end)-O.mfObj.time(end));
            else
                elapsedTime = (O.controlTime(end)-O.controlTime(end-1));
            end
            
            actualValue = O.mfObj.value;
            
            while isnan(actualValue)
                actualValue = O.mfObj.value;
            end

            error = O.setFlow.value(end) - actualValue;
            
            %Proportional Controller
            P_out = O.Kp*error;
            
            %Integrative Controller
            if O.nonSatV ~= O.value
                I_out = 0;
            else
                O.integral = O.integral + elapsedTime*error;
                I_out = O.Ki*O.integral;
            end
            
            out = P_out + I_out;
            
            O.value = O.value - out;
            
            O.nonSatV = O.value;
            
            if O.value > O.maxValue
                O.value = O.maxValue;
            elseif O.value < O.minValue
                O.value = O.minValue;
            end
            
            O.setValue(end+1) = O.value;
            
            O.changeSetting;
            
            O.count = O.count + 1;

        end %controlFlow
        
     
    end %methods
end
