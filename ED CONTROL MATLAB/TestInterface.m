%TestInterface of ED General Code

close all;
clear;
clc;


%Look in your arduino IDE which port you are connected to
arduinoObj = talkToArduino('COM8');

%CONFIGURATION PUMP
%first column with 1 or 0 if it is used for a pump or not
%second column for maximum Volt input
%third column for desired permeate massflow in l/min !!!!
%fourth column for the Kp constant
%fifth column for the Ki constant
%sixth column to say which massflow sensor to control in the normal operation, 1 for A5, 2 for A6, 3 for A7, 4 for A8   
%seventh column to say which massflow sensor to control in the backflush operation, 1 for A5, 2 for A6, 3 for A7, 4 for A8
configuration.pump = [1 5 0.25  1 0.1   4 4; %A -- Posttreatment Pump
                      1 5 2.5   2 0     3 3; %B --Rinse Pump always at 150 l/h
                      1 5 0.25  1 0     1 2; %C -- Concentrate
                      1 5 0.25  1 0     2 1]; %D -- Diluate

names.pump = ["Posttreatment Pump";
              "Rinse Pump";
              "Concentrate Pump";
              "Diluate Pump"];

%First input after how many seconds the polarity should be reversed
%Second input how long the "flush" should last
configuration.switchTime = [60;
                            20];

%CONFIGURATION MASSFLOW
%first column is either 1 or 0 if the sensor is used or not
%the second column for the maximum massflow in l/min
configuration.mf = [1 5; %A5
                    1 5; %A6
                    1 5; %A7
                    1 5];%A8

names.mf = ["Concentrate Flow";
            "Diluate Flow";
            "Rinse Flow";
            "Posttreatment Flow"];

%CONFIGURATION PRESSURE SENSORS
%first column is either 1 or 0 if the sensor is used or not
%second column for the maximum pressure in bar (Sick measures until 6 bar and the Gems pressure sensor until 10 bar)
%third column is the critical value you do not want to overshoot
%fourth column is the pressure that is near to the critical value where you want to
%be notified by a warning
configuration.pressure = [0 10 5 4.7; %A0 --> Gems
                          1 6 6 6; %A1
                          1 6 6 6; %A2
                          1 6 6 6; %A3
                          0 6 5 4.7; %A4
                          0 6 5 4.7]; %A15!!

names.pressure = ["Gems pressure sensor A0"; %1
                  "Diluate in Pressure"; %2 --A1  %TODO: only 3 pressure sensors!!
                  "Concentrate in Pressure"; %3 --A2
                  "Rinse Pressure"; %4 -- A3
                  "Pressure Sensor"; %5 -- A4
                  "Pressure Sensor"]; %6 -- A15

%Pressure difference
%first input if you want the pressure difference monitored or not
%second input for diluate pressure 2 for A1, 3 for A2, 4 for A3 !!!!!!!! LOOK IT IS ALWAYS ONE DIFFERENT
%third input for concentrate pressure 2 for A1, 3 for A2, 4 for A3
%fourth input for the maximum pressure difference
configuration.pressuredifferenceDC = [1; %is it used or not
                                      2; % Diluate pressure Sensor
                                      3; %Concentrate pressure sensor
                                      0.2]; %maximum pressure difference

%Pressure Difference between Rinse and Diluate
configuration.pressuredifferenceRD = [1; %is it used or not
                                      2; % Diluate pressure Sensor
                                      4; % Rinse pressure sensor
                                      10]; %maximum pressure difference


%CONFIGURATION CONDUCTIVITY SENSORS
%first column is either 1 or 0 if the sensor is used or not
%second column for the maximum conductivity in mS/cm
%third column for minimum conductivity in mS/cm
%fourth column for Kp
%fifth column for Ki
configuration.conductivity = [1 10 0.1 1 0; %Channel 1 -- Diluate out
                              1 60 50 0 0; %Channel 2 -- Concentrate
                              1 10 0.1 0 0]; %Channel 3 -- Diluate in


configuration.maxConductivity = 56; %mS/cm


%it needs to be double checked that this is also the order that they are
%plugged into the arduino and transmitter

names.conductivity = ["Diluate OUT Conductivity";
                      "Concentrate Conductivity";
                      "Diluate in Conductivity"];

%To say which ones are used
configuration.ocvNC = [1; %D44
                       0; %D45 % TODO: only ONE ocvNC !!
                       0];%D46

names.ocvNC = ["ocvNC ConcTank"; %D44
               "ocvNC D45"; %D45
               "ocvNC D46"]; %D46

%To say which ones are used
configuration.cv = [1; %D38 - before diluate - E101
                    1; %D39 - before concentrate - E102
                    1; %D40 - after diluate - E103
                    1; %D41 - after concentrate - E104
                    1];%D42 - BEFORE DILUATE - FOR THE NEW CONTROL

names.cv = ["cv D38"; %D38
            "cv D39"; %D39
            "cv D40"; %D40
            "cv D41"; %D41
            "CV3 before diluate"];%D42

%To say which ones are connected
configuration.ls = [1; %Highest of the ED Split Tank-1
                    1; %Lowest of the ED Split Tank-2
                    1; %Middle of the ED Split Tank-3
                    1; %ED Concentrate-4
                    1; %lowest of UF Tank-5
                    1; %ED Rinse-6
                    1];%

%OLD
configuration.ls = [1; %lowest of the UF Tank - 1
                    1; %highest of the ED Conc Tank - 2
                    1; % -3
                    1; %middle of the ED Split Tank -4
                    1; %Lowest of the ED Split Tank -5
                    1; %ED Rinse -6
                    1];%Highest of the ED Split Tank - 7

names.ls = ["ls22";
            "ls23";
            "ls24";
            "ls25";
            "ls26";
            "ls27";
            "ls28"];

%What you want your file to be named for the measurements
filename = 'TestDana.mat';

O = Interface(arduinoObj, configuration, names, filename);

