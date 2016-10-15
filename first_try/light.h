#ifndef LIGHTS_INCLUDED
#define LIGHTS_INCLUDED

#include "roomsensor.h"
#include "hallsensor.h"

class Lights {

private:
	double cur_wattage;

	brighten();
	dim();

public:
	// constructor
	Lights();

	// adjust lighting based on sensor input data 
	adjust();

};

#endif