#ifndef ROOMSENSOR_INCLUDED
#define ROOMSENSOR_INCLUDED

#include "lights.h"
#include "hvac.h"

#include <vector>

class RoomSensor {

private:
	// location
	Location loc;
	//  current dorm temp
	double cur_temp;
	//  inhabitant preferred temp
	double temp_pref;
	//  is the room currently occupied?
	bool occupied;


public:
	// constructor
	RoomSensor();


};

#endif