
#ifndef HVAC_INCLUDED
#define HVAC_INCLUDED

#include "roomsensor.h"
#include "hallsensor.h"

class HVAC {

private:
	double max_temp;
	double min_temp;

	double adj_rate;

	double energy_usage;
	heat();
	cool();

public:

	// constructor
	HVAC();

	// adjust heating/cooling based on sensor input data 
	adjust();



};

#endif