#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CPoint //base class
{		
    double x, y;
	public:
		CPoint(double a=0, double b=0): 
			x(a), y(b) {} 
		void SetPoint(double a=0, double b=0) { 
			x=a; y=b;
		}
		void MovePoint(double dx, double dy) {
			x += dx; y += dy;
		}
		double GetX() const { return x; }
		double GetY() const { return y; }
};

class CRect: public CPoint //derived class
{
	//private:
		double h, w; //new private data members
	public:	
		//inherit member functions from CPoint
		//add new member functions
		CRect(): CPoint(),h(0),w(0) { ; }
		CRect(double a, double b, double c, double d):
			h(c), w(d) { SetPoint(a,b); }
		void SetRect(double a, double b, double c, double d) {
			SetPoint(a,b);
			h = c; w = d;
		}
		double GetH() const { return h; }
		double GetW() const { return w; }
};

int main()
{
    CRect cr1;
	cr1.SetRect(2,3,20,10);
    //visit base public members through
    //a derived object
	cr1.MovePoint(3,2);
	cout << cr1.GetX() << ','
		 << cr1.GetY() << ','
		 << cr1.GetH() << ','
		 << cr1.GetW() << endl;

	system("pause");
	return 0;
}