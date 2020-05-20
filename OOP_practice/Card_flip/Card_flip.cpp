#include <iostream>
#include <time.h>
using namespace std;

struct CARD
{
    char value;
    bool front = false;
};

CARD board[37];

void init_board();
void display_board(int choice1=37, int choice2=37);
bool check_win();
char* shuffle(char* data);

int main()
{
    init_board();

    while (!check_win())
    {
        int first_choice, second_choice;

        cout << "Please enter card index: ";
        cin >> first_choice;
        display_board(first_choice);
        cout << "Please enter card index: ";
        cin >> second_choice;
        
        if (board[first_choice].value == board[second_choice].value)
        {
            board[first_choice].front = true;
            board[second_choice].front = true;
            display_board();
            cout << "Good Job!" << endl;
        }
        else
        {
            display_board(first_choice, second_choice);
            cout << "Try Again!" << endl;
        }
    }
    cout << "Congratulation!!" << endl;
}

void init_board()
{
    srand(time(NULL));
    char defdata[37] = "AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRR";
    char *data = shuffle(defdata);

    for (int i = 0; i < 36; i++)
    {
        board[i].value = data[i];
    }
    display_board();
}

char *shuffle(char *data)
{
    int cardSize = 36;
    while (cardSize > 1)
    {
        int k = rand();
        k = k % 36;
        cardSize--;
        char temp = data[cardSize];
        data[cardSize] = data[k];
        data[k] = temp;
    }
    return data;
}

void display_board(int choice1, int choice2)
{
    for (int i = 0; i < 6; i++)
    {
        for (int j = 0; j < 6; j++)
        {
            if (board[(i * 6) + j].front || choice1 == (i * 6) + j || choice2 == (i * 6) + j)
            {
                cout << board[(i * 6) + j].value;
            }
            else
            {
                cout << "*";
            }
        }
        cout << endl;
    }
}

bool check_win()
{
    for (int i = 0; i < 36; i++)
    {
        if (!((board + i)->front))
        {
            return false;
        }
    }
    return true;
}