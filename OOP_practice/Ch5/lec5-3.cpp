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
        void input();
        const CComplex operator+(CComplex&);
        // Q1: what is? CComplex operator+(CComplex&);
        // CComplex operator+(CComplex&);
        // friend const CComplex operator+(CComplex & o1, CComplex & o2);
};

void CComplex::input(){
  	cout << "input real="; cin >> real;
   	cout << "input imag="; cin >> imag;
} 

//overloading + as a member function
const CComplex CComplex::operator+( CComplex& o2 ){  
// Q1: what is? CComplex CComplex::operator+( CComplex& o2 ){  
// CComplex CComplex::operator+( CComplex& o2 ){  
	return CComplex(real+o2.real, imag+o2.imag);
}

// // overloading + as a friend function
// const CComplex operator+(CComplex & o1, CComplex & o2) {
//     CComplex c; 
// 	c.real=o1.real+o2.real;
//     c.imag=o1.imag+o2.imag; 
// 	return c;
// }

int main() { 
    CComplex c1(3,4), c2(2,-7);
	cout << "c1 = "; c1.display();
    cout << "c2 = "; c2.display();
    
	CComplex c3 = c1+c2;
    cout << "c1+c2 = "; c3.display();
    cout << "c1 = "; c1.display();
    
    CComplex t3 = (c1 + c2);
    cout << "t3(before input) = "; t3.display();
	t3.input();
	// Q1: what is? (c1+c2).input();
    // (c1+c2).input();
    cout << "t3(after input) = "; t3.display();
    
	system("Pause");
    return 0;
}

