#ifndef EXP1_INCLUDED
#define EXP1_INCLUDED

#include <stdio.h>   
#include <stdlib.h> 
#include <fstream>
#include <iostream>

using std::string;

class Experiment1
{

private:
	string datafile;
	int contract_length;
	bool active;

	string getTime(int);

public:

	// constructors
	Experiment1();
	Experiment1(string, int);

	// methods
	int selectPolicy(int);  // select policy for each time period based on current activity
	void runExperiment();   // run full experiment on data

};

#endif