#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CPsn //base class
{
	string name; char sex;
    public:
        CPsn(string sname, char s) {
            name = sname; sex = s;
        }
        ~CPsn() {}
        string GetName() { return name; }
        char GetSex() { return sex; }
};

class CStu : public CPsn {
    int age; string addr;
    public:
        CStu(string sname, char s, int a, string ad) : CPsn(sname, s)  {
            age=a; addr=ad;
        }
        void ShowCStu() {
            cout << "name=" << GetName() << endl;
            cout << "sex=" << GetSex() << endl;
            cout << "age=" << age << endl;
            cout << "address=" << addr << endl;
        }
        ~CStu(){}
};

int main() {
    CStu s1("Bob",'M',20,"123 Ave A, NY");
    CStu s2("Jan",'F',18,"101 Ave Q, AZ");
    s1.ShowCStu();
    s2.ShowCStu();

    system("pause");
    return 0;
}