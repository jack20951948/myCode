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
        const CComplex operator+(CComplex&);
        // overloading binary- as a member function
        const CComplex operator-(CComplex&);
        // overloading unary- as a member function
        const CComplex operator-();
        // // overloading unary- as a friend function
        // friend const CComplex operator-(CComplex&);
};

// overloading binary+ as a member function
const CComplex CComplex::operator+( CComplex& o2 ){  
	return CComplex(real+o2.real, imag+o2.imag);
}

// overloading binary- as a member function
const CComplex CComplex::operator-( CComplex& o2 ){  
	return CComplex(real-o2.real, imag-o2.imag);
}

// overloading unary- as a member function
const CComplex CComplex::operator-(){  
	return CComplex(-real, -imag);
}
// // overloading unary- as a friend function
// const CComplex operator-(CComplex& o1){  
// 	return CComplex(-o1.real, -o1.imag);
// }

int main() {  
    CComplex c1(3,4), c2(2,-7), c3;
    cout << "c1 = ";c1.display();
    cout << "c2 = ";c2.display();
    c3 = c1 - c2; // call binary operator-
    cout << "c3 = c1-c2 = "; c3.display();
    c3 = -c2;     // call unary operator-
    cout << "c3 = -c2 = "; c3.display();
    
	system("Pause");
    return 0;
}

