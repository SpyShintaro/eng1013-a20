"""
Over-height Exit Subsystem - Traffic Control Subsystem 3
Author: Abbey
Original Version Date: 23/04/2025
Version Number: 1.0
"""


from pymata4 import pymata4
import time

board = pymata4.Pymata4()

triggerPin = 3
echoPin = 2

greenLightPin = 13
yellowLightPin = 12
redLightPin = 11

Fl1 = 5
Fl2 = 6 

ldrPin = 1

board.set_pin_mode_sonar(triggerPin, echoPin, timeout=10000000)
board.set_pin_mode_digital_output(greenLightPin)
board.set_pin_mode_digital_output(yellowLightPin)
board.set_pin_mode_digital_output(redLightPin)
board.set_pin_mode_analog_input(ldrPin)
board.set_pin_mode_digital_output(Fl1)
board.set_pin_mode_digital_output(Fl2)	

print("CTRL+C to end program")

def find_light_type():
	
	resultLdr = board.analog_read(ldrPin)
	
	if resultLdr and 0 <= resultLdr[0] < 300:
		print("Night time detected")
		return "night"
	else:
		print("Day time detected")
		return "day"

def overheight_exit_subsystem():

	recentReadings = []
	tolerance = 5
	objectDetected = False

	try:
		while True:
			
			resultUs = board.sonar_read(triggerPin)
			
	#sensor is placed at a height of 4m, facing directly across road, so if overheight vehicle goes on road infront, it is detected
	#assume rooad is 4m wide, so 1:4 scale use

			if resultUs and 2 <= resultUs[0] <= 100:
				distance = resultUs[0]
				recentReadings.append(distance)
				
				if len(recentReadings) > 5:
					recentReadings.pop(0)

				if len(recentReadings) > 1 and abs(recentReadings[-1] - recentReadings[-2]) < tolerance:
					averageDistance = sum(recentReadings) / len(recentReadings)
					time.sleep(1)
					print(f"Average distance: {averageDistance:.2f} cm")
			
					if 2 <= averageDistance <= 100:
						if not objectDetected:
							print("Overheight vehicle detected")
							objectDetected = True
							
							lightType = find_light_type()

							if lightType == "night":
								board.digital_write(Fl1, 1)
								board.digital_write(Fl2, 1)	
							elif lightType == "day":
								board.digital_write(Fl1, 0)
								board.digital_write(Fl2, 0)
						
							board.digital_write(greenLightPin, 0)
							board.digital_write(yellowLightPin, 1)
							board.digital_write(redLightPin, 0)
							time.sleep(2)

							board.digital_write(greenLightPin, 1)
							board.digital_write(yellowLightPin, 0)
							board.digital_write(redLightPin, 0)
							time.sleep(5)

							while objectDetected:
								resultUs = board.sonar_read(triggerPin)
								if not resultUs or resultUs[0] > 100:
									print ("No object detected")	
									board.digital_write(Fl1, 0)
									board.digital_write(Fl2, 0)
									objectDetected = False
									break
								
								lightType = find_light_type()

								if lightType == "night":
									board.digital_write(Fl1, 1)
									board.digital_write(Fl2, 1)	
								elif lightType == "day":
									board.digital_write(Fl1, 0)
									board.digital_write(Fl2, 0)

								print("Object still detected")
								board.digital_write(greenLightPin, 1)
								board.digital_write(yellowLightPin, 0)
								board.digital_write(redLightPin, 0)
								time.sleep(1/2)

								board.digital_write(greenLightPin, 0)
								time.sleep(1/2)

				else: 
					time.sleep(1)
					print("Inconsistent readings, ignoring")

			else: 
				board.digital_write(greenLightPin, 0)
				board.digital_write(yellowLightPin, 0)
				board.digital_write(redLightPin, 1)
				time.sleep(1)
				print("No object detected")
		
								
	except KeyboardInterrupt:
		print("Ending program now...")
		board.digital_write(greenLightPin, 0)
		board.digital_write(yellowLightPin, 0)
		board.digital_write(redLightPin, 0)

		board.digital_write(Fl1, 0)
		board.digital_write(Fl2, 0)

		board.shutdown()



overheight_exit_subsystem()