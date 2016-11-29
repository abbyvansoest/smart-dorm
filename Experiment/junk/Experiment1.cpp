
int LEAVE_OFF = 0
int RENEW = 1

Experiment1::Experiment1() : Experiment1(0, "nope") {}

//  constructor 
Experiment1::Experiment1(string data, int renew) {

	if (data == "nope") {
		printf ("Provide a file");
		exit(EXIT_FAILURE);
	}

	this->datafile = data;
	this->contract_length = renew;
	this->active = false;
	this->sensors = ???

}

// select policy for each time period based on current activity
int Experiment1::selectPolicy(int cur_activity) {

	if (cur_activity == 0) {
		this->active = false;
		return LEAVE_OFF;
	}
	else if (cur_activity == 1) {
		this->active = true;
		return RENEW;
	}
}

string Experiment1::getTime(int timer) {
	int hour = timer / 60;
	int minutes = timer % 60;

	string s = toString(hour) + ":" + toString(minutes);
	return s;
}

// run full experiment on data
// parse through each line of the data, send to select policy 
void Experiment1::runExperiment() {

	ifstream datastream (this->datafile);
	if ( !datastream.is_open() ) {
    	// The file could not be opened
    	printf ("File unable to be opened");
		exit(EXIT_FAILURE);
	}
	else {

		int timer = 0;
		int num_mid_renew = 0;
		int num_turn_on = 0;
		int num_expired = 0;

		ofstream renew_in_middle("Experiment/renewed_existing.txt");
		ofstream turn_on_from_nothing("Experiment/renewed_new.txt");
		ofstream all_policy_actions("Experiment/selected_policies.txt");

		//  read in first line - has number of sensors being used
		int numSensors = int(datastream.readline());
		
		int[] timeInPolicy = new int[numSensors];

		//  for each line in the file (represents a minute), read in sensor information
		//  select a policy for each sensor
		//  update sensor-specifically
		string entry = datastream.readline();
		while (entry != "") {
			string t = getTime(timer);
			//  split entry by tab and convert to int array
			int[] entry_array = ???;

			// for each sensor
			for (int i = 0; i < numSensors; i++) {
				//  entry_array[i] = current activation status of sensor i
				//  policy = selected policy for sensor 
				//  time_left = time remaining in the contract for sensor i
				int policy = choosePolicy(entry_array[i]);
				int time_left = timeInPolicy[i];
				string action = "";

				if (policy == RENEW) {

					//  check if turning on or renewing in the middle of a contract
					if (time_left > 0) {
						num_mid_renew++;
						renew_in_middle << t + "\t time remaining was %d", time_left + "\n";
						action = "RENEWED";
					}

					//  or if turning on for the first time (from black out)
					else {
						num_turn_on++;
						turn_on_from_nothing << t + "\ttime remaining was %d", time_left + "\n";
						action = "TURNED ON";
					}
					time_left[i] = this->contract_length;
				}
				else if (policy == DO NOTHING) {
					// if  just expired
					if (time_left == 1) {
						num_expired++;
						action = "CONTRACT EXPIRED";
					}
					else if (time_left > 1) {
						action = "LIVING OUT CONTRACT";
					}
					else {
						action = "LEFT OFF";
					}
					//  decrement time left in i's contract if any time remains
					if (time_left > 0) timeInPolicy[i]--;
				}

				all_policy_actions << t + "\t" + action + "\n";

			}

			timer++;
		}

		renew_in_middle << num_mid_renew;
		renew_in_middle.close();
		turn_on_from_nothing << num_turn_on;
		turn_on_from_nothing.close();
		all_policy_actions << "number contracts renewed in middle: " + num_mid_renew;
		all_policy_actions << "number contracts created from nothing: " + num_turn_on;
		all_policy_actions << "number contracts expired: " + num_expired;


		all_policy_actions.close();
	}
}







