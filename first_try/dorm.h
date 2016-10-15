#ifndef DORM_INCLUDED
#define DORM_INCLUDED

#include "lights.h"
#include "hvac.h"
#include "roomsensor.h"
#include "hallsensor.h"
#include "resident.h"

#include <vector>

class Dorm {

private:
	Lights lighting;
	HVAC hvac;
	std::vector<RoomSensor> room_sensors;
	std::vector<HallSensor> hall_sensors;
	std::vector<Resident> residents;

public:
	//  high and low points for dorm temp
	double temp_high;
	double temp_low;
	Floorplan floorplan;

	// constructor
	Dorm();

	// simulate a full day of lighting/energy consumption in the dorm
	int simulateDay();

	// track statistics
	trackMovement();
	trackEnergy();
	trackSatisfaction();

};

#endif