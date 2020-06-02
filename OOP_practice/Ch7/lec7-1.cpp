#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;
const double PI = 3.14;

//base class
class CCircle {
    protected:
        double radius;
    public:
        CCircle(double r=1.0):radius(r) { ; }
        void setR(double r=1.0) { radius=r; }
        double calVol() const { 
            return (PI*radius*radius); 
        } 
        void showVol() const {
            cout << "radius=" << radius << " ";
            cout << "volume=" << calVol() << endl;
        }
};

//derived class
class CCylinder : public CCircle {
    protected:
        double length; //add one data member
    public:
        CCylinder(double r=5.0, double l=1.0) : CCircle(r),length(l) { ; }
        //Q: what if using the following statement instaed?
        //CCylinder(double r=1.0, double l=1.0) : radisu(r),length(l) { ; }
        
        void setRL(double r=5.0, double l=1.0){
            radius = r; length = l;  
        }
        //calculate the volume of a cylinder
        double calVol() const { 
            return (CCircle::calVol()*length); 
        } 
        //inherit showVol() from CCircle
        
        void displayVol() const {
            cout << "d radius=" << radius << " ";
            cout << "d volume=" << calVol() << endl;
        }
}; 

int main() {
    CCircle cr1, cr2(4);
    CCylinder cy1, cy2(2,3);
   
    cr1.setR(2);
    cr1.showVol(); cr2.showVol();
    cy1.setRL(3);
    cy1.showVol(); cy1.displayVol();  
	cy2.showVol(); cy2.displayVol();

    cr1 = cy1; //Q: what happen?
    cr1.showVol();
 
 	system("pause");
    return 0;
}