close all;
clear;
clc;

%Look in your arduino IDE which port you are connected to
arduinoObj = talkToArduino('COM8');

%CONFIGURATION PUMP
%first column with 1 or 0 if it is used for a pump or not
%second column for maximum Volt input
%third column for desired massflow in l/min !!!!
%fourth column for the Kp constant
%fifth column for the Ki constant
%sixth column to say which massflow sensor to control, 1 for A5, 2 for A6, 3 for A7, 4 for A8   
%seventh column to say how long the backwash should be in seconds -- feedpump just say 1 so it will not stop unless you push something
configuration.pump = [1 5 4 5 0 1 20; %A Backwash
                      1 5 5 5 0.01 2 1];%B Feed
                  
names.pump = ["Backwash Pump";
              "Feed Pump"];    

%CONFIGURATION pcvs
%matrix with 4 rows (A,B,C or D) and two columns
%first column with 1 or 0 if it is used for a pcv or not
%second column for desired begin input voltage (between 0.5 and 5)
%third column for desired massflow
%fourth column for the Kp constant
%fifth column for the Ki constant
%sixth column to say which pressure sensor will be used as the "control
%value", 1 for A5, 2 for A6, 3 for A7, 4 for A8
configuration.pcv = [0 0.6 3.3 0.6 0 1; %D
                     1 3 1.15 1 0 2];%C

names.pcv = ["pcv D";
             "pcv C"];
        
%CONFIGURATION MASSFLOW
%first column is either 1 or 0 if the sensor is used or not
%the second column for the maximum massflow in l/min
configuration.mf = [1 5; %A5
                    1 10; %A6
                    0 5; %A7
                    0 10];%A8
                
names.mf = ["Backwash Mass Flow";
            "Feed Mass Flow";
            "Feed Mass Flow Test";
            "Permeate Mass Flow"];

%CONFIGURATION PRESSURE SENSORS
%first column is either 1 or 0 if the sensor is used or not
%second column for the maximum pressure in bar (Sick measures until 6 bar and the Gems pressure sensor until 10 bar)
%third column is the critical value you do not want to overshoot 
%fourth column is the pressure that is near to the critical value where you want to
%be notified by a warning
configuration.pressure = [1 6 6 6 ; %A1
                          1 6 6 6; %A2
                          1 6 6 6]; %A3
                          
names.pressure = ["Feed pressure";
                  "Retentate pressure";
                  "Permeate pressure"];
 
%Transmembrane pressure
%first input if you want the transmembrane pressure monitored or not
%second input for feed pressure 1 for A1, 2 for A2, 3 for A3
%third input for permeate pressure 1 for A1, 2 for A2, 3 for A3
%fourth input for the maximum transmembrane pressure
configuration.transmembrane = [1; %Do you need it or not?
                               1; %Feed
                               3; %Permeate
                               0.85]; %bar
               
names.ocvNO = "ocvNO D44"; %D44

names.ocvNC = "ocvNC D47"; %D47

names.cv = "cv D38"; %D38
          


%What you want your file to be named for the measurements
filename = 'Test_Dana_02.05.22_1.mat';


O = Interface(arduinoObj, configuration, names, filename);

