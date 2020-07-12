#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class C1 {
    public: 
        C1() { cout << "construct C1\n"; }
        ~C1() { cout << "destruct C1\n"; } 
};

class C2 {
    public: 
        C2() { cout << "construct C2\n"; }
        ~C2() { cout << "destruct C2\n"; } 
};

class C3 {
    public: 
        C3() { cout << "construct C3\n"; }
        ~C3() { cout << "destruct C3\n"; } 
}; 

class C4 {
    public: 
        C4() { cout << "construct C4\n"; }
        ~C4() { cout << "destruct C4\n"; } 
};

class CD: public C3, virtual public C4,
          virtual public C2 {
    C1 obj;
    public: 
        CD() : obj(), C2(), C3(), C4() { 
            cout << "construct CD\n";
        }
        ~CD() { cout << "destruct CD\n"; } 
};

int main() { 
	//what happens?
    CD dd; 
	cout << "here!\n"; 
    
	//system("pause");
	return 0;
} 

