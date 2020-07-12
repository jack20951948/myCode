#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class B0 {   
    public: 
        void ShowFun() {                     //not virtual
            cout << "B0::ShowFun()" << endl;
        }
};

class C0 : public B0 {   
    public: 
        virtual void ShowFun() { //virtual
            cout << "C0::ShowFun()" << endl;
        } 
};

class C1 : public C0 {   
    public: 
        void ShowFun() { //virtual
            cout << "C1::ShowFun()" << endl;
        } 
};

class C2 : public C1 {   
    public: 
        void ShowFun() { //virtual
            cout << "C2::ShowFun()" << endl;
        } 
};

void FunPtr(C0 *ptr) {
    ptr->ShowFun();
}


int main() 
{
    B0 w, *p; C0 x, *q;
    C1 y; C2 z;
    p = &w; p->ShowFun();
    p = &y; p->ShowFun(); //Q1: what happen??
    q = &x; FunPtr(q);    //Q2: which to call? 
    q = &y; FunPtr(q);
    q = &z; FunPtr(q); 
	//q = &w; FunPtr(q);    //Q3: what happen??
	//FunPtr(&w); 			//Q4: what happen?? => cannot covert from B0* to C0*; but the reverse can
	//FunPtr(p);			//Q5: what happen?? => cannot covert from B0 to C0* ; but the reverse can
	
    system("pause");
    return 0;	
}
