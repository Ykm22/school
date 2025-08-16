%pereche(E: el, L:list, LRez:list)
%(i, i, o) - nedet
pereche(A, [B | _ ], [ A | B ]) :-
    A < b.
pereche( A, [ _ | T ], P) :-
    pereche(A, T, P).

%perechi(L:list, LRez:list)
%(i, o) - nedet
perechi( [H | T], P ) :-
    pereche(H, T, P).
perechi( [_|T], P) :-
    perechi(T, P).

%toatePerechi(L;list, LRez:list)
%(i, o) - determinist
toatePerechi(L, LRez) :-
    findall(X, perechi(L, X), LRez).

