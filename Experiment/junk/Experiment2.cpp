int HIGH = 0; 
int LOW = 1;
int INCREASING = 2; 
int DECRESING = 3;

// constructors
Experiment2() : Experiment2() {}

Experiment2(string data, int length) {

	this->datafile = data;
	this->hist_length = length;
	this->history = new int[this->hist_length];

}

~Experiment2() {
	delete []this->history;
}

// methods
int Experiment2::classifyHistory(int cur_status) {
	int classified = -1;

	//  have prepared classifier parameter files for 5, 10, 15, 20, 30
	//  need to have done training before 
	//  call based on the length of history desired

	return classified;
}

// select policy for each time period based on current activity and history
int Experiment2::selectPolicy(int current) {

	int classify = this->classifyHistory(current);


	if (classify == HIGH) {

	}
	else if (classify == LOW) {

	}
	else if (classify == INCREASING) {

	}
	else if (classify == DECRESING) {

	}

}

// run full experiment on data
void Experiment2::runExperiment() {


}


int main(int argc, int** argv) {

}

