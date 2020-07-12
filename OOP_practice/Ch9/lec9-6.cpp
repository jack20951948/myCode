#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class B { 
    public:   
        void f() { cout << "Bf "; }
        virtual void g() { cout << "Bg "; }
        void h() { g(); f(); }
        virtual void m() { g();  f(); }        
};
class D : public B { 
    public:
        void f() { cout << "Df "; }
        void g() { cout << "Dg "; }
        void h() { f(); g(); }                
};

int main() 
{
 	D d; 
	B *pB = &d;
    pB->f(); 
	pB->g(); 
	pB->h(); 
	pB->m();
    
	system("pause");
    return 0;	
}