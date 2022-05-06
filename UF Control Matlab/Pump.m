classdef Pump < handle %UF3
    
    % Now this Pump can also be used as a controller (22.4.22 - Dana)
    
     properties (GetAccess = public, SetAccess = protected)
        
        Ki %Integral Constant
        
        Kp %Proportional Constant
        
        name
        
        maxValue
        
        minValue = 0.6;
        
        command = [ '!', '@'];
        
        arduinoObj
        
        pumpTimer
        
        setupTimer
        
        mfObj %to say which massflowsensor is used for comparison
        
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
        
        setTime
        
        Interface
        
        stopIdentifier
        
        tmpCount = 1;
        
    end
    
    methods
        function O = Pump(arduinoObj, maxValue, identifier, name, setFlow, Kp, Ki, mfObj, pressureSensors, setTime, Interface)
            
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
            O.maxValue = maxValue; % 5 Volt
            O.command = O.command(identifier);
            O.name = name;
            O.setFlow.value = setFlow; % desired flow value
            O.setFlow.t = 0; % time at which desired value was changed
            O.integral = 0;
            O.Kp = Kp;
            O.Ki = Ki;
            O.mfObj = mfObj;
            O.value = 0; %to say to which Voltage it is set in the beginning // volt
            O.setValue = 0; % vector of all volt values
            O.nonSatV = 0; % in the beginning they are the same
            O.count = 0; % loops
            O.pressureSensors = pressureSensors; % for time
            O.setTime = setTime; % for backwash time
            O.Interface = Interface;

            O.pumpTimer = timer('ExecutionMode', 'fixedSpacing','Period',1);
            O.pumpTimer.StartFcn = @(~,~)disp([char(O.name), ' Controller started']);
            O.pumpTimer.StopFcn = @(~,~)disp([char(O.name), ' Controller stopped']);
            O.pumpTimer.TimerFcn = @(~,~)controlFlow(O);

        end % constructor
        
        
        function changeSetting(O)
            
            arduinoValue = (O.value(end)/O.maxValue)*4095;
            
            if arduinoValue > 4095
                error(['The input value has to be smaller or equal to ', num2str(O.maxValue), ' rpm']);
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
            
%            while isnan(actualValue)
%                actualValue = O.mfObj.value;
%            end

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
            
            O.setValue(end+1) = O.value; %for display
            
            O.changeSetting;
            
            O.count = O.count + 1;
            
            if O.setTime ~= 1 %"if this is a backwash pump"
                if (O.controlTime(end)- O.controlTime(O.stopIdentifier)) > O.setTime
                    stop(O.pumpTimer)
                    pause(1)
                    O.value = 0;
                    O.setValue(end+1) = O.value;
                    O.changeSetting;
%                     start(O.Interface.normalSetup);
%                     O.Interface.GUI.startBackwashButton.Value = false;
                    O.count = 0;
                    O.Interface.feedCount = 0;
                end
            elseif O.setTime == 1 
                if (O.controlTime(end)- O.controlTime(O.stopIdentifier)) > 60 && O.tmpCount == 1 %wait one minute for the feed pump such that it will measure the current TMP
                    O.Interface.sensor.transmembrane.begin = sum(O.Interface.sensor.transmembrane.data(end-2:end))/3; %relies on a log!
                    O.Interface.sensor.transmembrane.end = O.Interface.sensor.transmembrane.begin + 0.2;
                    O.tmpCount = 0;
                elseif sum(O.Interface.sensor.transmembrane.data(end-2:end))/3 > O.Interface.sensor.transmembrane.end && O.tmpCount == 0 %tmpCount tells you if TMPbegin has been measured or not
                    stop(O.pumpTimer)
                    pause(0.5)
                    disp('The transmembrane pressure went 0.2 bar higher than the beginning, so the feed pump stopped');
                    O.value = 0;
                    O.setValue(end+1) = O.value;
                    O.changeSetting;
                    O.Interface.GUI.startPumpButton.Value = false;
                    O.count = 0;
                    O.tmpCount = 1;
                    O.Interface.feedCount = 2;
                end
            end
            
        end %controlFlow
     
    end %methods
end

