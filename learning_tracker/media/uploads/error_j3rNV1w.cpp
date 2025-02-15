// Online C++ compiler to run C++ program online
#include <iostream>
#include <climits>
using namespace std;

int reverse(int x)
{
    int ans = 0;

    while (x != 0)
    {
        int digit = x % 10;

        // Check for overflow before multiplication and addition
        if (ans > INT_MAX / 10 || ans < INT_MIN / 10)
        {
            return 0;
        }
        ans = (ans * 10) + digit;
        x /= 10;
    }

    return ans;
}

int main()
{
    int n;
    cout << "Enter a number: ";
    cin >> n;
    cout << "The reverse is: " << reverse(n) << endl;

    return 0;
}