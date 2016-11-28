
int DO_NOTHING = 0
int RENEW = 1

Experiment1::Experiment1() : Experiment1(0, "nope") {}

//  constructor 
Experiment1::Experiment1(int renew, string data) {

	if (data == "nope") {
		printf ("Provide a file");
		exit(EXIT_FAILURE);
	}
	this->datafile = data;
	this->renewal = renew;
	this->active = false;

}

// select policy for each time period based on current activity
Experiment1::selectPolicy(int cur_activity) {

	if (cur_activity == 0) {
		this->active = false;
		return DO_NOTHING
	}
	else if (cur_activity == 1) {
		this->active = true;
		return RENEW
	}
}

// run full experiment on data
// parse through each line of the data, send to select policy 
Experiment1::runExperiment() {

	ifstream datastream (this->datafile);
	if ( !datastream.is_open() ) {
    	// The file could not be opened
    	printf ("File unable to be opened");
		exit(EXIT_FAILURE);
	}
	else {
	  // Safely use the file stream
	}


}

