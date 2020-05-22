#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CComplex {
    double real, imag;
    public:
        CComplex() { real=0; imag=0; }
        CComplex(double r, double i) { 
            real=r; imag=i; }
        CComplex cadd(CComplex & o2);
        void display() { cout << "(" << real
            << "," << imag << "i)" << endl; }
};

CComplex CComplex::cadd(CComplex & o2) {
    CComplex c; 
	c.real=real+o2.real;
    c.imag=imag+o2.imag; 
	return c;
}

int main() { 
    CComplex c1(3,4), c2(2,-7);
    cout << "c1 = "; c1.display();
    cout << "c2 = "; c2.display();
    
    CComplex c3 = c1.cadd(c2);
    cout << "c1+c2 = "; c3.display();
    
	system("Pause");
    return 0;
}

