%contains(E:elem, L:list)
%if E is in List
%(i, i) determinist

contains(E, [E|_]):-!.
contains(E, [_|T]) :-
    contains(E, T).

not_contains(_, []):-!.
not_contains(E, [_|T]) :-
    not_contains(E, T).
%list_to_set(L:list, Rez:list)
%(i, o) determinist

my_list_to_set(A


%my_list_to_set([], []).
%my_list_to_set([H|T], Rez) :-
%    contains(H, T),!,
%    my_list_to_set(T, Rez).
%my_list_to_set([H|T], [H|Rez]) :-
%    my_list_to_set(T, Rez).

%main_my_list_to_set(L, Rez) :-
%    my_list_to_set(L, Rez1),
%    my_reverse(Rez1, Rez).

my_reverse([H|T], Rez):-
    my_reverse_help(T, [H], Rez).
my_reverse_help([], E, E).
my_reverse_help([H|T], E, Rez) :-
    my_reverse_help(T, [H|E], Rez).


reverseList([H|T], Rez):-
    reverseListHelper(T,[H], Rez).
reverseListHelper([], Acc, Acc).
reverseListHelper([H|T], Acc, Rez):-
    reverseListHelper(T, [H|Acc], Rez).

descompune_list([], [], [], 0, 0).
descompune_list([H|T], [H|L1], L2, P1, I) :-
    H mod 2 =:= 0,!,
    descompune_list(T, L1, L2, P, I),
    P1 is P + 1.
descompune_list([H|T], L1, [H|L2], P, I1) :-
    descompune_list(T, L1, L2, P, I),
    I1 is I + 1.
descompune_main(L, [L1,L2], P, I) :-
    descompune_list(L, L1, L2, P, I).





























