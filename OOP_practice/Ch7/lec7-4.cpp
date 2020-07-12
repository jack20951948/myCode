#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class A
{
    private:
        double x;
    protected:
        long y;
    public:
        short z;
};

class B : public A {
    public:
        void f() {
            x = 3.0; //what happenes? Try to comment this line
            // x is private in class A; cannot access
            y = 4; 
            z = 2;
        }
};

int main() {
    B b;
    b.x = 1.3; //what happenes? Try to comment this line
    //x is private in class A; cannot be accessed by any mean
    b.y = 2;   //what happenes? Try to comment this line
	//y is protected in class B; cannot be accessed by an object
    b.z = 5;

    system("pause");
    return 0;
}