#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class B0
{		
    public: 
        void Show() { 
            cout << "B0::Show()" << endl;
        }
};
class B1 : public B0
{		
    public: 
        void Show() { 
            cout << "B1::Show()" << endl;
        }
};
class D2 : public B1
{		
    public: 
        void Show() { 
            cout << "D2::Show()" << endl;
        }
};

void fun(B0* ptr) {
    ptr->Show();
}

int main() {
    B0 r0;
    B1 r1;
    D2 r2;

    B0 *p;
    p = &r0; // B0 pointer to B0 object
    fun(p);
    p = &r1; // B0 pointer to B1 object
    fun(p);  // fun() would see input as a B0 class, force to transform to a B0 object, refer to line 29
    p = &r2; // B0 pointer to D2 object
    fun(p);  // fun() would see input as a B0 class, force to transform to a B0 object, refer to line 29

    system("pause");
    return 0;
}