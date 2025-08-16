my_merge([], [], []).
my_merge([H|T], [], [H|LRez]) :-
    my_merge(T, [], LRez).

my_merge([], [H|T], [H|LRez]) :-
    my_merge([], T, LRez).

my_merge([H1|T1], [H2|T2], [H1|LRez]) :-
    H1 =< H2,
    my_merge(T1, [H2|T2], LRez).

my_merge([H1|T1], [H2|T2], [H2|LRez]) :-
    H2 < H1,
    my_merge([H1|T1], T2, LRez).

no_duplicates([], _, []).
no_duplicates([H|T], E, [H|LRez]) :-
    H \= E,
    no_duplicates(T, H, LRez).
no_duplicates([H|T], E, LRez) :-
    H =:= E,
    no_duplicates(T, E, LRez).

main_merge(L1, L2, [H|LRez]) :-
    my_merge(L1, L2, [H|LRez1]),
    no_duplicates([H|LRez1], H, LRez).

heteroList_merge([], []).
heteroList_merge([H|T], LRez) :-
    number(H),!,
    heteroList_merge(T, LRez).
heteroList_merge([H|T], [List|LRez]) :-
    is_list(H),!,
    main_merge(H, LRez, List),
    heteroList_merge(T,  LRez).



