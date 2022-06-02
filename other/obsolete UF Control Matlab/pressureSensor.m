classdef pressureSensor < handle
    %UNTITLED3 Summary of this class goes here
    % Detailed explanation goes here
    
    properties (GetAccess = public, SetAccess = protected)
        
        name
        
        maxValue
        
        command = ['b' 'c' 'd'];
        
        arduinoObj
        
        criticalValue %maximum pressure that should not be exceeded
        
        warningValue %value where a warning is displayed
        
        pressureTimer
        
        closeButton
        
    end
    
    properties
        
        data = 0; % to store
        
        time = 0;
        
        num = 0;
        
        Interface
    end
    
    properties (Dependent)
        
        value
        
    end
    
    methods
        
        function O = pressureSensor(arduinoObj, maxValue, identifier, name, criticalValue, warningValue, closeButton, Interface) 
            
            if ~isa(arduinoObj,'talkToArduino')
                error('Input argument 1 has to be talkToArduino class object');
            elseif ~isnumeric(maxValue)
                error('Input argument 2 has to be a double for the maxValue');
            elseif identifier > 5 || identifier < 1
                error('Input argument 3 has to be a number between 1 and 5'); % 
            elseif ~isstring(name)
                error('Input argument 4 has to be a string for the name'); % "" is for string
            end
            
            O.arduinoObj = arduinoObj;
            O.maxValue = maxValue;
            O.command = O.command(identifier);
            O.name = name;
            O.criticalValue = criticalValue;
            O.warningValue = warningValue;
            O.closeButton = closeButton;
            O.Interface = Interface;
            
            O.pressureTimer = timer('ExecutionMode', 'fixedSpacing','Period',1);
            O.pressureTimer.StartFcn = @(~,~)disp('Pressure Tester started');
            O.pressureTimer.StopFcn = @(~,~)disp('Pressure Tester stopped');
            O.pressureTimer.TimerFcn = @(~,~)controlCriticalValue(O);
        end % end constructor
        
        function f = get.value(O)
            
            % get the value from the arduino
            raw_pressure_measurement = O.arduinoObj.sendCommand(O.command);
            
            %calculate the data into bar
            f = raw_pressure_measurement * O.arduinoObj.analogReference * O.maxValue/(1023*5);
            
        end % end get value
        
        function controlCriticalValue(O)
            
            average = sum(O.data(end-2:end))/3;
            
            if average > O.criticalValue
                disp(['The pressure sensor ', num2str(O.name), ' has reached the critical value so the pumps and arduino were shut down']);
                
                O.Interface.endSystem;
                % SET THE PUMPS TO 0 and display this!
%             for identifier = 1:2
%                 if O.Interface.configuration.pump(identifier,1) == 1
%                    O.Interface.sensor.pump(identifier).value = 0;
%                    O.Interface.sensor.pump(identifier).changeSetting;
%                 end
%             end
%             
%             disp('The Pumps are set to 0 rpm');
%         
%             %Stop pressureTimer
%             for identifier = 1:3
%                 if O.Interface.configuration.pressure(identifier,1)
%                     stop(O.Interface.sensor.pressure(identifier).pressureTimer);
%                     delete(O.Interface.sensor.pressure(identifier).pressureTimer);
%                 end
%             end
%             
%             %stop pcvTimer
%             if O.Interface.GUI.startControlButton.Value == true
%                 for identifier = 1:2
%                     if O.Interface.configuration.pcv(identifier,1)
%                         stop(O.Interface.sensor.pcv(identifier).pcvTimer); %pressure tester stopped
%                         delete(O.Interface.sensor.pcv(identifier).pcvTimer);
%                     end
%                 end
%             end
%             
%             if O.Interface.GUI.startButton.Value == true
%                 stop(O.Interface.timerLog);
%             end
%             
%             delete(O.Interface.timerLog); %measurements stopped
%             
%             delete(O.Interface.GUI.fig);
%             delete(O.arduinoObj);
%             
%             %Saving all the data as a matfile so you can read from it very easily with the same names as here 
%             %--> load('filename.mat') brings all the things into the workspace
%             save(O.Interface.export.filename);
            elseif average > O.warningValue
                warning(['The pressure sensor ', num2str(O.name), 'is near your critical value of ', num2str(O.criticalValue), ' bar. Take the according measures']);
            end
            
        end % end controlCriticalValue
    end
end

