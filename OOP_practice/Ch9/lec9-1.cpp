#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CPoint	//base class: class CPoint
{		
    double x, y;
	public:
		CPoint(double a=0, double b=0): 
			x(a), y(b) {} 
		void SetPoint(double a=0, double b=0) { 
			x=a; y=b;
		}
		double GetX() const { return x; }
		double GetY() const { return y; }
		friend ostream & operator << (ostream &, const CPoint&);
		string ToString() const { 
			return "CPoint";
		}
};

class CRect: public CPoint
{   //add new private data members
	double lg, wd; 
	public:	//add new member functions
		CRect(double a, double b, double c, double d) : 
			lg(c),wd(d) { SetPoint(a,b); } // call func in CPoint
		void SetRect(double a, double b, double c, double d) {
			SetPoint(a,b); lg = c; wd = d; 
		} // call func in CPoint
		double GetL() const { return lg; }
		double GetW() const { return wd; }
		double Area() const { return lg*wd; }
		friend ostream & operator << (ostream &, const CRect &);
		string ToString() const { 
			return "CRect";
		}
};

ostream & operator << (ostream & out, const CPoint& p) {
    out << p.x << " " << p.y; 
	return out;
}

ostream & operator << (ostream & out, const CRect& p) {
    out << p.GetX() << " " << p.GetY() 
        << " area " << p.Area(); 
	return out;
}

int main()
{  
    CRect cr1(2,3,20,10);
    cout << "old: " << cr1 << endl;
	cr1.SetRect(5,5,9,7);  
    cout << "new: " << cr1 << endl;
	CPoint &rRf = cr1;
    cout << "rRf: " << rRf << endl;
	 
	system("pause");
	return 0;
}