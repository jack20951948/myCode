#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CFig {
    protected:		
        double x, y;
    public:
        void SetDim(double a=0, double b=0) { 
            x=a; y=b;                       
        } 
        virtual void Area()=0;  //pure virtual! for derived class use, 
                                //if exist one or more pure virtual functions, we tent to call it abstract base class
};
class CRec: public CFig {
    public: 
        void Area(int i) { 
            cout << "Rec:" << x*y << endl; 
        }    
};
class CTri: public CFig {
    public:
        void Area() { 
            cout << "Tri:" << x*y/2 << endl; 
        }
};


int main() 
{
 	CFig *pF;
    // CFig  f1; //what happen? => cannot declar f1 because CFig is abstract base class 
    // CRec  r2; //what happen? => cannot declar r2 because CRec is abstract base class 
    CTri t3;
    t3.SetDim(20,10);
    pF = &t3;
    pF->Area();
    CFig &rF = t3;
    rF.SetDim(5,4);
    rF.Area(); 

	system("pause");
    return 0;	
}