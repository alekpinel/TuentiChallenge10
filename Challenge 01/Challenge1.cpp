/*
	27/4/2020
	Made by Alejandro Pinel Martínez
  In quarentine
	Tuenti Challenge 10
	Challenge 1 - Rock, Paper, Scissors
*/

#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Game {
private:
  int Player1;
  int Player2;

public:

   void Initialize(char data1, char data2) {
      Player1 = IntOfMove(data1);
      Player2 = IntOfMove(data2);
   }

   char Play() {
      if (Player1 == Player2){
        return '-';
      }
      else {
        int sum = Player1 + Player2;
        if (sum == 1)
          return 'R';
        else if (sum == 2)
          return 'P';
        else if (sum == 3)
          return 'S';
      }
      return 'E';
   }

private:
  int IntOfMove(char move) {
     if (move == 'R')
      return 0;
     else if (move == 'S')
      return 1;
     else if (move == 'P')
      return 2;
     else
      return -1;
  }
};

//Function to get the data if the file exits
bool GetData (string testfile, int & ncases, vector<Game> & cases) {
   bool error = false;

   //Open the test file
   fstream inputfile;
   inputfile.open (testfile.c_str() , ios::in);

   //Check if the file exists
   if (inputfile.is_open()){

      inputfile >> ncases;

      cases = vector<Game>(ncases);

      char data1, data2;
      for (int i = 0; i < ncases; i++){
         inputfile >> data1;
         inputfile >> data2;

         cases[i].Initialize(data1, data2);
      }

      inputfile.close();
   }
   else
      error = true;

   return error;
}

//Show the results on screen
string ShowResults (string results, int ncase) {
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
   vector<Game> cases;

   //Get the data
   bool posible_error = GetData(INPUTFILENAME, ncases, cases);

   //If the data is correct
   if (!posible_error){
      char result;

      string resultstring;
      for (int i = 0; i < ncases; i++){
         result = cases[i].Play();
         resultstring += ShowResults(string(1, result), i);
      }

      if (writeFile)
        WriteResult(OUTPUTFILENAME, resultstring);
   }
   else
      cout << "Test file is missing, the program can't do anything without it :(\n";

   return 0;
}
