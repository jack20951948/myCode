#include<fstream>  //ifstream
#include<iostream>
#include<string>     //包含getline()
#include<cmath>
using namespace std;

int main(){
    string s;

    ifstream inf;
    inf.open("in.txt");          //特別注意，這裡是：//  是雙斜槓喔~~     ifstream inf("d://out.txt");用這一句可以代替這兩句喔，很簡單有木有~~

    //開啟輸出檔案
    ofstream outf;
    outf.open("out.txt");

    while (getline(inf, s))      //getline(inf,s)是逐行讀取inf中的檔案資訊
    {
        outf << s << '\n';               
        cout << s << endl << endl;           
    }                            

    inf.close();
    outf.close();
    return 0;
}