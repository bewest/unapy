You've got all needed scripts for your first test with data transfer via GPRS

How to install the python software "http-connect" to your module

1.) Open the file "konfig.dat" with a normal editor like Wordpad or similar and modify the data and save.
    NOTE: The file MUST be named "konfig.dat"

2.) Upload the files with any ordinary terminal software
	FUNC.pyo
	CONFIG.pyo
	main.pyo
	konfig.dat
     
    to your modem. 

3.) Activate the start file with #ESCRIPT: "main.pyo"<cr>

4.) Set the terminal to autostart with AT#STARTMODESCR=1,10<cr>

5.) After this make a power reset and listen to the serial output

6.) All data (ASCII) which received on this port will be transmitted to the server
    NOTE: The size of the input buffer is 4000 bytes max!


Function of the LEDs:
status LED = show the status from netwerk (flashing short means the module is registrated
PWR LED    = show the data status (flashing short waiting for input data, permanet ON transmit data to server.

