#include "dorm.h"

//  default constructor without arguments
Dorm::Dorm() {
	this->temp_low = 50;
	this->temp_high = 80;
}

//  constructor with arguments provided
Dorm::Dorm(double low, double high, char* filename) {
	this->temp_low = low;
	this->temp_high = high;
	this->floorplan = Floorplan(filename);

	//  set of lights, HVAC, and sensors
	Lights lighting = Lights();
	HVAC hvac = HVAC();
	std::vector<RoomSensor> room_sensors;
	std::vector<HallSensor> hall_sensors;
	std::vector<Resident> residents;

}

//  simulate a full day in the dorm
int simulateDay() {

	while (!stop) {

		//  get time of day (???)

		//  based on time of day, move individuals according to statistically discovered pattenrs
			// percent of people moving, probability distribution of where they are moving, etc.
			//  based on current positions, other stats, learn to predict where a person will go
		
		// 	as movement happens, sensors are activated and updated 
			//  if a person's location comes into contact with a sensor, sensor is updated
			//  occupancy, timestamp, etc

		Location res_loc;
		HallSensor activate;
		int atDest = 0;

		while (atDest < totalResidents) {

			for (auto it->residents.begin(), it != residents.end(); ++it) {
				
				//  find resident location if not in room
				res_loc = it->getLoc();
				activate = activateSensors(res_loc, hall_sensors);
				// lighitng and hvac should automatically update after 
			}

			//  step residents towards destination
			stepResidents();
			//  if they reach the destination, update tracker variable
			atDest++;

		}

		//  continue until the day is complete
		if (cur_time >= end_time) stop = true;

	}

}

/* */ 
int main(void) {

}

