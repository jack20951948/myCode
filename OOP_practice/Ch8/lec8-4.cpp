#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CA	//common base class of CB and CC
{	
    public:
        int x;
        CA(int a=0) { x=a; }
};

//class CB : public CA	 //original one base class of CD
class CB : virtual public CA	 //Try 1: new base class of CD
{	
    public:
        int y;
        CB(int a=0, int b=0) : CA(a) { y=b; }
};

//class CC : public CA	 //original: one base class of CD
class CC : virtual public CA	 //Try 1: new base class of CD
{	
    public:
        int z;
        CC(int a=0, int b=0) : CA(a) { z=b; }
};

class CD: public CB, public CC 
{	
    public:
        int w;
        CD(int a=0, int b=0, int c=0, int d=0, int e=0) : 
            // CB(a,b), CC(c,d) { w=e; } // original constructor
            CA(a), CB(a,b), CC(c,d) { w=e; } //Try 1: new constructor
            // CB(a,b), CC(c,d) { w=e; } //Try 2: new new constructor, what if CA(a) is missing like original??
            //Result: a will not be initilized and thus equals 0!!!
        void ShowVal() {
            cout << " x=" << CB::x << " y=" << y;
            cout << " x=" << CC::x << " z=" << z;
            cout << " w=" << w << " x=" << x << endl;
        }
};

int main() 
{
 	CD obj(5,4,3,2,1);
	obj.ShowVal(); //what happens? 
	//There are two copies of x from CB and CC

	system("pause");
    return 0;	
}

