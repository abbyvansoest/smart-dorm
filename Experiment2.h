#ifndef EXP2_INCLUDED
#define EXP2_INCLUDED

#include <stdio.h>   
#include <stdlib.h> 
#include <fstream>
#include <iostream>

using std::string;

class Experiment2
{

private:
	string datafile;
	int* history
	int hist_length;
	int renewal;
	bool active;

public:

	// constructors
	Experiment2();
	Experiment2(string, int);
	~Experiment2();

	// methods
	int classifyHistory();
	int selectPolicy(int);  // select policy for each time period based on current activity
	void runExperiment();   // run full experiment on data

};

#endif