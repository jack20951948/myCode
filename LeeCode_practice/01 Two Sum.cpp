#include <vector>
#include <iostream>
using namespace std;

class Solution {
public:
    vector<int> input;
    int target;
    vector<int> output;

    Solution(vector<int>& nums, int target1) { 
        input = nums;
	    target = target1;
        output = {0, 1};
    }

    vector<int> twoSum() {
        for (vector<int>::iterator it_i = input.begin(); it_i != input.end(); it_i++){
            for (vector<int>::iterator it_i2 = it_i + 1; it_i2 != input.end(); it_i2++){
                if ((*it_i + *it_i2) == target){
                    return {output[0], output[1]};
                }
                output[1]++;
            }
            output[0]++;
            output[1] = output[0] + 1;
        }
        throw invalid_argument("Can't find the solution by the given numbers!");
    }

    void showResult(){
        cout << "input: ";
        vector <int>::iterator i;
        for (i=input.begin(); i!=input.end(); i++) cout << *i << " ";
        cout << endl;
        cout << "target: " << target << endl;
        cout << "output: " << output[0] << ", " << output[1];
    }
};

int main(){
    vector<int> input = {2, 4, 5, 8};
    int target = 9;
    Solution solution(input, target);
    vector<int> output = solution.twoSum();
    solution.showResult();
}