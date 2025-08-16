%contains(E:elem, L:list)
%if E is in List
%(i, i) determinist

contains(E, [E|_]):-!.
contains(E, [_|T]) :-
    contains(E, T).

%elimina toate nr care se repeta
%elimin6(L:list, Rez:list)

elimin6([], []).
elimin6([H|T], Rez) :-
    contains(H, T),!,
    elimin6(T, Rez).
elimin6([H|T], [H|Rez]):-
    elimin6(T, Rez).
