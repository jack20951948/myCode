#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CPoint //base class
{		
    double x, y;
public:
    CPoint(double a=0, double b=0): 
    	x(a), y(b) { } 
	void SetPoint(double a=0, double b=0) { 
        x = a; y = b;                     }
	void MovePoint(double dx, double dy) { 
        x += dx; y += dy;                }
	double GetX() const { return x; }
	double GetY() const { return y; }
};

class CRect: private CPoint //derived class
{
//private:
    double h, w; //new private data
public:
	CRect(): CPoint(),h(0),w(0) { ; }
	CRect(double a, double b, double c, double d): 
    	h(c), w(d) { SetPoint(a,b); } 
	double GetX() const { return CPoint::GetX(); }
	double GetY() const { return CPoint::GetY(); }
	double GetH() const { return h; }
	double GetW() const { return w; }
    //derived member functions can access
    //base member functions
    void SetRect(double a, double b, 
                 double c, double d) {
        CPoint::SetPoint(a,b);
        h = c; w = d;                }
    void MoveRect(double dx, double dy) {
        CPoint::MovePoint(dx, dy);      }  
};

int main()
{  
    CRect cr2;
	cr2.SetRect(2,3,20,10);
    //a derived object cannot access any
    //member of the base class
	//cr2.MovePoint(3,2); //illegal!!!
    //use its own member function
    cr2.MoveRect(3,2); //legal 
	cout << cr2.GetX() << ',' 
	     << cr2.GetY() << ','
		 << cr2.GetH() << ',' 
		 << cr2.GetW() << endl;
		 		 
	system("pause");
	return 0;
}


