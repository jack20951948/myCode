#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class Furniture { //common base class
    protected: int weight;
    public: 
        void SetWeight(int a=0) { weight=a; }
        int GetWeight() { return weight; }
        void ShowWeight() { 
            cout << "weight=" << weight << endl;
        } 
};

class Sofa : virtual public Furniture {
    public: 
        void sit() { cout << "sit!" << endl; }
        //void ShowWeight() { 
        //    cout << "Sofa weight=" << weight; } 
};

class Bed : virtual public Furniture {
    public: 
        void lie() { cout << "lie!" << endl; }
        //void ShowWeight() { 
        //    cout << "Bed weight=" << weight; } 
};

class Sofabed : public Sofa, public Bed {
    public: 
        void fold() { cout << "fold!" << endl; }
};


int main() 
{
 	Sofabed obj;
    obj.sit();
    obj.lie();
    obj.fold();
 
    obj.SetWeight(100); //call which one?  => the only one SetWeight in Furniture
    obj.ShowWeight(); //what happens? => call the only one ShowWeight in Furniture
    
	system("pause");
    return 0;	
}