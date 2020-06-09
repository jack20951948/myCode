#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class Sofa {
    protected: int weight;
    public: 
        void sit() { cout << "sit!" << endl; }
        void SetWeight(int a=0) { weight=a; }
        int GetSofaWeight() { return weight; }
        void ShowWeight() { 
            cout << "Sofa weight=" << weight; } 
};

class Bed {
    protected: int weight;
    public: 
        void lie() { cout << "lie!" << endl; }
        void SetWeight(int a=0) { weight=a; }
        int GetBedWeight() { return weight; }
        void ShowWeight() { 
            cout << "Bed weight=" << weight; } 
};

class SofaBed : public Sofa, public Bed  
{
    public: 
        void fold() { cout << "fold!" << endl; }
        void ShowWeight(){
            Sofa::ShowWeight();
            cout << "&";
            Bed::ShowWeight();
            cout << endl;
        }
};

int main() 
{
    SofaBed myfur;
  
    myfur.sit();
    myfur.lie();
    myfur.fold();

    myfur.ShowWeight();

    // myfur.SetWeight(100); //call which one?  
    //you need to specify the resolution. e.g.
    myfur.Sofa::SetWeight(200);
	myfur.Sofa::ShowWeight(); 
	cout << endl;
	
	myfur.Bed::SetWeight(300);
    myfur.Bed::ShowWeight(); 
	cout << endl;

    //side effect 2
	SofaBed obj;
	obj.Sofa::SetWeight(25);
	Bed *ptr;
	ptr = new Bed;

	ptr->SetWeight(70);
	ptr->ShowWeight();
	cout << endl;

	ptr = &obj; //convert SofaBed object to a Bed object
	ptr->ShowWeight(); //call which?? what happenes?
	//weight in Bed is never set!!!
	
	
	system("pause");
    return 0;	
}

