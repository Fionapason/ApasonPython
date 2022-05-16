close all;
clear;
clc;

%Look in your arduino IDE which port you are connected to
arduinoObj = talkToArduino('COM8', 115200);
% arduinoUno = talkToArduino('COM4', 9600);
arduinoUno = 0;

%CONFIGURATION PUMP
%first column with 1 or 0 if it is used for a pump or not
%second column for maximum Volt input
%third column for desired massflow in l/min !!!!
%fourth column for the Kp constant
%fifth column for the Ki constant
%sixth column to say which massflow sensor to control, 1 for A5, 2 for A6, 3 for A7, 4 for A8   
%seventh column to say how long the backwash should be in seconds -- feedpump just say 1 so it will not stop unless you push something
configuration.pump = [1 5 1.8 1 0 1 20; %A Backwash
                      1 5 1 1 0 2 1];%B Feed
                  
names.pump = ["Backwash Pump";
              "Feed Pump"];    
        
%CONFIGURATION MASSFLOW
%first column is either 1 or 0 if the sensor is used or not
%the second column for the maximum massflow in l/min
configuration.mf = [1 5; %A5
                    1 5; %A6
                    0 0; %A7
                    0 0];%A8
                
names.mf = ["Backwash Mass Flow";
            "Permeate Mass Flow";
            "";
            ""];

%CONFIGURATION PRESSURE SENSORS
%first column is either 1 or 0 if the sensor is used or not
%second column for the maximum pressure in bar (Sick measures until 6 bar and the Gems pressure sensor until 10 bar)
%third column is the critical value you do not want to overshoot 
%fourth column is the pressure that is near to the critical value where you want to
%be notified by a warning
configuration.pressure = [1 6 6 6 ; %A1
                          1 6 6 6]; %A2
                          
names.pressure = ["Feed pressure";
                  "Permeatepressure"];
 
%Transmembrane pressure
%first input if you want the transmembrane pressure monitored or not
%second input for feed pressure 1 for A1, 2 for A2, 3 for A3
%third input for permeate pressure 1 for A1, 2 for A2, 3 for A3
%fourth input for the maximum transmembrane pressure
configuration.transmembrane = [1; %Do you need it or not?
                               1; %Feed
                               2; %Permeate
                               0.8]; %bar
               
names.ocvNO = "ocvNO D44"; %D44

names.ocvNC = "ocvNC D47"; %D47

names.cv = "cv D38"; %D38

%To say which ones are connected
configuration.ls = [1; % highest level switch of the UF Tank -1
                    1; % middle level switch of the UF Tank -2
                    1; % highest level switch of Feed -3
                    1; % middle level switch of Feed -4
                    1; % low level switch of Feed -5
                    1; % highest level switch of Purge -6
                    1];% middle level switch of Purge -7

names.ls = ["ls22"; %1
            "ls23"; %2
            "ls24"; %3
            "ls25"; %4
            "ls26"; %5
            "ls27"; %6
            "ls28"];%7

% Do you want to measure power? 1 for yes, 0 for no
measurePowerConsumption = 0;
          


%What you want your file to be named for the measurements
filename = 'Test_Dana.mat';


O = Interface(arduinoObj, arduinoUno, configuration, names, filename, measurePowerConsumption);

