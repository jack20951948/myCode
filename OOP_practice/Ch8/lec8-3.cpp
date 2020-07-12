#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CB {
	public:
		void f() { cout << "CB's f()" << endl; }
		void f(int x) { 
			cout << "CB's f(x)" << endl;
		}        
};
        
class CD : public CB {
	public:
		void f() { cout << "CD's f()" << endl; }  
};

int main() 
{
	CD obj;
	obj.f();
	obj.f(5); //what happens?  	
	// Q: what if calling 
	// obj.CB::f(5);

	system("pause");
    return 0;	
}
