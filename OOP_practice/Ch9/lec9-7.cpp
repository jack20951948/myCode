#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class A { 
    public:   
        ~A() { cout << "A::~A()\n"; }        
};

class C : public A { 
    int * iary;
    public:
        C(int i) { iary = new int [i]; }
        ~C() { 
            delete [] iary;
            cout << "C::~C()\n";  }                
};

class B { 
    public:   
        virtual ~B() { cout << "B::~B()\n"; }        
};

class D : public B { 
    int * iary;
    public:
        D(int i) { iary = new int [i]; }
        ~D() { 
            delete [] iary;
            cout << "D::~D()\n";  }                
};

int main() 
{
	cout << "case 1:" << endl;
 	A *pa = new C(10);
    delete pa;
	
	cout << "case 2:" << endl;
	B *pB = new D(10);
    delete pB;
	
	system("pause");
    return 0;	
}