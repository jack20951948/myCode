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

class CCuboid : public CRect {
protected:
    double ht; //dp for depth
public:
    CCuboid(double a, double b, double c, double d, double e) :
        CRect(a,b,c,d) { ht = e; }
    void SetHeight(double d=1.0) { ht = d; }
    double GetHeight() const { return ht; }
    double Area() const { 
		return (2*CRect::Area()+2*GetL()*ht+2*GetW()*ht);              
	} 
    friend ostream & operator << (ostream &,
        const CCuboid &);
    string ToString() const	{ 
        return "CCuboid";
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

ostream & operator << (ostream & out, const CCuboid& p) {
    out << p.GetX() << " " << p.GetY()  
	    << " surface " << p.Area(); 
	return out;	
}

int main()
{  
    CCuboid cu1(2,3,20,10,5);
    cout << "old: " << cu1 << endl;
	cu1.SetRect(1,1,8,6);
    cout << "new: " << cu1 << endl;
	CPoint &pRef = cu1;
    cout << "pRef: " << pRef << endl;
 	CRect &rRef = cu1;
    cout << "rRef: " << rRef << endl; 
	
	system("pause");
	return 0;
}