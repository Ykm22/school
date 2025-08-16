%sterge(L:list, A:atom, Rez:list)
%(i, i, o) determinist

sterge([], _, []).
sterge(A, A, []):-!.
sterge([H|T], A, Rez) :-
    H =:= A,!,
    sterge(T, A, Rez).
sterge([H|T], A, [H|Rez]) :-
    sterge(T, A, Rez).

%numar(L:List, Rez:list)
%(i, o) determinist


numar([],
