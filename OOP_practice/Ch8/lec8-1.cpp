#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class B1 {
    int x;
    protected: 
        int GetX() { return x; }
    public:   
        void SetX(int a=1) { x=a; } 
};
class B2 {
    int y;
    public: 
        int GetY() { return y; }
        void SetY(int a=1) { y=a; } 
};
class B3 {
    int z;
    public: 
        int GetZ() { return z; }
        void SetZ(int a=1) { z=a; } 
};
class D4 : public B1,public B2,public B3 {
    int w;
    public: 
        void SetW(int a) { w=a; }
        void ShowVal() {
            cout << GetX() << " "<< GetY() << " "
                << GetZ() << " " << w << endl;
        }
}; 

int main() {
    D4 obj;
    obj.SetX(1); obj.SetY(2); 
    obj.SetZ(3); obj.SetW(4);
    obj.ShowVal(); 

 	system("pause");
    return 0;
}


