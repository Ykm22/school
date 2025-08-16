%gcd(X:integer, Y:integer, Z:integer)
%(i, i, o)
gcd(X, 0, X) :- !.
gcd(X, Y, Z) :-
    M is mod(X, Y),
    gcd(Y, M, Z).

%lcm(X:integer, Y:integer, LCM:integer)
%(i, i, o)
lcm(X, Y, LCM) :-
    gcd(X, Y, GCD),
    LCM is X*Y/GCD.

%lcm_list(L:list, LCM:integer)
%(i, o)
lcm_list([], 1) :- !.
lcm_list([H|T], LCM) :-
    lcm_list(T, LCM2),
    lcm(H, LCM2, LCM).

