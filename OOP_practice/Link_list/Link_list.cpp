#include <iostream>
using namespace std;

int main()
{
    struct Linklist{
        int value;
        Linklist* next_addr;

        Linklist(): value(0), next_addr(NULL){}
    };

    struct Linklist* root = new Linklist;
    struct Linklist* __parent_node = new Linklist;
    struct Linklist* __child_node = new Linklist;

    while (true)
    {
        char status;
        cout << "Please select an option:" << endl;
        cout << "1.Insert a node" << endl;
        cout << "2.Delete a node" << endl;
        cout << "3.Display the list" << endl;
        cout << "4.End" << endl;
        cin >> status;
        switch (status)
        {
            int input;
            case '1':
            {
                cout << "Please enter the number :" << endl;
                cin >> input;
                if (root->next_addr == NULL && __parent_node != root)
                {
                    delete __parent_node;
                    root->value = input;
                    root->next_addr = NULL;
                    __parent_node = root;
                }
                else
                {
                    __child_node = new Linklist;
                    __parent_node->next_addr = __child_node;
                    __child_node->value = input;
                    __child_node->next_addr = NULL;
                    __parent_node = __child_node;
                }
            }
            break;
            case '2':
            {
                cout << "Please enter the number :" << endl;
                cin >> input;
                if (root->value == input)
                {
                    Linklist* tmp = root;
                    root = root->next_addr;
                    delete tmp;
                    break;
                }
                __parent_node = root;
                __child_node = __parent_node->next_addr;
                while ((__child_node->next_addr != NULL) && (__child_node->value != input))
                {
                    __parent_node = __child_node;
                    __child_node = __child_node->next_addr;
                }
                if (__child_node->value == input)
                {
                    __parent_node->next_addr = __child_node->next_addr;
                    delete __child_node;
                }
                else
                {
                    cout << "Failed to delete node " << input << endl;
                }
            }
            break;
            case '3':
            {
                Linklist* tmp = root;
                while (tmp->next_addr != NULL)
                {
                    cout << tmp->value << "->";
                    tmp = tmp->next_addr;
                }
                if (root->next_addr == NULL && __parent_node != root)
                {
                    cout << "Please insert a node first!" << endl;
                }
                else
                {
                    cout << tmp->value << "->" << endl;
                }
            }
            break;
            case '4':
            {
                return 0;
            }
            break;
            default:
            {
                cout << "Enter from 1~4!" << endl;
            }
        }
    }
}