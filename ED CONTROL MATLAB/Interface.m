classdef Interface < handle %ED General Code
    
    properties
        
        GUI %General User Interface
        
        arduinoObj
        
        configuration %matrices to decide which sensors are connected etc
        
        names %to display all the sensors with their names
        
        sensor % to store the values and read them 
        
        timerLog %timer and functions
        
        export %things that will be exported for the measurements
        
        normalSetup %to change the valves accordingly
        
        reversalSetup %to change the valves accordingly
        
        reversalTimer 
        
        reversal = 0; %in the beginning no reversal is doing
        
        firstReversal = 0;
        
        pressureDifferenceDCTimer;
        
        pressureDifferenceRDTimer;
        
        concentrateTankControl;
        
        concState = 0;
        
        controlSystem;
        
        controlState = 0;
        
        startOpeningValve = 0;
        
        startupTimer;
        
        startState;
        
    end
    
    %IDEA TO SHOW THE TIME: datetime(now,'ConvertFrom','datenum','Format','HH:mm:ss')
    
    
    methods
        
        function O = Interface(arduinoObj, configuration, names, filename)
            
            O.export.filename = filename;
            
            O.names = names;
            
            O.sensor.num = 0;
            
            O.configuration = configuration;
            
            O.arduinoObj = arduinoObj;
            
            O.startState = 0;
            
            O.timerLog = timer('ExecutionMode', 'fixedSpacing','Period',1, 'BusyMode', 'drop');

            O.timerLog.StartFcn = @(~,~)disp('The measurements have started');

            O.timerLog.StopFcn = @(~,~)disp('The measurements have ended');

            O.timerLog.TimerFcn = @(~,~)plotValues(O);
            
            %-----
            
            O.normalSetup = timer('ExecutionMode', 'fixedSpacing', 'TasksToExecute', 1);

            O.normalSetup.StartFcn = @(~,~)disp('Normal Setup started');

            O.normalSetup.StopFcn = @(~,~)disp('Normal Setup is finished');

            O.normalSetup.TimerFcn = @(~,~)normalSetup(O);
            
            %-----
            O.reversalSetup = timer('ExecutionMode', 'fixedSpacing', 'TasksToExecute', 1);

            O.reversalSetup.StartFcn = @(~,~)disp('Reversal Setup started');

            O.reversalSetup.StopFcn = @(~,~)disp('Reversal Setup is finished');

            O.reversalSetup.TimerFcn = @(~,~)reversalSetup(O);
            
            %------
            O.reversalTimer = timer('ExecutionMode', 'fixedSpacing', 'Period',1);

            O.reversalTimer.StartFcn = @(~,~)disp('Reversal Operation started');

            O.reversalTimer.StopFcn = @(~,~)disp('Reversal Operation finished');

            O.reversalTimer.TimerFcn = @(~,~)reversalOperation(O);
            
            %----
            O.pressureDifferenceDCTimer = timer('ExecutionMode', 'fixedSpacing','Period',5);

            O.pressureDifferenceDCTimer.StartFcn = @(~,~)disp('Pressure Difference DC tester started');

            O.pressureDifferenceDCTimer.StopFcn = @(~,~)disp('Pressure Difference DC tester is finished');

            O.pressureDifferenceDCTimer.TimerFcn = @(~,~)measurecriticalPDDC(O);
            
            %----
            O.pressureDifferenceRDTimer = timer('ExecutionMode', 'fixedSpacing','Period',1);

            O.pressureDifferenceRDTimer.StartFcn = @(~,~)disp('Pressure Difference RD tester started');

            O.pressureDifferenceRDTimer.StopFcn = @(~,~)disp('Pressure Difference RD tester is finished');

            O.pressureDifferenceRDTimer.TimerFcn = @(~,~)measurecriticalPDRD(O);
            
            %-----
            
            O.concentrateTankControl = timer('ExecutionMode', 'fixedSpacing','Period',2);

            O.concentrateTankControl.StartFcn = @(~,~)disp('Concentrate Tank Controller started');

            O.concentrateTankControl.StopFcn = @(~,~)disp('Concentrate Tank Controller is finished');

            O.concentrateTankControl.TimerFcn = @(~,~)concTankController(O);
            
            %----
            
            O.controlSystem = timer('ExecutionMode', 'fixedSpacing','Period',1);

            O.controlSystem.StartFcn = @(~,~)disp('General Controller of ED started');

            O.controlSystem.StopFcn = @(~,~)disp('General Controller of ED is finished');

            O.controlSystem.TimerFcn = @(~,~)controlSystemED(O);
            
            %----
            
            O.startupTimer = timer('ExecutionMode', 'fixedSpacing','Period',1);

            O.startupTimer.StartFcn = @(~,~)disp('Startup of ED started');

            O.startupTimer.StopFcn = @(~,~)disp('Startup of ED is finished');

            O.startupTimer.TimerFcn = @(~,~)startupED(O);
            
            O.GUI.fig = uifigure();
            O.GUI.fig.Position = [100, 80, 1200, 900];
            O.GUI.fig.Scrollable = 'on';
            
            % Callback functions
            O.GUI.fig.CloseRequestFcn = @(src,event)closeFig(O);
            
            O.GUI.overallGrid = uigridlayout(O.GUI.fig);
            
            O.GUI.overallGrid.RowHeight = {'fit', 'fit', 'fit', 'fit', 'fit', 'fit', 'fit'};
            O.GUI.overallGrid.ColumnWidth = {'fit', 'fit', 'fit', 'fit', 'fit', 'fit', 'fit'};
            O.GUI.overallGrid.Scrollable = 'on';

            % ---------- Setup of Pump Graphs
            O.GUI.pumpPanel = uipanel(O.GUI.overallGrid);
            O.GUI.pumpPanel.Layout.Row = [1 2];
            O.GUI.pumpPanel.Layout.Column = [1 2];
            
            O.GUI.pumpGrid = uigridlayout(O.GUI.pumpPanel);
            O.GUI.pumpGrid.RowHeight = {'fit', 'fit'};
            O.GUI.pumpGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of Fields for the Massflow Setting for the Pump
            
            O.GUI.pumpSetPanel = uipanel(O.GUI.overallGrid);
            O.GUI.pumpSetPanel.Layout.Row = 3;
            O.GUI.pumpSetPanel.Layout.Column = 2;
            
            O.GUI.pumpSetGrid = uigridlayout(O.GUI.pumpSetPanel);
            O.GUI.pumpSetGrid.RowHeight = {'fit'};
            O.GUI.pumpSetGrid.ColumnWidth = {'fit'};
            
            % ---------- Setup of Polarity
            
            O.GUI.polarityPanel = uipanel(O.GUI.overallGrid);
            O.GUI.polarityPanel.Layout.Row = 2;
            O.GUI.polarityPanel.Layout.Column = 5;
            
            O.GUI.polarityGrid = uigridlayout(O.GUI.polarityPanel);
            O.GUI.polarityGrid.RowHeight = {'fit'};
            O.GUI.polarityGrid.ColumnWidth = {'fit'};
            
            % ---------- Setup of Button Panel
            O.GUI.buttonPanel = uipanel(O.GUI.overallGrid);
            O.GUI.buttonPanel.Layout.Row = 3;
            O.GUI.buttonPanel.Layout.Column = 1;
            
            O.GUI.buttonGrid = uigridlayout(O.GUI.buttonPanel);
            O.GUI.buttonGrid.RowHeight = {'fit', 'fit'};
            O.GUI.buttonGrid.ColumnWidth = {'fit', 'fit'};
            
            O.GUI.closeButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.closeButton.Text = 'Stop System';
            O.GUI.closeButton.Layout.Row = 5;
            O.GUI.closeButton.Layout.Column = 1;
            O.GUI.closeButton.Value = false;
            
            O.GUI.closeButton.ValueChangedFcn = @(src,event)stopSystem(O, event.Value);
            
            O.GUI.startButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.startButton.Text = 'Start Measurements';
            O.GUI.startButton.Layout.Row = 1;
            O.GUI.startButton.Layout.Column = 1;
            O.GUI.startButton.Value = false;
            
            O.GUI.startButton.ValueChangedFcn = @(src,event)startMeasuring(O, event);

            O.GUI.startControlButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.startControlButton.Text = 'Normal Feed Operation';
            O.GUI.startControlButton.Layout.Row = 2;
            O.GUI.startControlButton.Layout.Column = 1;
            O.GUI.startControlButton.Value = false;
            
            O.GUI.startControlButton.ValueChangedFcn = @(src,event)startNormalFeed(O, event);
            
            O.GUI.startReversalButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.startReversalButton.Text = 'ED Reversal Operation';
            O.GUI.startReversalButton.Layout.Row = 3;
            O.GUI.startReversalButton.Layout.Column = 1;
            O.GUI.startReversalButton.Value = false;
            
            O.GUI.startReversalButton.ValueChangedFcn = @(src,event)startReversal(O, event);
            
            O.GUI.startED = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.startED.Text = 'ED System';
            O.GUI.startED.Layout.Row = 4;
            O.GUI.startED.Layout.Column = 1;
            O.GUI.startED.Value = false;
            
            O.GUI.startED.ValueChangedFcn = @(src,event)startED(O, event);
            
            % ---------- Setup of Fields for the Current of the ED
            
            O.GUI.EDCurrentPanel = uipanel(O.GUI.overallGrid);
            O.GUI.EDCurrentPanel.Layout.Row = 1;
            O.GUI.EDCurrentPanel.Layout.Column = 5;
            
            O.GUI.EDCurrentGrid = uigridlayout(O.GUI.EDCurrentPanel);
            O.GUI.EDCurrentGrid.RowHeight = {'fit'};
            O.GUI.EDCurrentGrid.ColumnWidth = {'fit'};
            
            % ---------- Setup of Flow Graphs
            O.GUI.flowPanel = uipanel(O.GUI.overallGrid);
            O.GUI.flowPanel.Layout.Row = [1 2];
            O.GUI.flowPanel.Layout.Column = [3 4];
            
            O.GUI.flowGrid = uigridlayout(O.GUI.flowPanel);
            O.GUI.flowGrid.RowHeight = {'fit', 'fit'};
            O.GUI.flowGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of C-Valve Graphs
            O.GUI.cvPanel = uipanel(O.GUI.overallGrid);
            O.GUI.cvPanel.Layout.Row = 6;
            O.GUI.cvPanel.Layout.Column = [1 4];
            
            O.GUI.cvGrid = uigridlayout(O.GUI.cvPanel);
            O.GUI.cvGrid.RowHeight = {'fit', 'fit'};
            O.GUI.cvGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of OC-Valve Graphs (normally open)
            O.GUI.ocvNOPanel = uipanel(O.GUI.overallGrid);
            O.GUI.ocvNOPanel.Layout.Row = 7;
            O.GUI.ocvNOPanel.Layout.Column = [1 3];
            
            O.GUI.ocvNOGrid = uigridlayout(O.GUI.ocvNOPanel);
            O.GUI.ocvNOGrid.RowHeight = {'fit', 'fit'};
            O.GUI.ocvNOGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of Pressure Graphs
            O.GUI.pressurePanel = uipanel(O.GUI.overallGrid);
            O.GUI.pressurePanel.Layout.Row = [4 5];
            O.GUI.pressurePanel.Layout.Column = [1 3];
            
            O.GUI.pressureGrid = uigridlayout(O.GUI.pressurePanel);
            O.GUI.pressureGrid.RowHeight = {'fit', 'fit'};
            O.GUI.pressureGrid.ColumnWidth = {'fit', 'fit'};

            % ---------- Setup of Conductivity Graphs
            O.GUI.conductivityPanel = uipanel(O.GUI.overallGrid);
            O.GUI.conductivityPanel.Layout.Row = 3;
            O.GUI.conductivityPanel.Layout.Column = [3 5];
            
            O.GUI.conductivityGrid = uigridlayout(O.GUI.conductivityPanel);
            O.GUI.conductivityGrid.RowHeight = {'fit', 'fit'};
            O.GUI.conductivityGrid.ColumnWidth = {'fit', 'fit'};          
                                    
            createGraphs(O);
            
        end % constructor
        
        %% Create graphs and sensor objects
        
        function createGraphs(O)

            % Flow sensors
            for identifier = 1:4
                if O.configuration.mf(identifier,1)
                    flowGraphSetup(O,identifier);
                    O.sensor.mf(identifier) = massFlowSensor(O.arduinoObj, O.configuration.mf(identifier, 2), identifier, O.names.mf(identifier));
                else
                    O.sensor.mf(identifier) = massFlowSensor(O.arduinoObj, O.configuration.mf(identifier, 2), identifier, O.names.mf(identifier));
                end
            end
            
            EDCurrentSetup(O);
        
            %Pressure Sensors
            for identifier = 1:6
                if O.configuration.pressure(identifier,1)
                    pressureGraphSetup(O,identifier);
                    O.sensor.pressure(identifier) = pressureSensor(O.arduinoObj, O.configuration.pressure(identifier, 2), identifier, O.names.pressure(identifier), O.configuration.pressure(identifier, 3), O.configuration.pressure(identifier, 4), O.GUI.closeButton, O);
                else
                    O.sensor.pressure(identifier) = pressureSensor(O.arduinoObj, O.configuration.pressure(identifier, 2), identifier, O.names.pressure(identifier), O.configuration.pressure(identifier, 3), O.configuration.pressure(identifier, 4), O.GUI.closeButton, O);
                end
            end
            
            %Conductivity Sensors
            for identifier = 1:3
                if O.configuration.conductivity(identifier,1)
                    conductivityGraphSetup(O,identifier);
                    O.sensor.conductivity(identifier) = ConductivitySensor(O.arduinoObj, O.configuration.conductivity(identifier, 2), O.configuration.conductivity(identifier, 3), identifier, O.names.conductivity(identifier));
                else
                    O.sensor.conductivity(identifier) = ConductivitySensor(O.arduinoObj, O.configuration.conductivity(identifier, 2), O.configuration.conductivity(identifier, 3), identifier, O.names.conductivity(identifier));
                end
            end
            
            count = 0;
            %Pumps
            for identifier = 1:4
                if O.configuration.pump(identifier,1)
                    if count == 0
                        O.sensor.pumpIdentifier = identifier;
                    end
                    pumpGraphSetup(O,identifier);
                    pumpSetSetup(O,identifier);
                    count = 1;
                    O.sensor.pump(identifier) = Pump(O.arduinoObj, O.configuration.pump(identifier,2), identifier, O.names.pump(identifier), O.configuration.pump(identifier,3), O.configuration.pump(identifier,4), O.configuration.pump(identifier,5), O.sensor.mf(O.configuration.pump(identifier,6)), O.sensor.pressure, O);
                else
                    O.sensor.pump(identifier) = Pump(O.arduinoObj, O.configuration.pump(identifier,2), identifier, O.names.pump(identifier), O.configuration.pump(identifier,3), 0, 0, 0, 0, 0 );
                end
            end
            
            %ocvNC 
            for identifier = 1:length(O.configuration.ocvNC)
                if O.configuration.ocvNC(identifier,1)
                    O.sensor.ocvNC(identifier) = ocvNC(O.arduinoObj, identifier, O.names.ocvNC(1));
                    ocvNOGraphSetup(O,identifier);
                end
            end
            
            %cv
            for identifier = 1:length(O.configuration.cv)
                if O.configuration.cv(identifier,1)
                    O.sensor.cv(identifier) = cv(O.arduinoObj, identifier, O.names.cv(1));
                    cvGraphSetup(O,identifier);
                end
            end
            
            %Polarity Setup
            O.sensor.polarity = Polarity(O.arduinoObj, "Polarity", 0); %1 is positive, -1 is negative, 0 is off
            polarityGraphSetup(O);
            
            
            %Pressure Difference Setup
            if O.configuration.pressuredifferenceDC(1,1)
                O.sensor.pressuredifferenceDC = struct('data', 0, 'time', 0);
            end
            
            if O.configuration.pressuredifferenceRD(1,1)
                O.sensor.pressuredifferenceRD = struct('data', 0, 'time', 0);
%                 transmembranePressureGraphSetup(O,1);
            end
            
            %Level Switches
            for identifier = 1:7
                if O.configuration.ls(identifier,1)
                    O.sensor.ls(identifier) = ls(O.arduinoObj, identifier, O.names.ls(identifier,1));
                end
            end
            
        end %createGraphs
        
        %%
        function EDCurrentSetup(O)    
            
            name = "Current drawing from the ED [A]";
            
            O.GUI.EDCurrent.connection = uigridlayout(O.GUI.EDCurrentGrid);
            O.GUI.EDCurrent.connection.RowHeight = {20, 'fit'};
            O.GUI.EDCurrent.connection.ColumnWidth = {'fit'};
            O.GUI.EDCurrent.connection.Layout.Row = 1;
            O.GUI.EDCurrent.connection.Layout.Column = 1;
            
            O.GUI.EDCurrent.label = uilabel(O.GUI.EDCurrent.connection);
            O.GUI.EDCurrent.label.Text = name;
            O.GUI.EDCurrent.label.FontSize = 14;
            O.GUI.EDCurrent.label.FontWeight = 'bold';
            O.GUI.EDCurrent.label.HorizontalAlignment = 'center';
            O.GUI.EDCurrent.label.Layout.Row = 1;
            O.GUI.EDCurrent.label.Layout.Column = 1;
            
            O.GUI.EDCurrent.field = uieditfield(O.GUI.EDCurrent.connection,'numeric');
            O.GUI.EDCurrent.field.Value = 0;
            O.sensor.EDCurrent = 0;
            O.sensor.EDCurrenttime = 0;
            
            %Callback functions
            O.GUI.EDCurrent.field.ValueChangedFcn = @(~,event)setEDCurrentChanged(O, event);
            
        end
        
        function pumpSetSetup(O, identifier)    
                       
            O.GUI.pumpSet(identifier).connection = uigridlayout(O.GUI.pumpSetGrid);
            O.GUI.pumpSet(identifier).connection.RowHeight = {'fit'};
            O.GUI.pumpSet(identifier).connection.ColumnWidth = {'fit'};
            O.GUI.pumpSet(identifier).connection.Layout.Row = identifier;
            O.GUI.pumpSet(identifier).connection.Layout.Column = 1;
            
            O.GUI.pumpSet(identifier).label = uilabel(O.GUI.pumpSet(identifier).connection);
            O.GUI.pumpSet(identifier).label.Text = ["Set mass flow for", O.names.pump(identifier)];
            O.GUI.pumpSet(identifier).label.FontSize = 14;
            O.GUI.pumpSet(identifier).label.FontWeight = 'bold';
            O.GUI.pumpSet(identifier).label.HorizontalAlignment = 'center';
            O.GUI.pumpSet(identifier).label.Layout.Row = 1;
            O.GUI.pumpSet(identifier).label.Layout.Column = 1;
            
            O.GUI.pumpSet(identifier).field = uieditfield(O.GUI.pumpSet(identifier).connection,'numeric');
            O.GUI.pumpSet(identifier).field.Value = O.configuration.pump(identifier,3);
            
            %Callback functions
            O.GUI.pumpSet(identifier).field.ValueChangedFcn = @(~,event)setPumpFieldChanged(O, event, identifier);
            
        end
        
        function pumpGraphSetup(O,identifier)
            
            rowIdentifier = [1, 1, 2, 2];
            columnIdentifier = [1, 2, 1, 2];
            
            O.GUI.pump(identifier).ax = uiaxes(O.GUI.pumpGrid,...
                                        'YLim',[0 5],...
                                        'XLim', [-inf inf]);
            O.GUI.pump(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.pump(identifier).ax.Layout.Column = columnIdentifier(identifier);
            O.GUI.pump(identifier).ax.Title.String = O.names.pump(identifier,1);
            O.GUI.pump(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.pump(identifier).ax.YLabel.String = 'Voltage input [V]';
            O.GUI.pump(identifier).ax.Box = 'on';
            O.GUI.pump(identifier).ax.XMinorGrid = 'on';
            O.GUI.pump(identifier).ax.YMinorGrid = 'on';
            set(O.GUI.pump(identifier).ax,'NextPlot','replacechildren')
            
        end
        
        function flowGraphSetup(O,identifier)
            
            rowIdentifier = [1, 1, 2, 2];
            columnIdentifier = [1, 2, 1, 2];
            
            O.GUI.mf(identifier).ax = uiaxes(O.GUI.flowGrid,...
                'YLim',[0 O.configuration.mf(identifier,2)],...
                'XLim', [-inf inf]);
            O.GUI.mf(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.mf(identifier).ax.Layout.Column = columnIdentifier(identifier); 
            O.GUI.mf(identifier).ax.Title.String = O.names.mf(identifier,1);
            O.GUI.mf(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.mf(identifier).ax.YLabel.String = 'flow [l/min]';
            O.GUI.mf(identifier).ax.Box = 'on';
            O.GUI.mf(identifier).ax.XMinorGrid = 'on';
            O.GUI.mf(identifier).ax.YMinorGrid = 'on';

        end
        
        function pressureGraphSetup(O,identifier)
            
            rowIdentifier = [2, 1, 1, 1, 2, 2];
            columnIdentifier = [3, 1, 2, 3, 1, 2];
            
            O.GUI.pressure(identifier).ax = uiaxes(O.GUI.pressureGrid,...
                'YLim',[0 6],...
                'XLim', [-inf inf]);
            O.GUI.pressure(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.pressure(identifier).ax.Layout.Column = columnIdentifier(identifier);
            O.GUI.pressure(identifier).ax.Title.String = O.names.pressure(identifier,1);
            O.GUI.pressure(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.pressure(identifier).ax.YLabel.String = 'pressure [bar]';
            O.GUI.pressure(identifier).ax.Box = 'on';
            O.GUI.pressure(identifier).ax.XMinorGrid = 'on';
            O.GUI.pressure(identifier).ax.YMinorGrid = 'on';
            set(O.GUI.pressure(identifier).ax,'NextPlot','replacechildren')
            
        end %end pressureGraphSetup
       

        function conductivityGraphSetup(O,identifier)
            
            rowIdentifier = [1, 1, 1];
            columnIdentifier = [1, 2, 3];
            
            O.GUI.conductivity(identifier).ax = uiaxes(O.GUI.conductivityGrid,...
                'YLim',[0 6],...
                'XLim', [-inf inf]);
            O.GUI.conductivity(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.conductivity(identifier).ax.Layout.Column = columnIdentifier(identifier);
            O.GUI.conductivity(identifier).ax.Title.String = O.names.conductivity(identifier,1);
            O.GUI.conductivity(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.conductivity(identifier).ax.YLabel.String = 'conductivity [mS]';
            O.GUI.conductivity(identifier).ax.Box = 'on';
            O.GUI.conductivity(identifier).ax.XMinorGrid = 'on';
            O.GUI.conductivity(identifier).ax.YMinorGrid = 'on';
            set(O.GUI.conductivity(identifier).ax,'NextPlot','replacechildren')
            
        end  % end conductivityGraphSetup

        function temperatureGraphSetup(O,identifier)
            
            rowIdentifier = [1, 1, 2, 2];
            columnIdentifier = [1, 2, 1, 2];
            
            O.GUI.temperature(identifier).ax = uiaxes(O.GUI.temperatureGrid,...
                'YLim',[0 6],...
                'XLim', [-inf inf]);
            O.GUI.temperature(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.temperature(identifier).ax.Layout.Column = columnIdentifier(identifier);
            O.GUI.temperature(identifier).ax.Title.String = O.names.temperature(identifier,1);
            O.GUI.temperature(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.temperature(identifier).ax.YLabel.String = 'temperature [˚C]';
            O.GUI.temperature(identifier).ax.Box = 'on';
            O.GUI.temperature(identifier).ax.XMinorGrid = 'on';
            O.GUI.temperature(identifier).ax.YMinorGrid = 'on';
            set(O.GUI.temperature(identifier).ax,'NextPlot','replacechildren')
            
        end  % end conductivityGraphSetup
        
        function ocvNOGraphSetup(O,identifier)
            
            rowIdentifier = [1, 1, 1];
            columnIdentifier = [1 2 3];
            
            O.GUI.ocvNC(identifier).ax = uiaxes(O.GUI.ocvNOGrid,...
                                        'YLim',[0 5],...
                                        'XLim', [-inf inf]);
            O.GUI.ocvNC(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.ocvNC(identifier).ax.Layout.Column = columnIdentifier(identifier);
            O.GUI.ocvNC(identifier).ax.Title.String = O.names.ocvNC(identifier,1);
            O.GUI.ocvNC(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.ocvNC(identifier).ax.YLabel.String = 'Voltage input [V]';
            O.GUI.ocvNC(identifier).ax.Box = 'on';
            O.GUI.ocvNC(identifier).ax.XMinorGrid = 'on';
            O.GUI.ocvNC(identifier).ax.YMinorGrid = 'on';
            set(O.GUI.ocvNC(identifier).ax,'NextPlot','replacechildren')
        end
        
        function cvGraphSetup(O,identifier) 
            
            rowIdentifier = [1 1 1 1 1];
            columnIdentifier = [1 2 3 4 5];
            
            O.GUI.cv(identifier).ax = uiaxes(O.GUI.cvGrid,...
                                        'YLim',[0 5],...
                                        'XLim', [-inf inf]);
            O.GUI.cv(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.cv(identifier).ax.Layout.Column = columnIdentifier(identifier);
            O.GUI.cv(identifier).ax.Title.String = O.names.cv(identifier,1);
            O.GUI.cv(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.cv(identifier).ax.YLabel.String = 'Voltage input [V]';
            O.GUI.cv(identifier).ax.Box = 'on';
            O.GUI.cv(identifier).ax.XMinorGrid = 'on';
            O.GUI.cv(identifier).ax.YMinorGrid = 'on';
            set(O.GUI.cv(identifier).ax,'NextPlot','replacechildren')
            
        end
        
        function polarityGraphSetup(O)
            
            O.GUI.polarity.ax = uiaxes(O.GUI.polarityGrid,...
                                        'YLim',[0 5],...
                                        'XLim', [-inf inf]);
            O.GUI.polarity.ax.Layout.Row = 1;
            O.GUI.polarity.ax.Layout.Column = 1;
            O.GUI.polarity.ax.Title.String = 'Polarity';
            O.GUI.polarity.ax.XLabel.String = 'time [s]';
            O.GUI.polarity.ax.YLabel.String = 'Polarity Low (0) or High (1)';
            O.GUI.polarity.ax.Box = 'on';
            O.GUI.polarity.ax.XMinorGrid = 'on';
            O.GUI.polarity.ax.YMinorGrid = 'on';
            set(O.GUI.polarity.ax,'NextPlot','replacechildren')
            
        end
     
        %% PLOTTING
        
        function plotValues(O)
            
            O.arduinoObj.flushing;

            %Plot pressure sensors
            for identifier = 1:6
                if O.configuration.pressure(identifier,1)
                    O.sensor.pressure(identifier).num = O.sensor.pressure(identifier).num + 1;
                    O.sensor.num = O.sensor.num + 1;
                    if O.sensor.num == 1
                        O.sensor.pressure(identifier).time(end+1) = now;
                        O.sensor.beginTimeIdentifier = identifier;
                        
                        for i = 1:4
                            O.sensor.pump(i).beginTimeIdentifier = identifier;
                        end
                        
                        break
                    end
                    
                    if O.sensor.pressure(identifier).num == 3
                        start(O.sensor.pressure(identifier).pressureTimer);
                        if identifier == O.sensor.beginTimeIdentifier
                            start(O.pressureDifferenceDCTimer)
                            start(O.pressureDifferenceRDTimer)
                        end
                    end
                    
                    O.sensor.pressure(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    % exclude NaN
                    pressureValue = O.sensor.pressure(identifier).value;
                    count = 0;
                    while isnan(pressureValue)
                        pressureValue = O.sensor.pressure(identifier).value;
                        count = count + 1;
                        if count == 10
                            warning('Something is wrong with the Arduino - it always gives NaN - check the system');
                        end
                    end
                    O.sensor.pressure(identifier).data(end+1) = pressureValue;
                    elapsedTime = linspace(0, O.sensor.pressure(identifier).time(end), length(O.sensor.pressure(identifier).data));
                    
                    if length(O.sensor.pressure(identifier).time) > 15
                        O.GUI.pressure(identifier).ax.XLim = [O.sensor.pressure(identifier).time(end-13) O.sensor.pressure(identifier).time(end)];
                        O.GUI.pressure(identifier).ax.YLim = [min(O.sensor.pressure(identifier).data((end-13):end))-0.3 max(O.sensor.pressure(identifier).data((end-14):end))+0.3];
                    else 
                        O.GUI.pressure(identifier).ax.YLim = [min(O.sensor.pressure(identifier).data)-0.3 max(O.sensor.pressure(identifier).data)+0.3];
                    end
                    
                    O.GUI.pressure(identifier).ax.Title.String = [O.names.pressure(identifier,1); 'current value: ', num2str(O.sensor.pressure(identifier).data(end)), ' bar'];
                    plot(O.GUI.pressure(identifier).ax, elapsedTime, O.sensor.pressure(identifier).data);
                end
            end
            
            O.arduinoObj.flushing;
            
            %Plot massflow sensors
            for identifier = 1:4
                if O.configuration.mf(identifier,1)
                    O.sensor.mf(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    % exclude NaN
                    mfValue = O.sensor.mf(identifier).value;
                    count = 0;
                    while isnan(mfValue)
                        mfValue = O.sensor.mf(identifier).value;
                        count = count + 1;
                        if count == 10
                            warning('Something is wrong with the Arduino - it always gives NaN - check the system');
                        end
                    end
                    O.sensor.mf(identifier).data(end+1) = mfValue;
                    elapsedTime = linspace(0, O.sensor.mf(identifier).time(end), length(O.sensor.mf(identifier).data));
                    if length(O.sensor.mf(identifier).time) > 15
                        O.GUI.mf(identifier).ax.XLim = [O.sensor.mf(identifier).time(end-13) O.sensor.mf(identifier).time(end)];
                        O.GUI.mf(identifier).ax.YLim = [min(O.sensor.mf(identifier).data((end-13):end))-0.3 max(O.sensor.mf(identifier).data((end-13):end))+0.3];
                    else 
                        O.GUI.mf(identifier).ax.YLim = [min(O.sensor.mf(identifier).data)-0.3 max(O.sensor.mf(identifier).data)+0.3];
                    end
                    O.GUI.mf(identifier).ax.Title.String = [O.names.mf(identifier,1); 'current value: ', num2str(O.sensor.mf(identifier).data(end)), ' l/min'];
                    plot(O.GUI.mf(identifier).ax, elapsedTime, O.sensor.mf(identifier).data);
                end
            end
            
            if O.GUI.closeButton.Value == true
                stopSystem(O,true);
            end
            


            %Plot conductivity sensors
            for identifier = 1:3
                if O.configuration.conductivity(identifier,1)
                    O.sensor.conductivity(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    O.sensor.conductivity(identifier).data(end+1) = O.sensor.conductivity(identifier).value;
                    elapsedTime = linspace(0, O.sensor.conductivity(identifier).time(end), length(O.sensor.conductivity(identifier).data));
                    
                    if length(O.sensor.conductivity(identifier).time) > 15
                        O.GUI.conductivity(identifier).ax.XLim = [O.sensor.conductivity(identifier).time(end-13) O.sensor.conductivity(identifier).time(end)];
                        O.GUI.conductivity(identifier).ax.YLim = [min(O.sensor.conductivity(identifier).data((end-13):end))-0.3 max(O.sensor.conductivity(identifier).data((end-13):end))+0.3];
                    else 
                        O.GUI.conductivity(identifier).ax.YLim = [min(O.sensor.conductivity(identifier).data)-0.3 max(O.sensor.conductivity(identifier).data)+0.3];
                    end
                    
                    O.GUI.conductivity(identifier).ax.Title.String = [O.names.conductivity(identifier,1); 'current value: ', num2str(O.sensor.conductivity(identifier).data(end)), ' mS'];
                    plot(O.GUI.conductivity(identifier).ax, elapsedTime, O.sensor.conductivity(identifier).data);
                end
            end
            
            %Plot pump input
            for identifier = 1:4
                if O.configuration.pump(identifier,1)
                    O.sensor.pump(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    O.sensor.pump(identifier).data(end+1) = O.sensor.pump(identifier).setValue(end);
                    elapsedTime = linspace(0, O.sensor.pump(identifier).time(end), length(O.sensor.pump(identifier).data));
                    if length(O.sensor.pump(identifier).time) > 15
                        O.GUI.pump(identifier).ax.XLim = [O.sensor.pump(identifier).time(end-13) O.sensor.pump(identifier).time(end)];
                        O.GUI.pump(identifier).ax.YLim = [min(O.sensor.pump(identifier).data((end-13):end))-0.3 max(O.sensor.pump(identifier).data((end-14):end))+0.3];
                    else 
                        O.GUI.pump(identifier).ax.YLim = [min(O.sensor.pump(identifier).data)-0.3 max(O.sensor.pump(identifier).data)+0.3];
                    end
                    O.GUI.pump(identifier).ax.Title.String = [O.names.pump(identifier,1); 'current value: ', num2str(O.sensor.pump(identifier).data(end)), ' Volt'];
                    plot(O.GUI.pump(identifier).ax, elapsedTime, O.sensor.pump(identifier).data);
                end
            end
            
            %Plot ocvNC
            for identifier = 1: length(O.configuration.ocvNC)
                if O.configuration.ocvNC(identifier,1)
                    O.sensor.ocvNC(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    O.sensor.ocvNC(identifier).data(end+1) = O.sensor.ocvNC(identifier).value;
                    elapsedTime = linspace(0, O.sensor.ocvNC(identifier).time(end), length(O.sensor.ocvNC(identifier).data));
                    if length(O.sensor.ocvNC(identifier).time) > 15
                        O.GUI.ocvNC(identifier).ax.XLim = [O.sensor.ocvNC(identifier).time(end-13) O.sensor.ocvNC(identifier).time(end)];
                        O.GUI.ocvNC(identifier).ax.YLim = [min(O.sensor.ocvNC(identifier).data((end-13):end))-0.3 max(O.sensor.ocvNC(identifier).data((end-14):end))+0.3];
                    else 
                        O.GUI.ocvNC(identifier).ax.YLim = [min(O.sensor.ocvNC(identifier).data)-0.3 max(O.sensor.ocvNC(identifier).data)+0.3];
                    end
                    O.GUI.ocvNC(identifier).ax.Title.String = [O.names.ocvNC(identifier,1); 'current value: ', num2str(O.sensor.ocvNC(identifier).data(end)), ' Volt'];
                    plot(O.GUI.ocvNC(identifier).ax, elapsedTime, O.sensor.ocvNC(identifier).data);
                end
            end
            
            %Plot cv 
           for identifier = 1:length(O.configuration.cv)
               if O.configuration.cv(identifier,1)
                    O.sensor.cv(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    O.sensor.cv(identifier).data(end+1) = O.sensor.cv(identifier).value;
                    elapsedTime = linspace(0, O.sensor.cv(identifier).time(end), length(O.sensor.cv(identifier).data));
                    if length(O.sensor.cv(identifier).time) > 15
                        O.GUI.cv(identifier).ax.XLim = [O.sensor.cv(identifier).time(end-13) O.sensor.cv(identifier).time(end)];
                        O.GUI.cv(identifier).ax.YLim = [min(O.sensor.cv(identifier).data((end-13):end))-0.3 max(O.sensor.cv(identifier).data((end-14):end))+0.3];
                    else 
                        O.GUI.cv(identifier).ax.YLim = [min(O.sensor.cv(identifier).data)-0.3 max(O.sensor.cv(identifier).data)+0.3];
                    end
                    O.GUI.cv(identifier).ax.Title.String = [O.names.cv(identifier,1); 'current value: ', num2str(O.sensor.cv(identifier).data(end)), ' Volt'];
                    plot(O.GUI.cv(identifier).ax, elapsedTime, O.sensor.cv(identifier).data);
               end
           end
           
           
           %Plot polarity
            O.sensor.polarity.time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
            O.sensor.polarity.data(end+1) = O.sensor.polarity.value;
            elapsedTime = linspace(0, O.sensor.polarity.time(end), length(O.sensor.polarity.data));
            if length(O.sensor.polarity.time) > 15
                O.GUI.polarity.ax.XLim = [O.sensor.polarity.time(end-13) O.sensor.polarity.time(end)];
                O.GUI.polarity.ax.YLim = [min(O.sensor.polarity.data((end-13):end))-0.3 max(O.sensor.polarity.data((end-14):end))+0.3];
            else 
                O.GUI.polarity.ax.YLim = [min(O.sensor.polarity.data)-0.3 max(O.sensor.polarity.data)+0.3];
            end
            O.GUI.polarity.ax.Title.String = [O.names.cv(identifier,1); 'current value: ', num2str(O.sensor.polarity.data(end)), ' Volt'];
            plot(O.GUI.polarity.ax, elapsedTime, O.sensor.polarity.data);
            
            %Level switches
            for identifier = 1:7
                if O.configuration.ls(identifier,1)
                    O.sensor.ls(identifier).data(end+1) = O.sensor.ls(identifier).value;
                    O.sensor.ls(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                end
            end
            
        end % end plotValues
        
        function endSystem(O)
            
            disp('-------------')
            disp('Stopping the System')
            
            %stop reversal operation
            if O.GUI.startReversalButton.Value == true
                stop(O.reversalTimer)
                delete(O.reversalTimer)
                %SWITCH POLARITY TO NORMAL
                O.sensor.polarity.value = 1;
                O.sensor.polarity.changeSetting;
            end
            
            %stop normal Operation
            if O.GUI.startControlButton.Value == true
                for identifier = 1:4
                    if O.configuration.pump(identifier,1)
                        stop(O.sensor.pump(identifier).pumpTimer);
                        delete(O.sensor.pump(identifier).pumpTimer);
                    end
                end
            end
            
            pause(0.5)
            
            start(O.normalSetup)
            
            pause(0.5)
            
            % SET THE PUMPS TO 0 and display this!
            for identifier = 1:4
                if O.configuration.pump(identifier,1) == 1
                   O.sensor.pump(identifier).value = 0;
                   O.sensor.pump(identifier).changeSetting;
                   pause(0.5)
                end
            end
            
            disp('The Pumps are set to 0 rpm');

            %Stop pressureTimer
            for identifier = 1:6
                if O.configuration.pressure(identifier,1)
                    stop(O.sensor.pressure(identifier).pressureTimer);
                    delete(O.sensor.pressure(identifier).pressureTimer);
                end
            end

            %Stop plotting
            if O.GUI.startButton.Value == true
                stop(O.timerLog);
            end
            
            if O.GUI.startED.Value
                stop(O.controlSystem)
                stop(O.concentrateTankControl)
            end
            
            delete(O.controlSystem)
            delete(O.concentrateTankControl)

            delete(O.timerLog);

            delete(O.GUI.fig);
            delete(O.arduinoObj);
%             delete(O.arduino2);
            disp('Disconnected from Arduino');
            
            stop(timerfind);
            delete(timerfind);

            %Saving all the data as a matfile so you can read from it very easily with the same names as here 
            %--> load('filename.mat') brings all the things into the workspace
            save(O.export.filename);
            
        end % end endSystem
        
    end %end methods
end

%% Callback functions definition

function startMeasuring(O, event)
    
    if event.Value
        O.GUI.startButton.Value = event.Value;
        start(O.timerLog);
    else
        O.GUI.startButton.Value = event.Value;
        stop(O.timerLog);
    end
    
end

function startED(O, event)

    if event.Value
        O.GUI.startED.Value = event.Value;
        start(O.startupTimer)
    else
        O.GUI.startED.Value = event.Value;
        %stop polarity
        %stop Pumps
%         stop(O.controlSystem)
%         stop(O.concentrateTankControl);
    end

end

function startNormalFeed(O, event)
    
    if event.Value
        O.GUI.startControlButton.Value = true;
        start(O.normalSetup);
        for identifier = 1:4
            if O.configuration.pump(identifier,1)
                start(O.sensor.pump(identifier).pumpTimer);
            end
        end
        O.sensor.polarity.value = 1;
        O.sensor.polarity.changeSetting;
    else
        O.GUI.startControlButton.Value = false;
        for identifier = 1:4
            if O.configuration.pump(identifier,1)
                stop(O.sensor.pump(identifier).pumpTimer);
                pause(0.3)
                O.sensor.pump(identifier).value = 0;
                O.sensor.pump(identifier).setValue(end) = O.sensor.pump(identifier).value;
                O.sensor.pump(identifier).changeSetting;
            end
        end
    end    
end

function startReversal(O, event)
    
    if event.Value
        O.GUI.startReversalButton.Value = true;
        start(O.reversalTimer);       
    else
        O.GUI.startReversalButton.Value = false;
        stop(O.reversalTimer);
        for identifier = 1:4
            if O.configuration.pump(identifier,1)
                stop(O.sensor.pump(identifier).pumpTimer);
                pause(0.3)
                O.sensor.pump(identifier).value = 0;
                O.sensor.pump(identifier).setValue(end) = O.sensor.pump(identifier).value;
                O.sensor.pump(identifier).changeSetting;
            end
        end
        start(O.normalSetup);
    end    
end

%function reversalOperation(O)
%
%   if O.firstReversal == 0
%       O.firstReversal = 1;
%       O.sensor.pump(O.sensor.pumpIdentifier).controlTime(end+1) = (now - O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*24*3600;
%       O.sensor.pump(O.sensor.pumpIdentifier).stopIdentifier = length(O.sensor.pump(O.sensor.pumpIdentifier).controlTime);
%   end
%
%   if (O.sensor.pump(O.sensor.pumpIdentifier).controlTime(end)-O.sensor.pump(O.sensor.pumpIdentifier).controlTime(O.sensor.pump(O.sensor.pumpIdentifier).stopIdentifier)) > O.configuration.switchTime(1,1) && O.reversal == 0 %DO REVERSAL
%       %Reversal
%       stopPumps(O);
%       start(O.reversalSetup)
%       %DO THE POLARITY SWITCH
%       O.sensor.polarity.value = -1;
%       O.sensor.polarity.changeSetting;
%       plotValues(O);
%
%       O.sensor.pump(O.sensor.pumpIdentifier).stopIdentifier = length(O.sensor.pump(O.sensor.pumpIdentifier).controlTime);
%       pause(0.2)
%       for identifier = 1:4
%            if O.configuration.pump(identifier,1)
%                O.sensor.pump(identifier).mfObj = O.sensor.mf(O.configuration.pump(identifier,7));
%                start(O.sensor.pump(identifier).pumpTimer);
%            end
%       end
%       O.reversal = 1;
%   elseif (O.sensor.pump(O.sensor.pumpIdentifier).controlTime(end)-O.sensor.pump(O.sensor.pumpIdentifier).controlTime(O.sensor.pump(O.sensor.pumpIdentifier).stopIdentifier)) > O.configuration.switchTime(2,1) && O.reversal == 1%DO NORMAL
%       %Normal Operation
%       stopPumps(O);
%       start(O.normalSetup);
%       %DO THE POLARITY SWITCH
%       O.sensor.polarity.value = 1;
%       O.sensor.polarity.changeSetting;
%       plotValues(O);
%
%       O.sensor.pump(O.sensor.pumpIdentifier).stopIdentifier = length(O.sensor.pump(O.sensor.pumpIdentifier).controlTime);
%       pause(0.2)
%       for identifier = 1:4
%            if O.configuration.pump(identifier,1)
%                O.sensor.pump(identifier).mfObj = O.sensor.mf(O.configuration.pump(identifier,6));
%                start(O.sensor.pump(identifier).pumpTimer);
%            end
%       end
%       O.reversal = 0;
%   end
%
%end

function stopPumps(O)
    for identifier = 1:4
            if O.configuration.pump(identifier,1)
                stop(O.sensor.pump(identifier).pumpTimer);
                pause(1)
                O.sensor.pump(identifier).value = 0;
                O.sensor.pump(identifier).setValue(end) = O.sensor.pump(identifier).value;
                O.sensor.pump(identifier).integral = 0;
                O.sensor.pump(identifier).nonSatV = 0;
                O.sensor.pump(identifier).changeSetting;
                O.sensor.pump(identifier).count = 0;
                pause(1)
            end
    end
end %stop all pumps

function startPump(O,identifier)
    
    if O.configuration.pump(identifier,1)
        start(O.sensor.pump(identifier).pumpTimer);
    else
        disp('No pump is connected');
    end
    
end %end startPump

function stopPump(O,identifier)
    
    if O.configuration.pump(identifier,1)
       stop(O.sensor.pump(identifier).pumpTimer);
       pause(0.5)
       O.sensor.pump(identifier).value = 0;
       O.sensor.pump(identifier).integral = 0;
       O.sensor.pump(identifier).nonSatV = 0;
       O.sensor.pump(identifier).setValue(end) = 0;
       O.sensor.pump(identifier).changeSetting;
       O.sensor.pump(identifier).count = 0;
       pause(0.3)
    end
    
end %end stopPump

function reversalSetup(O)


    O.sensor.cv(1).open; %low
    O.sensor.cv(2).open; %low
    O.sensor.cv(3).close; %high
    O.sensor.cv(4).close; %high
    
end

function normalSetup(O)
    
    O.sensor.cv(1).close; %high
    O.sensor.cv(2).close; %high
    O.sensor.cv(3).open; %low
    O.sensor.cv(4).open; %low
    
end

function measurecriticalPDDC(O)
    
    if O.configuration.pressuredifferenceDC(1,1)
       O.sensor.pressuredifferenceDC.data(end+1) = O.sensor.pressure(O.configuration.pressuredifferenceDC(2,1)).data(end) - O.sensor.pressure(O.configuration.pressuredifferenceDC(3,1)).data(end); % Diluate - Concentrate
       O.sensor.pressuredifferenceDC.time(end+1) = O.sensor.pressure(O.configuration.pressuredifferenceDC(2,1)).time(end);
       if length(O.sensor.pressuredifferenceDC.data) > 3
            average = sum(O.sensor.pressuredifferenceDC.data(end-2:end))/3;
       else
            average = 0;
       end
    else
        return
    end
    
    if abs(average) > O.configuration.pressuredifferenceDC(4,1)
        disp('The pressure difference between Diluate and Concentrate is too big, the flow is being adjusted')
        
        if average > 0
            % Diluate pressure is bigger than Concentrate pressure - lower the flow of the diluate
            O.sensor.pump(4).setFlow.value(end+1) = O.sensor.pump(4).setFlow.value(end) - 1/60; %lower by 1l/h = 1/60 l/min
            O.sensor.pump(4).setFlow.t(end+1) = (now - O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
        else
            % Concentrate pressure is bigger than Diluate pressure - lower the flow of the concentrate
            O.sensor.pump(3).setFlow.value(end+1) = O.sensor.pump(3).setFlow.value(end) - 1/60; %lower by 1l/h = 1/60 l/min
            O.sensor.pump(3).setFlow.t(end+1) = (now - O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
        end
    end
    
    if abs(O.sensor.pump(4).setFlow.value(end)) < 0.9*O.configuration.pump(4,3) || abs(O.sensor.pump(3).setFlow.value(end)) < 0.9*O.configuration.pump(3,3)
        disp('The flow in the ED is too low because the pressure difference is too high - the system was therefore shut down')
        O.endSystem;
    end
            
end % end controlCriticalPDDC

function measurecriticalPDRD(O)

    if O.configuration.pressuredifferenceRD(1,1)
        O.sensor.pressuredifferenceRD.data(end+1) = O.sensor.pressure(O.configuration.pressuredifferenceRD(2,1)).data(end) - O.sensor.pressure(O.configuration.pressuredifferenceRD(3,1)).data(end); %Diluate - Rinse
        O.sensor.pressuredifferenceRD.time(end+1) = O.sensor.pressure(O.configuration.pressuredifferenceRD(2,1)).time(end);
        if length(O.sensor.pressuredifferenceRD.data) > 3
            average = sum(O.sensor.pressuredifferenceRD.data(end-2:end))/3;
        else
            average = 0;
        end
    else
        return
    end

    if abs(average) > O.configuration.pressuredifferenceRD(4,1)
        disp('-----------')
        disp('The pressure difference between Diluate and Rinse is too big, the system was shut down - please adjust the hand valve')

        if average > 0
            disp('Please turn the hand valve to the right')
        else
            disp('Please turn the hand valve to the left')
        end

        O.endSystem;
    end
        
            
end % end controlCriticalPDRD

function concTankController(O)

    if O.sensor.conductivity(2).data(end) > 56 && O.concState == 0
        O.sensor.ocvNC(1).open;
        O.concState = 1;
        O.startOpeningValve = now;
    elseif (O.sensor.ls(1).data(end) == 0 && O.concState == 1) || (((now - O.startOpeningValve)*24*3600 > 30) && O.concState == 1) %need to check this time - Dana - 10.5.2022
        O.sensor.ocvNC(1).close;
        O.concState = 0;
    end

end %end concTankController


function startupED(O)
    
    UF = O.arduinoObj.sendCommand('[');
    
    %Check the level switches
    %UF is middle levelswitch
    %ls(5) is post treatment/split tank
    if UF == 1 && O.sensor.ls(5).data(end) == 1  % all the tanks are full - can go directly to controlSystem
        %startState is 0 at the beginning
        O.controlState = 0;
        start(O.controlSystem)
        start(O.concentrateTankControl)
        stop(O.startupTimer)
    
    elseif O.sensor.ls(2).data(end) == 0 % pre tank ED not full, we want to fill it
        O.sensor.ocvNC(1).open;
        O.startState = 1; % in ED tank fill mode
        
    elseif O.sensor.ls(2).data(end) == 1 && O.startState == 1 % pre ED tank full
        O.sensor.ocvNC(1).close; % stop filling ED tank
        O.startState = 2; % ED tank ready, waiting for UF tank
        
    elseif (O.startState == 2 && UF == 1) || (O.startState == 0 && UF ==1) %everything good except ls(5)
        O.controlState = -1; % ED pumps should run but NOT the posttreatment pump
        start(O.controlSystem)
        start(O.concentrateTankControl)
        stop(O.startupTimer)
        
    end

end

function controlSystemED(O)

    if O.controlState == 0 %initialize to start all pumps
        
        start(O.normalSetup)
        
        for i = 2:4 % all but PT pump
            startPump(O,i)
        end
        
        %start the polarity
        O.sensor.polarity.value = 1;
        O.sensor.polarity.changeSetting;
        
        pause(1)
        startPump(O,1) % start pt pump
        
        O.controlState = 1; %all pumps are running in normal operation
        
    elseif O.controlState == -1 %very beginning, the posttreatment pump is turned off
        
        start(O.normalSetup)
        
        for i = 2:4
            startPump(O,i)
        end
        
        %start the polarity
        O.sensor.polarity.value = 1;
        O.sensor.polarity.changeSetting;
        
        O.controlState = 2; % normal operation sans PT pump
        
    elseif O.sensor.ls(5).data(end) == 0 && O.controlState == 1 % check if we should keep PT pump
        stopPump(O,1)
        O.controlState = 2; %Posttreatment Pump is stopped
        
    elseif O.controlState == 2 && O.sensor.ls(5).data(end) == 1 % check if we can start PT pump
        startPump(O,1)
        O.controlState = 1; %all pumps are running in normal operation

    % has enough time passed to do reversal
    elseif (O.sensor.pump(3).controlTime(end)-O.sensor.pump(3).controlTime(O.sensor.pump(3).stopIdentifier)) > O.configuration.switchTime(1,1) %check how long the concentrate pump is running
        
        O.sensor.pump(3).stopIdentifier = length(O.sensor.pump(3).controlTime);
        
        %stop the diluate and concentrate pumps
        for i = 3:4
            stopPump(O,i)
        end
        
        %switch the 3 way valves
        if O.sensor.polarity.value == 1
            start(O.reversalSetup)
        elseif O.sensor.polarity.value == -1
            start(O.normalSetup)
        else
            disp('something is weird with the polarity switch when doing reversal - please check')
        end
        
        %change polarity
        if O.sensor.polarity.value == 1
            O.sensor.polarity.value = -1;
            O.sensor.polarity.changeSetting;
        elseif O.sensor.polarity.value == -1
            O.sensor.polarity.value = 1;
            O.sensor.polarity.changeSetting;
        else
            disp('something is weird with the polarity switch when doing reversal - please check')
        end
        %so we see that the pumps went to zero!
        plotValues(O);
        
        %start the pumps again
        for i = 3:4
            startPump(O,i)
        end
    end

end %controlSystemED

function stopSystem(O,event)

    if O.GUI.closeButton.Value == true || event.Value
        if isempty(timerfind)
            disp('No timers anymore')
            return
        else
            O.endSystem;
        end  
    end

end % end StopSystem

function closeFig(O)
        
    selection = uiconfirm(O.GUI.fig,'Close the figure window?',...
        'Confirmation');

    switch selection
        case 'OK'
            O.endSystem;
        case 'Cancel'
            return
    end
    
end
    
function setEDCurrentChanged(O, event)
    O.sensor.EDCurrent(end+1) = event.Value;
    O.sensor.EDCurrenttime(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
end
    
function setPumpFieldChanged(O, event, identifier)
    O.GUI.pump(identifier).field.Value = event.Value;
    O.sensor.pump(identifier).setFlow.value(end+1) = event.Value;
    O.sensor.pump(identifier).setFlow.t(end+1) = (now - O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
end
    