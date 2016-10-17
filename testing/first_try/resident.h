#ifndef RES_INCLUDED
#define RES_INCLUDED

#include "lights.h"
#include "hvac.h"
#include "roomsensor.h"
#include "hallsensor.h"
#include "resident.h"

#include <vector>

class Resident {

private:
	RoomSensor room;
	double temp_pref;
	Location loc;
	Destination dest;
	bool atDest;

public:

	// constructor
	Resident();

	//  return an int based on if the resident is too cold, hot, or neutral
	int isHappy();

};

#endif