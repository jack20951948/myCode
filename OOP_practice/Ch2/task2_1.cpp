#include<fstream>
#include<iostream>
#include<string>

using namespace std;

int main(int argc, char *argv[])
{
    string s;

    ifstream inf(argv[1]);
    ofstream outf(argv[2]);

    while (getline(inf, s))
    {
        outf << s << '\n';               
        cout << s << endl << endl;           
    }                            

    inf.close();
    outf.close();
    return 0;
}