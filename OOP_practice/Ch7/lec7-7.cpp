#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class B0
{		
public: 
	void Show() { 
    	cout << "B0::Show()" << endl; }
};
class B1 : public B0
{		
public: 
	void Show() { 
    	cout << "B1::Show()" << endl; }
};
class D2 : public B1
{		
public: 
	void Show() { 
    	cout << "D2::Show()" << endl; }
};

void fun(B0* ptr) {
    ptr->Show();
}

int main() {
    B0 r0;
    B1 r1;
    D2 r2;

    B0 *p;
    p = &r0; //B0 pointer to B0 object
    fun(p);
    p = &r1; //B0 pointer to B1 object
    fun(p);
    p = &r2; //B0 pointer to D2 object
    fun(p); 
 
    system("pause");
    return 0;
}

