#include <iostream>
#include <cstdlib>
#include <cstring>

using namespace std;

class CCustomer {
    friend void showAFriend(CCustomer);
    int cid; double balance;
public:
    CCustomer(int x=0, double y=0) { 
        cid=x; balance=y; 
	}
	
	// member function 
    void showCCustomer() {
		cout << "===in the member function===" << endl; 
		cout << cid << " with $"  << balance << endl; 
	} 
};

//friend function
void showAFriend(CCustomer c){
    cout << "===in the friend function===" << endl;
    cout << c.cid << " with $" << c.balance << endl;
}

int main() {
    CCustomer one( 10963, 3437.95);

    //call member function
    one.showCCustomer();

    //call friend function
    showAFriend(one);   
	 
	system("Pause");
    return 0;  
}


