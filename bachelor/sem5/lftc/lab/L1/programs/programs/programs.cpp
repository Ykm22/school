#include <iostream>

using namespace std;

void p1() {
    float radius, pi, perimeter, area;
    pi = 3.14;
    cin >> radius;
    perimeter = 2 * pi * radius;
    area = pi * radius * radius;
    cout << perimeter << " " << area;
}

void p2() {
    int a, b, gcd;
    cin >> a >> b;
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    cout << a;
}

void p3() {
    int n, x, sum;
    sum = 0;
    cin >> n;
    while (n != 0) {
        cin >> x;
        sum = sum + x;
        n = n - 1;
    }
    cout << sum;
}

void p4() {
    int n, x, sum = 0;
    cin >> n;
    while (n != 0) {
        cin >> x;
        sum += x;
        n--;
    }
    cout << sum;
}

int main() {
    p1();
    cout << endl;
    p2();
    cout << endl;
    p3();
    cout << endl;
    p4();
    cout << endl;
    return 0;
}