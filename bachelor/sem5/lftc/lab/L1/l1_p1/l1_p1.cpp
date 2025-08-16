#include <iostream>

using namespace std;

int main()
{
    double radius, pi, perimeter, area;
    pi = 3.14;
    cin >> radius;
    perimeter = 2 * pi * radius;
    area = pi * radius * radius;
    cout << perimeter << " " << area;
    return 0;
}