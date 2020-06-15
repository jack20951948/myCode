#include <iostream>
#include <cstdlib>
#include <string>

using namespace std;

class Pet 
{
	public:
		string name;
		virtual void print() const;
};
void Pet::print() const {
	cout << "Pet::print() " << name << endl;	
}

class Dog : public Pet
{
	public:
		string breed;
		virtual void print() const;	//keyword virtual not needed, but put here for clarity.
};
void Dog::print() const {
	cout << "Dog::print() " << name << " " << breed << endl;	
}
int main() 
{
 	Pet vpet; //base-class object
	Dog vdog; //derived-class object
	vdog.name = "Tiny";
	vdog.breed = "Maltese";
	vpet = vdog;	// Legal!
	vpet = static_cast<Pet>(vdog); //legal!
	//vdog = static_cast<Dog>(vpet);  //Q1: What happens? => ILLEGAL!
	vpet.print();
	
	Pet *ppet;
	Dog *pdog;
	ppet = new Pet;
	pdog = new Dog;
	pdog->name = "Tiny";
	pdog->breed = "Maltese";
	pdog->print(); //Q2: which print to call?
	ppet = pdog;
	ppet->print(); //Q2: which print to call?
	//cout << ppet->breed << endl; //Error!! Cannot access breed => slicing problem
	
	/*	
	Pet *tpet; 
	tpet->name = "Giant";
	tpet = new Dog;
	Dog *tdog = dynamic_cast<Dog*>(tpet); 
	tdog->print(); //Q3: problematic!! => Self study of dynamic_cast<>
	*/
	
	system("pause");
    return 0;	
}
