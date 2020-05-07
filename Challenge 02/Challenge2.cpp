/*
	27/4/2020
	Made by Alejandro Pinel Martínez
  In quarentine
	Tuenti Challenge 10
	Challenge 2 - The Lucky One
*/

#include <iostream>
#include <fstream>
#include <vector>
#include <list>

using namespace std;

class Tournament {
private:
  struct Match{
    int Player1, Player2;
    int result;
    Match(int p1, int p2, int r){
      Player1 = p1;
      Player2 = p2;
      result = r;
    }
    int Loser(){
      if (result == 0){
        return Player1;
      }
      else{
        return Player2;
      }
    }
  };

list<Match> matches;
vector<bool> players;
int nplayers;

public:

   Tournament() {
     nplayers = 0;
   }

   void AddMatch(int p1, int p2, int r) {
     matches.push_back(Match(p1 - 1, p2 - 1, r));
     if (p1 > nplayers){
       nplayers = p1;
     }
     if (p2 > nplayers){
       nplayers = p2;
     }
   }

   int BestPlayer(){
     players = vector<bool>(nplayers, true);

     for (list<Match>::iterator i = matches.begin(); i != matches.end(); i++){
       players[(*i).Loser()] = false;
     }

     int bestone = -1;
     for (int i = 0; i < nplayers && bestone == -1; i++){
       if (players[i])
        bestone = i;
     }

     return bestone + 1;
   }
};

//Function to get the data if the file exits
bool GetData (string testfile, int & ncases, vector<Tournament> & cases) {
   bool error = false;

   //Open the test file
   fstream inputfile;
   inputfile.open (testfile.c_str() , ios::in);

   //Check if the file exists
   if (inputfile.is_open()){

      inputfile >> ncases;

      cases = vector<Tournament>(ncases);

      int nmatches, p1, p2, r;
      for (int i = 0; i < ncases; i++){
         inputfile >> nmatches;
         for (int j = 0; j < nmatches; j++){
           inputfile >> p1 >> p2 >> r;
           cases[i].AddMatch(p1, p2, r);
         }
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
   vector<Tournament> cases;

   //Get the data
   bool posible_error = GetData(INPUTFILENAME, ncases, cases);

   //If the data is correct
   if (!posible_error){
      int result;

      string resultstring;
      for (int i = 0; i < ncases; i++){
         result = cases[i].BestPlayer();
         resultstring += ShowResults(to_string(result), i);
      }

      if (writeFile)
        WriteResult(OUTPUTFILENAME, resultstring);
   }
   else
      cout << "Test file is missing, the program can't do anything without it :(\n";

   return 0;
}
