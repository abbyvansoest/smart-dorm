
//  main program to run full set of experiments
//  for baseline high (length = infinity), low(length = 0), contract renewal (length = variable)
int choosePolicy(int length) {


}
// //  for experiments 2 -- data is array of historical sensor info  
// int choosePolicy(int[] data) {

// }
// // for experiment 3 -- data is matrix of historical info for multiple sensors
// //  (run experiment 2 policy choice on each sensor, select from pool based on freq 
// // and uniformity of selections - if highly contrasted what to do?)
// int choosePolicy(int[][] data) {

// }


// main calls proper execution method which moves through data and handles it properly
void executeBaseline(string filename) {

	//  call first choosePolicy method with a length of 0 and infinity
	

}
void execute1(string filename) {

	//  call first choosePolicy method with a variable length

}
// void execute2(string filename) {

// 	//  call second choosePolicy method with historical data of variable lengths

// }
// void execute3(string filename) {

// 	//  call third choosePolicy method with a accumulated set of data from multiple sensors

// }

// based on experiment number, call proper execution file 
int main(int argc, char *argv[]) {

	using namespace std;

	int exp_number = argv[1]
	string filename = argv[2]

	if (exp_number == 0) {
		executeBaseline(filename);
	}
	if (exp_number == 1) {
		execute1(filename);
	}
	if (exp_number == 2) {
		execute2(filename);
	}
	if (exp_number == 3) {
		execute3(filename);
	}

} 