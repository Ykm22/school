%subst(L:list, E:elem, L2:list, R:list)
%where there's E, substitute with L2
%(i,i,i,o) determinist

subst([], _, _, []).
subst([H|T], H, L2, [L2|Rez]) :-
    !,subst(T, H, L2, Rez).
subst([H|T], _, L2, [H|Rez]) :-
    subst(T, _, L2, Rez).

elimin([], _, []).
elimin([H|T], M, [H|Rez]) :-
    M \= 0,!,
    M1 is M - 1,
    elimin(T, M1, Rez).
elimin([_|T], M, Rez) :-
    M1 is M - 1,
    elimin(T, M1, Rez).
