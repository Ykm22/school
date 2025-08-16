%contains(E:elem, L:list)
%if E is in List
%(i, i) determinist

contains(E, [E|_]):-!.
contains(E, [_|T]) :-
    contains(E, T).

%diferenta_multimi(L1:list, L2:list, Res:List)
%(i, i, o), (i, i, i) determinist
%L1\L2

diferenta_multimi([], [], []).
diferenta_multimi([], [_|_], []).
diferenta_multimi([E|T], L2, Rez) :-
    contains(E, L2),!,
    diferenta_multimi(T, L2, Rez).
diferenta_multimi([E|T], L2, [E|Rez]) :-
    diferenta_multimi(T, L2, Rez).

%add_after_even_1(L:list, Rez:list)
%(i, i, o)
add_after_even_1([], []).
add_after_even_1([H|T], [H, 1|Rez]):-
    H mod 2 =:= 0,!,
    add_after_even_1(T, Rez).
add_after_even_1([H|T], [H|Rez]) :-
    add_after_even_1(T, Rez).




