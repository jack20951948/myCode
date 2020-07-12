#include <iostream>
#include <cstdlib>
#include <fstream>
#include <iomanip>
using namespace std;

int main() {
    fstream myFile;
    myFile.open("test1.dat", ios::in);
    if (myFile.good())
        cout << "File opened!" << endl;
    else
        cout << "Cannot open file!" << endl;
	myFile.open("test2.dat", ios::out);
    if (myFile.good())
        cout << "File opened!" << endl;
    else
        cout << "Cannot open file!" << endl;
 	myFile.open("test3.dat", ios::app); //append, in模式下不能用， out會從文末開始編輯
    if (myFile.good())
        cout << "File opened!" << endl;
    else
        cout << "Cannot open file!" << endl;
    myFile.open("test4.dat", ios::ate); //in模式定位到文件尾， out模式覆蓋
    if (myFile.good())
        cout << "File opened!" << endl;
    else
        cout << "Cannot open file!" << endl; 
		
		
	double sum=0, t; int count=0;
    ifstream in("dat6-3.txt", ios::in);
    if (!in) 
        cout << "Cannot open file!" << endl;
    while (in >> t) {
        sum += t;
        count++;
    }
    cout << "avg = " << sum/count << endl;
	
		
		   
    system("Pause");    
    return 0;
}

