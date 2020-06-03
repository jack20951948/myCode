#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CBase
{
    // private:
        double x;
    protected:
        int GetX() { return x; }
    public:
        void SetX(double a) { x = a; }
        void ShowX() { cout << x << endl; }
};

class CDerived: protected CBase {
    double y; // its own private member
    // protected:
        // inherit all public/protected in CBase as protected in CDerived
    public:
        void SetY(double b) { y = b; }
        // visit protected member GetX() in CBase
        void SetY() { y = GetX(); }
        void ShowY() { cout << y << endl; }
};

int main()
{
    CDerived cd;

    cd.SetX(15);  //what happen? Try to comment this line
    // SetX() is inherited as protected in CDerived; cannot be accessed by objects
    cd.SetY(20);

    cd.ShowX();   // what happen? Try to comment this line
    // ShowX() is inherited as protected in CDerived; cannot be accessed by objects
    cd.ShowY();

    system("pause");
    return 0;
}