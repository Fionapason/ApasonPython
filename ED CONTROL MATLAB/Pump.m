classdef Pump < handle %ED General Code
    
    properties (GetAccess = public, SetAccess = protected)
        
        Ki %Integral Constant
        
        Kp %Proportional Constant
        
        name
        
        maxValue
        
        minValue = 0.6;
        
        command = ['!', '@', '#', '$'];
        
        arduinoObj
        
        pumpTimer
        
    end
    
    properties
        
        data = 0; % to store
        
        time = 0;
        
        value
        
        controlTime = 0;
        
        setValue
        
        integral
        
        nonSatV
        
        setFlow % A specific flow we want to achieve
        
        count
        
        pressureSensors
        
        beginTimeIdentifier
        
        setTime
        
        Interface
        
        stopIdentifier
        
        tmpCount = 1;
        
        mfObj %to say which massflowsensor is used for comparison
        
        adjustment

    end


    methods
        function O = Pump(arduinoObj, maxValue, identifier, name, setFlow, Kp, Ki, mfObj, pressureSensors, Interface)

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
            O.setFlow.value = setFlow;
            O.setFlow.t = 0;
            O.integral = 0;
            O.Kp = Kp;
            O.Ki = Ki;
            O.mfObj = mfObj;
            O.value = 0; %to say to which Voltage it is set in the beginning
            O.setValue = 0;
            O.nonSatV = 0; % in the beginning they are the same
            O.count = 0;
            O.pressureSensors = pressureSensors;
            O.Interface = Interface;
            O.adjustment = 1;

            O.pumpTimer = timer('ExecutionMode', 'fixedSpacing','Period',1);
            O.pumpTimer.StartFcn = @(~,~)disp([char(O.name), ' Controller started']);
            O.pumpTimer.StopFcn = @(~,~)disp([char(O.name), ' Controller stopped']);
            O.pumpTimer.TimerFcn = @(~,~)controlFlow(O);

        end % constructor
        
        
        function changeSetting(O)
            
            arduinoValue = (O.value/O.maxValue)*4095;
            
            if arduinoValue > 4095
                error(['The input value has to be smaller or equal to ', num2str(O.value), ' rpm']);
            elseif arduinoValue < 0
                error(['The input value has to be a positive number and smaller or equal to ', num2str(arduinoValue), ' rpm']);
            end
            
            O.arduinoObj.writeCommand(O.command, num2str(arduinoValue));
            
        end %changeSetting
        
        function controlFlow(O) %Controller
            
            
            O.controlTime(end+1) = (now - O.pressureSensors(O.beginTimeIdentifier).time(2))*24*3600;
            
            if O.count == 0
                elapsedTime = (O.controlTime(end)-O.mfObj.time(end));
                O.stopIdentifier = length(O.controlTime);
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
            
            O.value = O.value + out;
            
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

