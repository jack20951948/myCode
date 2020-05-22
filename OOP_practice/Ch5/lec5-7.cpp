#include <cstdlib>
#include <iostream>
#include <cstring>
using namespace std;

class CStr
{
    private:
        char * line;
    public:    
        CStr() { ; } //A
        //CStr() { line = NULL; } //A
        CStr(char* cline) { 
            line = new char [strlen(cline)+1];
            strcpy(line, cline); 
        } //B
        ~CStr() {
            if (line) delete [] line;
            line = NULL;
            cout << "clean up CStr object!" << endl;  
        }
        
        //overloading [] as a member function
        char& operator[](int i);
};

char& CStr::operator[](int i) {
	if (i>=strlen(line)) { 
        cerr << "Error: " << i << " is out of bound!!!"; 
    }
    return line[i];
};


int main() {//Program prog3-2
	CStr one("lec5-7"); //call constructor   
    cout << one[3] << endl; //what happens?
    cout << one[8] << endl; //what happens?
    
	system("Pause");
	return 0;
}




