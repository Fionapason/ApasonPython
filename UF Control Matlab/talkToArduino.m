classdef talkToArduino
    
    properties (GetAccess = public, SetAccess = private)
        
        arduinoObj
        
        comPort
        
        baudRate = 115200;
        
        analogReference = 5.0;
        
    end
    
   
    methods
        
        function O = talkToArduino(comPort)
            if nargin<1
                error('Indicate the com port as first argument');
            end
            O.comPort = comPort;
            
            %to find the correct serialport name, go to the command line and type
            %"serialportlist("available")"
            %On Mac this will look like "/dev/tty.usb..." or "/dev/cu.usb..."
            %On Windows this will look like "COM..."
            
            disp(['Connecting to Arduino on ',O.comPort]);
            
            O.arduinoObj = serialport(O.comPort, O.baudRate);
            
            flush(O.arduinoObj);
            
            assert(isequal(read(O.arduinoObj,1,"char"), 'a'));
            
            write(O.arduinoObj,'a', "char")
            
            assert(isequal(read(O.arduinoObj,1,"char"), '+'));
            
            flush(O.arduinoObj);
            
            write(O.arduinoObj, '+', "char")
            assert(isequal(read(O.arduinoObj,1,"char"), 'a'));
            flush(O.arduinoObj);
            
            
            write(O.arduinoObj, ';', "char")
            assert(isequal(read(O.arduinoObj,1,"char"), '-'));
            flush(O.arduinoObj);
            
            disp('Successfully connected');
            
        end % end constructor
        
        
        function reply = sendCommand(O,command)
            
            write(O.arduinoObj, command , "char");

            reply = str2double(readline(O.arduinoObj));
            
            flush(O.arduinoObj);

        end %end reading
        
        function valveSendCommand(O,command)
            
            write(O.arduinoObj, command , "char");
            
            flush(O.arduinoObj);

        end %end reading
        
        function writeCommand(O, command, value)
            
            %First write the command and then write the value you want to
            %set it to
            write(O.arduinoObj, command , "char");
            pause(0.1)
            write(O.arduinoObj, value, 'string');
            pause(0.1);
            
%           assert(isequal(read(O.arduinoObj, 1, "char"), '+'));
            
            flush(O.arduinoObj);
            
            flush(O.arduinoObj);
            
        end %end writing
        
        function flushing(O)
            flush(O.arduinoObj);
        end
        
        function delete(O)
           delete(O.arduinoObj); 
        end
              
    end % end methods
 
end % end classdef

