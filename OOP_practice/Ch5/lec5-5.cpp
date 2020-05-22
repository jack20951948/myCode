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
        void display() { cout << "(" << real
            << "," << imag << "i)" << endl; }
        //overloading various opetors     
        CComplex operator+(CComplex& o2); //for o1+o2
        CComplex operator+(double r);    //for o1+x
        void operator+=(CComplex& o2);    //for o1+=o2
        friend CComplex operator+(       //for x+o1   
                        double r, CComplex& o1);
        friend CComplex operator-(       //for o2=-o1
                        CComplex& o1);
};

//overloading as member functions
CComplex CComplex::operator+(CComplex& o2) {
    CComplex t; 
	t.real=real+o2.real;
    t.imag=imag+o2.imag; 
	return t; 
} 

CComplex CComplex::operator+(double r) {
    CComplex t; 
	t.real=real+r;
    t.imag=imag; 
	return t; 
}
 
void CComplex::operator+=(CComplex& o2) {
    real+=o2.real; imag+=o2.imag; 
} 

//overloading as friend functions
CComplex operator+(double r, CComplex& o1) {
    CComplex o2; 
	o2.real=r+o1.real;
    o2.imag=o1.imag; 
	return o2; 
}

CComplex operator-(CComplex& o1) {
    return CComplex(-o1.real,-o1.imag);
}

int main() {
    CComplex c1(12,-20), c2(-5, 9), c3;
    c3=c1+c2; c3.display();
    c3=c1+10; c3.display();
    c3=-8+c2; c3.display();
    c2+=c1;   c2.display();
    c1=-c3;   c1.display();
    
    system("Pause");
    return 0;
}

