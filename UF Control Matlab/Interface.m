classdef Interface < handle
    
    properties
        
        GUI %General User Interface
        
        arduinoObj
        
        configuration %matrices to decide which sensors are connected etc
        
        names %to display all the sensors with their names
        
        sensor % to store the values and read them 
        
        timerLog %timer and functions
        
        export %things that will be exported for the measurements
        
        normalSetup % all valves at 0 volt
        
        backflushSetup % all valves at 5 volt
        
        transmembraneTimer % To check if the transmembrane pressure is at a good level
        
        systemTimer %including the backwash directly when a critical TMP is reached
        
        feedCount = 0;
        
    end
    
    %IDEA TO SHOW THE TIME: datetime(now,'ConvertFrom','datenum','Format','HH:mm:ss')
    
    
    methods
        
        function O = Interface(arduinoObj, configuration, names, filename)
            
            O.export.filename = filename;
            
            O.names = names;
            
            O.sensor.num = 0;
            
            O.configuration = configuration;
            
            O.arduinoObj = arduinoObj;
            
            O.timerLog = timer('ExecutionMode', 'fixedSpacing','Period',1, 'BusyMode', 'drop');

            O.timerLog.StartFcn = @(~,~)disp('The measurements have started');

            O.timerLog.StopFcn = @(~,~)disp('The measurements have ended');

            O.timerLog.TimerFcn = @(~,~)plotValues(O);
            
            %-------
            O.normalSetup = timer('ExecutionMode', 'fixedSpacing', 'TasksToExecute', 1);

            O.normalSetup.StartFcn = @(~,~)disp('Normal Setup started');

            O.normalSetup.StopFcn = @(~,~)disp('Normal Setup is finished');

            O.normalSetup.TimerFcn = @(~,~)normalSetup(O);
            
            %-----
            O.backflushSetup = timer('ExecutionMode', 'fixedSpacing', 'TasksToExecute', 1);

            O.backflushSetup.StartFcn = @(~,~)disp('Backflush Setup started');

            O.backflushSetup.StopFcn = @(~,~)disp('Backflush Setup is finished');

            O.backflushSetup.TimerFcn = @(~,~)backflushSetup(O);
            
            %----
            O.transmembraneTimer = timer('ExecutionMode', 'fixedSpacing','Period',1);

            O.transmembraneTimer.StartFcn = @(~,~)disp('TMP tester started');

            O.transmembraneTimer.StopFcn = @(~,~)disp('TMP tester is finished');

            O.transmembraneTimer.TimerFcn = @(~,~)measurecriticalTMP(O);
            
            %----
            
            O.systemTimer = timer('ExecutionMode', 'fixedSpacing','Period',1);

            O.systemTimer.StartFcn = @(~,~)disp('Overall System started');

            O.systemTimer.StopFcn = @(~,~)disp('Overall System is finished');

            O.systemTimer.TimerFcn = @(~,~)controlSystem(O);
            
            O.GUI.fig = uifigure();
            O.GUI.fig.Position = [100, 80, 900, 705];
            O.GUI.fig.Scrollable = 'on';
            
            % Callback functions
            O.GUI.fig.CloseRequestFcn = @(src,event)closeFig(O);
            
            O.GUI.overallGrid = uigridlayout(O.GUI.fig);
            
            O.GUI.overallGrid.RowHeight = {'fit', 'fit', 'fit', 'fit', 'fit', 'fit', 'fit', 'fit'};
            O.GUI.overallGrid.ColumnWidth = {'fit', 'fit', 'fit', 'fit'};
            O.GUI.overallGrid.Scrollable = 'on';
            
            
            % ---------- Setup of Button Panel
            O.GUI.buttonPanel = uipanel(O.GUI.overallGrid);
            O.GUI.buttonPanel.Layout.Row = 2;
            O.GUI.buttonPanel.Layout.Column = 1;
            
            O.GUI.buttonGrid = uigridlayout(O.GUI.buttonPanel);
            O.GUI.buttonGrid.RowHeight = {'fit', 'fit'};
            O.GUI.buttonGrid.ColumnWidth = {'fit', 'fit'};
            
            O.GUI.startButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.startButton.Text = 'Start Measurements';
            O.GUI.startButton.Layout.Row = 1;
            O.GUI.startButton.Layout.Column = 1;
            O.GUI.startButton.Value = false;
            
            O.GUI.startButton.ValueChangedFcn = @(src,event)startMeasuring(O, event);

            O.GUI.startControlButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.startControlButton.Text = 'Start the Valve Control';
            O.GUI.startControlButton.Layout.Row = 3;
            O.GUI.startControlButton.Layout.Column = 1;
            O.GUI.startControlButton.Value = false;
            
            O.GUI.startControlButton.ValueChangedFcn = @(src,event)startControl(O, event);
            
            O.GUI.startBackwashButton = uibutton(O.GUI.buttonGrid,'state'); %--------- added by Yannik ---------------------
            O.GUI.startBackwashButton.Text = 'Start Backwash';
            O.GUI.startBackwashButton.Layout.Row = 4;
            O.GUI.startBackwashButton.Layout.Column = 1;
            O.GUI.startBackwashButton.Value = false;
            
            O.GUI.startBackwashButton.ValueChangedFcn = @(src,event)startBackwash(O, event); %--------- added by Yannik ---------------------
            
            O.GUI.startPumpButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.startPumpButton.Text = 'Start the Feed Pump';
            O.GUI.startPumpButton.Layout.Row = 2;
            O.GUI.startPumpButton.Layout.Column = 1;
            O.GUI.startPumpButton.Value = false;
            
            O.GUI.startPumpButton.ValueChangedFcn = @(src,event)startFeedPump(O, event);
            
            O.GUI.startSystemButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.startSystemButton.Text = 'Start the UF';
            O.GUI.startSystemButton.Layout.Row = 5;
            O.GUI.startSystemButton.Layout.Column = 1;
            O.GUI.startSystemButton.Value = false;
            
            O.GUI.startSystemButton.ValueChangedFcn = @(src,event)startSystem(O, event);
            
            O.GUI.closeButton = uibutton(O.GUI.buttonGrid,'state');
            O.GUI.closeButton.Text = 'Stop System';
            O.GUI.closeButton.Layout.Row = 6;
            O.GUI.closeButton.Layout.Column = 1;
            O.GUI.closeButton.Value = false;
            
            O.GUI.closeButton.ValueChangedFcn = @(src,event)stopSystem(O, event.Value);
            
            % ---------- Setup of Proportional Control Valve Graphs
            O.GUI.pcvPanel = uipanel(O.GUI.overallGrid);
            O.GUI.pcvPanel.Layout.Row = [1 2];
            O.GUI.pcvPanel.Layout.Column = 4;
            
            O.GUI.pcvGrid = uigridlayout(O.GUI.pcvPanel);
            O.GUI.pcvGrid.RowHeight = {'fit', 'fit'};
            O.GUI.pcvGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of Pump Graphs
            O.GUI.pumpPanel = uipanel(O.GUI.overallGrid);
            O.GUI.pumpPanel.Layout.Row = 1;
            O.GUI.pumpPanel.Layout.Column = 1;
            
            O.GUI.pumpGrid = uigridlayout(O.GUI.pumpPanel);
            O.GUI.pumpGrid.RowHeight = {'fit', 'fit'};
            O.GUI.pumpGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of OC-Valve Graphs (normally open) ---------------------- added by Yannik
            O.GUI.ocvNOPanel = uipanel(O.GUI.overallGrid);
            O.GUI.ocvNOPanel.Layout.Row = 4;
            O.GUI.ocvNOPanel.Layout.Column = 1;
            
            O.GUI.ocvNOGrid = uigridlayout(O.GUI.ocvNOPanel);
            O.GUI.ocvNOGrid.RowHeight = {'fit', 'fit'};
            O.GUI.ocvNOGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of OC-Valve Graphs (normally closed) -------------------- added by Yannik
            O.GUI.ocvNCPanel = uipanel(O.GUI.overallGrid);
            O.GUI.ocvNCPanel.Layout.Row = 4;
            O.GUI.ocvNCPanel.Layout.Column = 2;
            
            O.GUI.ocvNCGrid = uigridlayout(O.GUI.ocvNCPanel);
            O.GUI.ocvNCGrid.RowHeight = {'fit', 'fit'};
            O.GUI.ocvNCGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of C-Valve Graphs --------------------------------------- added by Yannik
            O.GUI.cvPanel = uipanel(O.GUI.overallGrid);
            O.GUI.cvPanel.Layout.Row = 4;
            O.GUI.cvPanel.Layout.Column = 3;
            
            O.GUI.cvGrid = uigridlayout(O.GUI.cvPanel);
            O.GUI.cvGrid.RowHeight = {'fit', 'fit'};
            O.GUI.cvGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of Fields for the Massflow Setting to control them
            
            O.GUI.mfSetPanel = uipanel(O.GUI.overallGrid);
            O.GUI.mfSetPanel.Layout.Row = 2;
            O.GUI.mfSetPanel.Layout.Column = 2;
            
            O.GUI.mfSetGrid = uigridlayout(O.GUI.mfSetPanel);
            O.GUI.mfSetGrid.RowHeight = {'fit'};
            O.GUI.mfSetGrid.ColumnWidth = {'fit'};
            
            % ---------- Setup of Fields for the Massflow Setting for the Pump
            
            O.GUI.pumpSetPanel = uipanel(O.GUI.overallGrid);
            O.GUI.pumpSetPanel.Layout.Row = 2;
            O.GUI.pumpSetPanel.Layout.Column = 3;
            
            O.GUI.pumpSetGrid = uigridlayout(O.GUI.pumpSetPanel);
            O.GUI.pumpSetGrid.RowHeight = {'fit'};
            O.GUI.pumpSetGrid.ColumnWidth = {'fit'};
            
            
            % ---------- Setup of Flow Graphs
            O.GUI.flowPanel = uipanel(O.GUI.overallGrid);
            O.GUI.flowPanel.Layout.Row = 1;
            O.GUI.flowPanel.Layout.Column = [2 3];
            
            O.GUI.flowGrid = uigridlayout(O.GUI.flowPanel);
            O.GUI.flowGrid.RowHeight = {'fit', 'fit'};
            O.GUI.flowGrid.ColumnWidth = {'fit', 'fit'};
            
            
            % ---------- Setup of Pressure Graphs
            O.GUI.pressurePanel = uipanel(O.GUI.overallGrid);
            O.GUI.pressurePanel.Layout.Row = 3;
            O.GUI.pressurePanel.Layout.Column = [1 3];
            
            O.GUI.pressureGrid = uigridlayout(O.GUI.pressurePanel);
            O.GUI.pressureGrid.RowHeight = {'fit', 'fit'};
            O.GUI.pressureGrid.ColumnWidth = {'fit', 'fit'};
            
            % ---------- Setup of Transmembrane Pressure
            O.GUI.transmembranePressurePanel = uipanel(O.GUI.overallGrid);
            O.GUI.transmembranePressurePanel.Layout.Row = 3;
            O.GUI.transmembranePressurePanel.Layout.Column = 4;
            
            O.GUI.transmembranePressureGrid = uigridlayout(O.GUI.transmembranePressurePanel);
            O.GUI.transmembranePressureGrid.RowHeight = {'fit', 'fit'};
            O.GUI.transmembranePressureGrid.ColumnWidth = {'fit', 'fit'};
                        
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
        
            %Pressure Sensors
            for identifier = 1:3
                if O.configuration.pressure(identifier,1)
                    pressureGraphSetup(O,identifier);
                    O.sensor.pressure(identifier) = pressureSensor(O.arduinoObj, O.configuration.pressure(identifier, 2), identifier, O.names.pressure(identifier), O.configuration.pressure(identifier, 3), O.configuration.pressure(identifier, 4), O.GUI.closeButton, O);
                else
                    O.sensor.pressure(identifier) = pressureSensor(O.arduinoObj, O.configuration.pressure(identifier, 2), identifier, O.names.pressure(identifier), O.configuration.pressure(identifier, 3), O.configuration.pressure(identifier, 4), O.GUI.closeButton, O);
                end
            end
            
            %Pressure Sensors
            if O.configuration.transmembrane(1,1)
                O.sensor.transmembrane = struct('data', 0, 'time', 0, 'end', 10, 'begin', 10);
                transmembranePressureGraphSetup(O,1);
            end
            
            %PCV
            for identifier = 1:2
                if O.configuration.pcv(identifier,1)
                    pcvGraphSetup(O,identifier);
                    mfSetSetup(O,identifier);
                    O.sensor.pcv(identifier) = pcv(O.arduinoObj, identifier, O.names.pcv(identifier), O.configuration.pcv(identifier,2), O.configuration.pcv(identifier,3), O.configuration.pcv(identifier,4), O.configuration.pcv(identifier,5), O.sensor.mf(O.configuration.pcv(identifier,6)), O.sensor.pressure);
                else
                    O.sensor.pcv(identifier) = pcv(O.arduinoObj, identifier, O.names.pcv(identifier),0.5,0,0,0,0,0);
                end
                O.sensor.pcv(identifier).changeSetting;
            end
            
            %ocvNO ------------------------------- added by Yannik
            
            O.sensor.ocvNO(1) = ocvNO(O.arduinoObj, 1, O.names.ocvNO(1));
            ocvNOGraphSetup(O,1);

            
            %ocvNC ------------------------------- added by Yannik
            
            O.sensor.ocvNC(1) = ocvNC(O.arduinoObj, 1, O.names.ocvNC(1));
            ocvNCGraphSetup(O,1);

            
            %cv ------------------------------------ added by Yannik
            O.sensor.cv(1) = cv(O.arduinoObj, 1, O.names.cv(1));
            cvGraphSetup(O,1);

            
            %Pumps
            for identifier = 1:2
                if O.configuration.pump(identifier,1)
                    pumpGraphSetup(O,identifier);
                    pumpSetSetup(O,identifier);
                    O.sensor.pump(identifier) = Pump(O.arduinoObj, O.configuration.pump(identifier,2), identifier, O.names.pump(identifier), O.configuration.pump(identifier,3), O.configuration.pump(identifier,4), O.configuration.pump(identifier,5), O.sensor.mf(O.configuration.pump(identifier,6)), O.sensor.pressure, O.configuration.pump(identifier,7), O);
                else
                    O.sensor.pump(identifier) = Pump(O.arduinoObj, O.configuration.pump(identifier,2), identifier, O.names.pump(identifier), O.configuration.pump(identifier,3), 0, 0, 0, 0, 0 , 0);
                end
            end
            
            
        end %createGraphs
        
        
        %%
        
        function mfSetSetup(O, identifier)    
            
            name = ["Set Massflow for PCV D [l/min]" "Set Massflow for PCV C [l/min]"];
            
            O.GUI.mfSet(identifier).connection = uigridlayout(O.GUI.mfSetGrid);
            O.GUI.mfSet(identifier).connection.RowHeight = {'fit', 'fit'};
            O.GUI.mfSet(identifier).connection.ColumnWidth = {'fit'};
            O.GUI.mfSet(identifier).connection.Layout.Row = identifier;
            O.GUI.mfSet(identifier).connection.Layout.Column = 1;
            
            O.GUI.mfSet(identifier).label = uilabel(O.GUI.mfSet(identifier).connection);
            O.GUI.mfSet(identifier).label.Text = name(identifier);
            O.GUI.mfSet(identifier).label.FontSize = 14;
            O.GUI.mfSet(identifier).label.FontWeight = 'bold';
            O.GUI.mfSet(identifier).label.HorizontalAlignment = 'center';
            O.GUI.mfSet(identifier).label.Layout.Row = 1;
            O.GUI.mfSet(identifier).label.Layout.Column = 1;
            
            O.GUI.mfSet(identifier).field = uieditfield(O.GUI.mfSet(identifier).connection,'numeric');
            O.GUI.mfSet(identifier).field.Value = O.configuration.pcv(identifier,3);
            
            %Callback functions
            O.GUI.mfSet(identifier).field.ValueChangedFcn = @(~,event)setPressureFieldChanged(O, event, identifier);
            
        end
        
        function pumpSetSetup(O, identifier)    
            
            name = ["Set Massflow for Backwash Pump [l/min]" "Set Massflow for Feed Pump[l/min]"];
            
            O.GUI.pumpSet(identifier).connection = uigridlayout(O.GUI.pumpSetGrid);
            O.GUI.pumpSet(identifier).connection.RowHeight = {'fit', 'fit'};
            O.GUI.pumpSet(identifier).connection.ColumnWidth = {'fit'};
            O.GUI.pumpSet(identifier).connection.Layout.Row = identifier;
            O.GUI.pumpSet(identifier).connection.Layout.Column = 1;
            
            O.GUI.pumpSet(identifier).label = uilabel(O.GUI.pumpSet(identifier).connection);
            O.GUI.pumpSet(identifier).label.Text = name(identifier);
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
        
        function pcvGraphSetup(O,identifier)
            
            rowIdentifier = [1, 2];
            columnIdentifier = [1, 1];
            
            O.GUI.pcv(identifier).ax = uiaxes(O.GUI.pcvGrid,...
                                        'YLim',[0 5],...
                                        'XLim', [-inf inf]);
            O.GUI.pcv(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.pcv(identifier).ax.Layout.Column = columnIdentifier(identifier);
            O.GUI.pcv(identifier).ax.Title.String = O.names.pcv(identifier,1);
            O.GUI.pcv(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.pcv(identifier).ax.YLabel.String = 'Voltage input [V]';
            O.GUI.pcv(identifier).ax.Box = 'on';
            O.GUI.pcv(identifier).ax.XMinorGrid = 'on';
            O.GUI.pcv(identifier).ax.YMinorGrid = 'on';
            
        end
        
        function ocvNOGraphSetup(O,identifier) %--------------------------------- added by Yannik
            
            O.GUI.ocvNO(identifier).ax = uiaxes(O.GUI.ocvNOGrid,...
                                        'YLim',[0 5],...
                                        'XLim', [-inf inf]);
            O.GUI.ocvNO(identifier).ax.Layout.Row = 1;
            O.GUI.ocvNO(identifier).ax.Layout.Column = 1;
            O.GUI.ocvNO(identifier).ax.Title.String = O.names.ocvNO(identifier,1);
            O.GUI.ocvNO(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.ocvNO(identifier).ax.YLabel.String = 'Voltage input [V]';
            O.GUI.ocvNO(identifier).ax.Box = 'on';
            O.GUI.ocvNO(identifier).ax.XMinorGrid = 'on';
            O.GUI.ocvNO(identifier).ax.YMinorGrid = 'on';
            
        end
        
        function ocvNCGraphSetup(O,identifier) %-------------------------------- added by Yannik
            
            O.GUI.ocvNC(identifier).ax = uiaxes(O.GUI.ocvNCGrid,...
                                        'YLim',[0 5],...
                                        'XLim', [-inf inf]);
            O.GUI.ocvNC(identifier).ax.Layout.Row = 1;
            O.GUI.ocvNC(identifier).ax.Layout.Column = 1;
            O.GUI.ocvNC(identifier).ax.Title.String = O.names.ocvNC(identifier,1);
            O.GUI.ocvNC(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.ocvNC(identifier).ax.YLabel.String = 'Voltage input [V]';
            O.GUI.ocvNC(identifier).ax.Box = 'on';
            O.GUI.ocvNC(identifier).ax.XMinorGrid = 'on';
            O.GUI.ocvNC(identifier).ax.YMinorGrid = 'on';
            
        end
        
        function cvGraphSetup(O,identifier) %-------------------------------- added by Yannik
            
            rowIdentifier = 1;
            columnIdentifier = 1;
            
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
        
        function pumpGraphSetup(O,identifier)
            
            rowIdentifier = [1, 2];
            columnIdentifier = [1, 1];
            
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
            
        end
        
        function pressureGraphSetup(O,identifier)
            
            rowIdentifier = [1, 1, 1];
            columnIdentifier = [1, 2, 3];
            
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
        
        function transmembranePressureGraphSetup(O,identifier)
            
            rowIdentifier = 1;
            columnIdentifier = 1;
            
            O.GUI.transmembranePressure(identifier).ax = uiaxes(O.GUI.transmembranePressureGrid,...
                'YLim',[0 6],...
                'XLim', [-inf inf]);
            O.GUI.transmembranePressure(identifier).ax.Layout.Row = rowIdentifier(identifier);
            O.GUI.transmembranePressure(identifier).ax.Layout.Column = columnIdentifier(identifier);
            O.GUI.transmembranePressure(identifier).ax.Title.String = "Transmembrane Pressure";
            O.GUI.transmembranePressure(identifier).ax.XLabel.String = 'time [s]';
            O.GUI.transmembranePressure(identifier).ax.YLabel.String = 'Transmembrane pressure [bar]';
            O.GUI.transmembranePressure(identifier).ax.Box = 'on';
            O.GUI.transmembranePressure(identifier).ax.XMinorGrid = 'on';
            O.GUI.transmembranePressure(identifier).ax.YMinorGrid = 'on';
            set(O.GUI.transmembranePressure(identifier).ax,'NextPlot','replacechildren')
            
        end %end transmembranePressureGraphSetup
     
        %% PLOTTING
        
        function plotValues(O)
            
            O.arduinoObj.flushing;
            O.arduinoObj.flushing;
            
            %Plot pressure sensors
            for identifier = 1:3
                if O.configuration.pressure(identifier,1)
                    O.sensor.pressure(identifier).num = O.sensor.pressure(identifier).num + 1;
                    O.sensor.num = O.sensor.num + 1;
                    if O.sensor.num == 1
                        O.sensor.pressure(identifier).time(end+1) = now;
                        O.sensor.beginTimeIdentifier = identifier;
                        
                        for i = 1:2
                            O.sensor.pcv(i).beginTimeIdentifier = identifier;
                            O.sensor.pump(i).beginTimeIdentifier = identifier;
                        end
                        
                        break
                    end
                    
                    if O.sensor.pressure(identifier).num == 3
                        start(O.sensor.pressure(identifier).pressureTimer);
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
            
            %Plot transmembrane pressure
            for identifier = 1
                if O.configuration.pressure(identifier,1)

                    O.sensor.transmembrane.time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    O.sensor.transmembrane.data(end+1) = O.sensor.pressure(O.configuration.transmembrane(2,1)).data(end) - O.sensor.pressure(O.configuration.transmembrane(3,1)).data(end);
                    elapsedTime = linspace(0, O.sensor.transmembrane.time(end), length(O.sensor.transmembrane.data));
                    if length(O.sensor.transmembrane.data)== 5
%                         start(O.transmembraneTimer)
                    end
                    if length(O.sensor.transmembrane.time) > 15
                        O.GUI.transmembranePressure.ax.XLim = [O.sensor.transmembrane.time(end-13) O.sensor.transmembrane.time(end)];
                        O.GUI.transmembranePressure.ax.YLim = [min(O.sensor.transmembrane.data((end-13):end))-0.3 max(O.sensor.transmembrane.data((end-14):end))+0.3];
                    else 
                        O.GUI.transmembranePressure.ax.YLim = [min(O.sensor.transmembrane.data)-0.1 max(O.sensor.transmembrane.data)+0.1];
                    end

                    O.GUI.transmembranePressure.ax.Title.String = ['Transmembrane current value: ', num2str(O.sensor.transmembrane.data(end)), ' bar'];
                    plot(O.GUI.transmembranePressure.ax, elapsedTime, O.sensor.transmembrane.data);
                end
            end
            
            %Plot pcvs
            for identifier = 1:2
                if O.configuration.pcv(identifier,1)
                    O.sensor.pcv(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    O.sensor.pcv(identifier).data(end+1) = O.sensor.pcv(identifier).value;
                    elapsedTime = linspace(0, O.sensor.pcv(identifier).time(end), length(O.sensor.pcv(identifier).data));
                    if length(O.sensor.pcv(identifier).time) > 15
                        O.GUI.pcv(identifier).ax.XLim = [O.sensor.pcv(identifier).time(end-13) O.sensor.pcv(identifier).time(end)];
                        O.GUI.pcv(identifier).ax.YLim = [min(O.sensor.pcv(identifier).data((end-13):end))-0.3 max(O.sensor.pcv(identifier).data((end-14):end))+0.3];
                    else 
                        O.GUI.pcv(identifier).ax.YLim = [min(O.sensor.pcv(identifier).data)-0.3 max(O.sensor.pcv(identifier).data)+0.3];
                    end
                    O.GUI.pcv(identifier).ax.Title.String = [O.names.pcv(identifier,1); 'current value: ', num2str(O.sensor.pcv(identifier).data(end)), ' Volt'];
                    plot(O.GUI.pcv(identifier).ax, elapsedTime, O.sensor.pcv(identifier).data);
                end
            end
            
            
            %Plot pump input
            for identifier = 1:2
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
            
            %Plot ocvNO -------------------- added by Yannik
            for identifier = 1
                O.sensor.ocvNO(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                O.sensor.ocvNO(identifier).data(end+1) = O.sensor.ocvNO(identifier).value;
                elapsedTime = linspace(0, O.sensor.ocvNO(identifier).time(end), length(O.sensor.ocvNO(identifier).data));
                if length(O.sensor.ocvNO(identifier).time) > 15
                    O.GUI.ocvNO(identifier).ax.XLim = [O.sensor.ocvNO(identifier).time(end-13) O.sensor.ocvNO(identifier).time(end)];
                    O.GUI.ocvNO(identifier).ax.YLim = [min(O.sensor.ocvNO(identifier).data((end-13):end))-0.3 max(O.sensor.ocvNO(identifier).data((end-14):end))+0.3];
                else 
                    O.GUI.ocvNO(identifier).ax.YLim = [min(O.sensor.ocvNO(identifier).data)-0.3 max(O.sensor.ocvNO(identifier).data)+0.3];
                end
                O.GUI.ocvNO(identifier).ax.Title.String = [O.names.ocvNO(identifier,1); 'current value: ', num2str(O.sensor.ocvNO(identifier).data(end)), ' Volt'];
                plot(O.GUI.ocvNO(identifier).ax, elapsedTime, O.sensor.ocvNO(identifier).data);
            end
            
            %Plot ocvNC -------------------- added by Yannik
            for identifier = 1
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
            
           %Plot cv -------------------- added by Yannik
           for identifier = 1
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
            
           O.arduinoObj.flushing;
            
            %Plot massflow sensors
            for identifier = 1:4
                if O.configuration.mf(identifier,1)
                    O.sensor.mf(identifier).time(end+1) = (now-O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
                    % exclude NaN
                    mfValue = O.sensor.pressure(identifier).value;
                    count = 0;
                    while isnan(mfValue)
                        mfValue = O.sensor.pressure(identifier).value;
                        count = count + 1;
                        if count == 10
                            warning('Something is wrong with the Arduino - it always gives NaN - check the system');
                        end
                    end
                    O.sensor.mf(identifier).data(end+1) = mfValue;
                    elapsedTime = linspace(0, O.sensor.mf(identifier).time(end), length(O.sensor.mf(identifier).data));
                    if length(O.sensor.mf(identifier).time) > 15
                        O.GUI.mf(identifier).ax.XLim = [O.sensor.mf(identifier).time(end-13) O.sensor.mf(identifier).time(end)];
                        O.GUI.mf(identifier).ax.YLim = [min(O.sensor.mf(identifier).data((end-13):end))-0.3 max(O.sensor.mf(identifier).data((end-14):end))+0.3];
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
            
        end % end plotValues
        
        function endSystem(O)
            
            %stop pumpTimer
            if O.GUI.startPumpButton.Value == true
                for identifier = 2
                    if O.configuration.pump(identifier,1)
                        stop(O.sensor.pump(identifier).pumpTimer);
                        delete(O.sensor.pump(identifier).pumpTimer);
                    end
                end
                
            elseif O.GUI.startBackwashButton.Value == true
                for identifier = 1
                    if O.configuration.pump(identifier,1)
                        stop(O.sensor.pump(identifier).pumpTimer);
                        delete(O.sensor.pump(identifier).pumpTimer);
                    end
                end
            end
            
            pause(0.5)
            
            % SET THE PUMPS TO 0 and display this!
            for identifier = 1:2
                if O.configuration.pump(identifier,1) == 1
                   O.sensor.pump(identifier).value = 0;
                   O.sensor.pump(identifier).changeSetting;
                end
            end

            disp('The Pumps are set to 0 rpm');

            %Stop pressureTimer
            for identifier = 1:3
                if O.configuration.pressure(identifier,1)
                    stop(O.sensor.pressure(identifier).pressureTimer);
                    delete(O.sensor.pressure(identifier).pressureTimer);
                end
            end
            
            %stop transmembrane pressure timer
            
            stop(O.transmembraneTimer);
            delete(O.transmembraneTimer);

            %stop pcvTimer
            if O.GUI.startControlButton.Value == true
                for identifier = 1:2
                    if O.configuration.pcv(identifier,1)
                        stop(O.sensor.pcv(identifier).pcvTimer);
                        delete(O.sensor.pcv(identifier).pcvTimer);
                    end
                end
            end

            %Stop plotting
            if O.GUI.startButton.Value == true
                stop(O.timerLog);
            end
            
            %stop Controller
            if O.GUI.startSystemButton.Value == true;
                stop(O.systemTimer)
            end

            delete(O.timerLog);

            delete(O.GUI.fig);
            delete(O.arduinoObj);
            disp('Disconnected from Arduino');

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
    
end %end startMeasuring

function startSystem(O, event)

    if event.Value
        O.GUI.startSystemButton.Value = event.Value;
        start(O.systemTimer)
    else
        O.GUI.startSystemButton.Value = event.Value;
        stop(O.systemTimer)
        O.endSystem;
    end

end

function startFeedPump(O, event)
    
    if event.Value
        O.GUI.startPumpButton.Value = true;
        start(O.normalSetup);
        startPump(O,2);
    else
        O.GUI.startPumpButton.Value = false;
        stopPump(O,2);
    end
    
end %end startFeedPump

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
       pause(0.3)
       O.sensor.pump(identifier).value = 0;
       O.sensor.pump(identifier).setValue(end) = 0;
       O.sensor.pump(identifier).changeSetting;
    end
    
end %end stopPump

function measurecriticalTMP(O)
            
    average = sum(O.sensor.transmembrane.data(end-2:end))/3;

    if average > O.configuration.transmembrane(4,1)
        disp('The TMP has reached the critical value so the feed pump was shut down');
        
        stopPump(O,2)
        O.GUI.startPumpButton.Value = false;
    end
            
end % end controlCriticalTMP

function controlSystem(O)

    average = sum(O.sensor.transmembrane.data(end-2:end))/3;
    
    %O.feedCount := pump state
    if O.feedCount == 0 %Normal Feed Operation
        start(O.normalSetup);
        startPump(O,2); %feed pump
        O.feedCount = 1;
    elseif average > O.configuration.transmembrane(4,1) && O.feedCount == 1 %Check if the transmembrane pressure is not too high
        disp('The TMP has reached the critical value so the feed pump was shut down');
        stopPump(O,2) %feed pump
        O.feedCount = 2;
    elseif O.feedCount == 2 %Backwash Operation
        start(O.backflushSetup);
        startPump(O,1);
        O.feedCount = 3; %just that it does not always want to start the backflush pump again when it is already running
    end

end
        
function backflushSetup(O)
    
    O.sensor.ocvNC(1).open;
    O.sensor.ocvNO(1).close;
    O.sensor.cv(1).open;
    O.sensor.pcv(2).value = 0;
    O.sensor.pcv(2).setValue = 0;
    O.sensor.pcv(2).changeSetting;
    
end

function normalSetup(O)
    
    O.sensor.ocvNC(1).close;
    O.sensor.ocvNO(1).open;
    O.sensor.cv(1).close;
    
end

function startBackwash(O, event)
    
    if event.Value
        O.GUI.startBackwashButton.Value = true;
        start(O.backflushSetup);
        startPump(O,1);
    else
        O.GUI.startBackwashButton.Value = false;
        stopPump(O,1);
    end
    
end

function startControl(O, event)
    
    if event.Value
        O.GUI.startControlButton.Value = true;
        for identifier = 1:2
            if O.configuration.pcv(identifier,1)
                start(O.sensor.pcv(identifier).pcvTimer);
            end
        end
    else
        O.GUI.startControlButton.Value = false;
        for identifier = 1:2
            if O.configuration.pcv(identifier,1)
                stop(O.sensor.pcv(identifier).pcvTimer);
            end
        end
    end    
end

function stopSystem(O,event)

    if O.GUI.closeButton.Value == true || event.Value
        
        O.endSystem;
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
    
function setPressureFieldChanged(O, event, identifier)
    % Do an error if the value is too high or too low
    O.GUI.pcv(identifier).field.Value = event.Value;
    O.sensor.pcv(identifier).setFlow.value(end+1) = event.Value;
    O.sensor.pcv(identifier).setFlow.t(end+1) = now;
end

function setPumpFieldChanged(O, event, identifier)
    O.GUI.pump(identifier).field.Value = event.Value;
    O.sensor.pump(identifier).setFlow.value(end+1) = event.Value;
    O.sensor.pump(identifier).setFlow.t(end+1) = (now - O.sensor.pressure(O.sensor.beginTimeIdentifier).time(2))*3600*24;
end