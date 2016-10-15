#include "resident.h"

//  default constructor without arguments
Resident::Resident() {
	this->room = null;
	this->temp_pref = 68;
	this->loc = Location(0, 0);
	this->dest = 0;
}

//  constructor with arguments provided
Resident::Resident(RoomSensor r, double t) {
	this->room = r;
	this->temp_pref = t;
	this->loc = this->room.getLocation();
	this->dest = 0;//////////////// need to think
	this->atDest;

}