%my_reverse(L:list, LRez:list)
%(i, o) (i, i) - determinist
%L - lista pe care vrem sa o inversam
%LRez - rezultatul, lista L inversata
my_reverse([], []).
my_reverse([E], [E]).
my_reverse([H|T], LRez) :-
    my_reverse(T, LRez2),
    !,
    append(LRez2, [H], LRez).

%predecessor(L:list, Flag:int, LRez:list)
%(i, i, o), (i, i, i) - determinist
% L: Lista de cifre INVERSATA a unui numar din care vrem sa obtinem
% predecesorul
%Flag: Arata daca
%            1 - mai trebuie sa facem scaderi
%            0 - am terminat de scazut
% LRez: Lista de cifre INVERSATA care reprezinta predecesorul lui
% numarului reprezentat pe lista L
predecessor([], _, []) .
predecessor([E], 1, [E2]) :-
    E2 is E - 1.
predecessor([E], 0, [E]).
predecessor([H|T], 1, [H2|LRez]) :-
    H > 0,
    H2 is H - 1,!,
    predecessor(T, 0, LRez).
predecessor([H|T], 1, [9|LRez]) :-
    H = 0,
    !,
    predecessor(T, 1, LRez).
predecessor([H|T], 0, [H|LRez]) :-
    predecessor(T, 0, LRez).

remove_zero([], []).
remove_zero([H|T], [H|T]) :-
    H =\= 0.
remove_zero([H|T], T) :-
    H =:= 0.

%predecessor_main(L:list, Result:list)
%(i, o), (i, i) - determinist
%L : Lista de cifre a unui numar din care vrem sa obtinem predecesorul
%Result : Lista de cifre a predecesorului
predecessor_main(L, Result) :-
    my_reverse(L, Reversed_L),
    predecessor(Reversed_L, 1, Predecessor),
    !,
    my_reverse(Predecessor, Result1),
    remove_zero(Result1, Result).

p2_14a_go1 :-
    predecessor_main([6, 2, 0, 0, 0], LRez),
    write(LRez).
p2_14a_go2 :-
    predecessor_main([1, 0, 0, 0, 0], LRez),
    write(LRez).
p2_14a_go3 :-
    predecessor_main([9, 9, 9, 9, 9], LRez),
    write(LRez).
p2_14a_go4 :- predecessor_main([1,0,0], [0, 9, 9]).

%predecessor_heterogeneousList(L:hetList, LRez:hetList
%(i, i), (i, o) - determinist
%L: lista eterogena initiala
%LRez: lista eterogena dupa modificare
predecessor_heterogeneousList([], []).
predecessor_heterogeneousList([H|T], [H|LRez]) :-
    number(H),
    !,
    predecessor_heterogeneousList(T, LRez).
predecessor_heterogeneousList([H|T], [H2|LRez]):-
    is_list(H),
    predecessor_main(H, H2),
    predecessor_heterogeneousList(T, LRez).
p2_14b_go :-
    predecessor_heterogeneousList([1, [2, 3], 4, 5, [6, 7, 9], 10, 11, [1, 2, 0], 6], LRez),
    write(LRez).









