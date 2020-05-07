/*
	27/4/2020
	Made by Alejandro Pinel Martínez
  In quarentine
	Tuenti Challenge 10
	Challenge 3 - Fortunata and Jacinta
*/

#include <iostream>
#include <fstream>
#include <wchar.h>
#include <locale.h>
#include <stdlib.h>
#include <vector>
#include <list>
#include <map>
#include <set>
#include <algorithm>
#include <stdlib.h>
#include <cctype>
#include <Windows.h>
#include "UTF8/utf8.h"
#include <sstream>

using namespace std;

//Write the results in a output file
void WriteResult(string filename, string result){
  ofstream file;
  file.open (filename);
  file << result;
  file.close();
}

struct WordInfo {
   string word;
   int frecuency;
   int rank;

   WordInfo(string w, int f, int r){
      word = w;
      frecuency = f;
      rank = r;
   }
};

bool WordSort(pair<int, string> w1, pair<int, string> w2) {
   if (w1.first != w2.first){
      return w1.first > w2.first;
   }
   else{
      return w1.second < w2.second;
   }
}

class Book{
private:
   struct Rank{
      int frecuency;
      int rank;

      Rank(){
         frecuency = rank = 0;
      }
   };

   //Map words with frecuencies and ranking
   map<string, Rank> dict;
   //Vector with frecuencies and the word
   vector<pair<int, string>> ranking;

public:

   void AddWord(string word){
      dict[word].frecuency = dict[word].frecuency + 1;
   }

   void Compile(){
      int nelem = dict.size();
      ranking = vector<pair<int, string>>(nelem);
      map<string, Rank>::iterator word = dict.begin();
      for (int i = 0; i < nelem && word != dict.end(); i++){
         ranking[i].first = (*word).second.frecuency;
         ranking[i].second = (*word).first;
         word++;
      }

      sort(ranking.begin(), ranking.end(), WordSort);

      for (int i = 0; i < nelem; i++){
         dict[ranking[i].second].rank = i;
      }

      //WriteResult("dictionary", AllDictionary());
      //cout << AllDictionary();
   }

   WordInfo GetInfo(string w){
      return WordInfo(w, dict[w].frecuency, dict[w].rank + 1);
   }

   WordInfo GetInfo(int r){
      return WordInfo(ranking[r].second, ranking[r].first, r);
   }

   string AllDictionary(){
      string res;
      for (unsigned int i = 0; i < ranking.size(); i++){
         res = res + to_string(i + 1) + ": " + ranking[i].second + " - " + to_string(ranking[i].first) + "\n";
      }
      return res;
   }
};

Book BOOK;

class Search {
private:
   string tosearch;

   int IsANumber(string s){
      char * p;
      int number = strtol(s.c_str(), &p, 10);

      if (*p != 0) {
         return -1;
      }
      else{
         return number;
      }
   }

public:
   void Initialize(string word){
      tosearch = word;
   }

   string GetInfo(){
      int n = IsANumber(tosearch);
      string s;

      //It is a word
      if (n == -1){
         WordInfo w = BOOK.GetInfo(tosearch);
         s = to_string(w.frecuency) + " #" + to_string(w.rank);
      }
      //It is a number
      else{
         WordInfo w = BOOK.GetInfo(n - 1);
         s = w.word + " " + to_string(w.frecuency);
      }

      return s;
   }
};

vector<string> validchar {"a", "b" , "c", "d", "e", "f", "g", "h", "i", "j",
   "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w",
   "x", "y", "z", "á", "é", "í", "ó", "ú", "ü"};

vector<string> change1 {"Á", "É", "Í", "Ó", "Ú", "Ü", "Ñ"};
vector<string> change2 {"á", "é", "í", "ó", "ú", "ü", "ñ"};


string TransformChar(string s){
   std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c){ return std::tolower(c); });

   bool changed = false;
   for (size_t i = 0; i < change1.size() && !changed; i++){
      if (s.compare(change1[i]) == 0) {
         s = change2[i];
         changed = true;
      }
   }

   bool correct = false;
   for (size_t i = 0; i < validchar.size() && !correct; i++){
      if (s.compare(validchar[i]) == 0)
         correct = true;
   }

   if (!correct){
      s = " ";
   }

   return s;
}

void GetChars(string s, vector<string> & chars){
   char* str = (char*)s.c_str();    // utf-8 string
   char* str_i = str;                  // string iterator
   char* end = str+strlen(str)+1;      // end iterator

   while (str_i < end)
   {
      uint32_t code = utf8::next(str_i, end); // get 32 bit code of a utf-8 symbol
      if (code == 0)
         continue;

      char symbol[5]  = {0,0,0,0,0};
      utf8::append(code, symbol); // initialize array `symbol`
      string thechar(symbol);

      chars.push_back(thechar);
   }
}

//Function to get the data if the file exits
bool GetData (string bookfilename, string testfile, int & ncases, vector<Search> & cases) {
   bool error = false;

   //Open the test file
   fstream bookfile;
   bookfile.open (bookfilename.c_str() , ios::in);

   //Check if the file exists
   if (bookfile.is_open()){

      string word = "";
      int wordsize = 0;
      string finalchar;
      string line;
      // For every line
      while (getline(bookfile, line)) {

         std::vector<string> chars;
         GetChars(line, chars);

         //For every char
         for (unsigned int i = 0; i < chars.size(); i++){
            finalchar = TransformChar(chars[i]);

            if (finalchar != " "){
               word = word + finalchar;
               wordsize++;
            }
            else{
               if (word != "" && wordsize > 2) {
                  BOOK.AddWord(word);
               }
               word = "";
               wordsize = 0;
            }
         }

         if (word != "" && wordsize > 2) {
            BOOK.AddWord(word);
         }
         word = "";
         wordsize = 0;
      }

      bookfile.close();
      BOOK.Compile();
   }
   else
      error = true;

   //Open the test file
   fstream inputfile;
   inputfile.open (testfile.c_str() , ios::in);

   //Check if the file exists
   if (inputfile.is_open() && !error){
      inputfile >> ncases;
      cases = vector<Search>(ncases);
      string word;
      for (int i = 0; i < ncases; i++){
         inputfile >> word;
         cases[i].Initialize(word);
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



int main () {
  bool isSubmit = true;
  bool writeFile = true;

  SetConsoleOutputCP( CP_UTF8 );

  string BOOKFILENAME = "pg17013.txt";
  //string BOOKFILENAME = "minibook";

  string INPUTFILENAME = "testInput";
  string OUTPUTFILENAME = "testOutput";

  if (isSubmit){
    INPUTFILENAME = "submitInput";
    OUTPUTFILENAME = "submitOutput";
  }

   int ncases;
   vector<Search> cases;

   //Get the data
   bool posible_error = GetData(BOOKFILENAME, INPUTFILENAME, ncases, cases);

   //If the data is correct
   if (!posible_error){
      string result;

      string resultstring = "";
      for (int i = 0; i < ncases; i++){
         result = cases[i].GetInfo();
         resultstring += ShowResults(result, i);
      }

      if (writeFile)
        WriteResult(OUTPUTFILENAME, resultstring);
   }
   else
      cout << "Test file is missing, the program can't do anything without it :(\n";

   return 0;
}
