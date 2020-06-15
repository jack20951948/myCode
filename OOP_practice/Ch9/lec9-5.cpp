#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;
// case 1: w/o parameters
class A {   
	public: 
		virtual void ShowFun() { //virtual
			cout << "A::ShowFun()" << endl; 
		}
		//for Q1: uncomment below
		//virtual void ShowFun(int i) { //virtual
		//    cout << "A::ShowFun()" << endl; 
		//}
};

class C : public A {   
	public: 
		void ShowFun(int i) { //not virtual => because not the same parameter 
			cout << "C::ShowFun()" << endl; 
		}
};

// case 2: w/ parameters
class B {  //case 2
	public: 
		virtual void ShowFun(char c) {
			cout << "B::ShowFun()" << endl; 
		} 
};

class D : public B {   
	public: 
		void ShowFun(int i) { //not virtual => because not the same parameter 
			cout << "D::ShowFun()" << endl; 
		} 
};

int main() 
{
	cout << "case 1:" << endl;
	//case 1
 	C c;
    A *pa = &c, &ra = c, a = c;
    a.ShowFun();
    pa->ShowFun(); 
    ra.ShowFun(); 
    //Q1: what if feeding a integer parameter?? what happenes? remeber to uncomment code in A
	//a.ShowFun(1);	
    //pa->ShowFun(2); 
    //ra.ShowFun(3); 
    
    
	cout << "case 2:" << endl;
	//case2
	D d;
    B *pb = &d, &rb = d, b = d;
    b.ShowFun(0);
    pb->ShowFun(0); 
    rb.ShowFun(0); 
	
	system("pause");
    return 0;	
}
