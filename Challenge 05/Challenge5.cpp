/*
	28/4/2020
	Made by Alejandro Pinel Martínez
  In quarentine
	Tuenti Challenge 10
	Challenge 5 - Tuentistic Numbers
*/

#include <iostream>
#include <fstream>
#include <vector>
#include "include/BigInteger.h"

using namespace std;

bool IsTuentisticable(BigInteger number) {
   return (number >= 60) || (number >= 40 && number <= 58) || (number >= 20 && number <= 29);
}

BigInteger Tuentistifation_Ultra(BigInteger number) {

   if (IsTuentisticable(number)){
      return number / 20;
   }
   else {
      return -1;
   }

   return number;
}

//Function to get the data if the file exits
bool GetData (string testfile, int & ncases, vector<BigInteger> & cases) {
   bool error = false;

   //Open the test file
   fstream inputfile;
   inputfile.open (testfile.c_str() , ios::in);

   //Check if the file exists
   if (inputfile.is_open()){

      inputfile >> ncases;

      cases = vector<BigInteger>(ncases);

      string data1;
      for (int i = 0; i < ncases; i++){
         inputfile >> data1;

         cases[i] = BigInteger(data1);
         data1 = cases[i];
      }

      inputfile.close();
   }
   else
      error = true;
   return error;
}

//Show the results on screen
string ShowResults (string results, int ncase) {
   if (results.compare("-1") == 0){
      results = "IMPOSSIBLE";
   }
    string stringresult = "Case #" + to_string(ncase + 1) + ": " + results + "\n";
    cout << stringresult;
    return stringresult;
}

//Write the results in a output file
void WriteResult(string filename, string result){
  ofstream file;
  file.open (filename);
  file << result;
  file.close();
}

int main () {

  bool isSubmit = true;
  bool writeFile = true;

  string INPUTFILENAME = "testInput";
  string OUTPUTFILENAME = "testOutput";

  if (isSubmit){
    INPUTFILENAME = "submitInput";
    OUTPUTFILENAME = "submitOutput";
  }

   int ncases;
   vector<BigInteger> cases;
   BigInteger result;

   //Get the data
   bool posible_error = GetData(INPUTFILENAME, ncases, cases);

   //If the data is correct
   if (!posible_error){

      BigInteger result;

      string resultstring;
      for (int i = 0; i < ncases; i++){
         result = Tuentistifation_Ultra(cases[i]);
         resultstring += ShowResults(result, i);
      }

      if (writeFile)
        WriteResult(OUTPUTFILENAME, resultstring);

   }
   else
      cout << "Test file is missing, the program can't do anything without it :(\n";

   return 0;
}
