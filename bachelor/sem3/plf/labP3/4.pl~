%toate nr de la 1 la n
%cu nr consec |x - y| <= m

%generare_toate_nr de la x la x + limit
%my_generate(X:int, Limit:int, Rez:int)
%(i, i, o) - nedeterminist
my_generate(X, Limit, X) :- X =< Limit.
my_generate(X, Limit, R) :-
    X1 is X + 1,
    X1 =< Limit,
    my_generate(X1, Limit, R).

%crearea unei liste de la current la n
%unde nr consecutive au ca diferenta in modul >= m
%generand pentru fiecare termen prin backtracking
%numarul urmator care respecta acea cerinta
%my_create_list(N:int, M:int, Current:int, Rez:list)
%(i, i, i, o) - nedeterminist
%important ca sirul sa inceapa si sa se termine cu n
%apar doua cazuri: 1-daca urmatorul unui numar este mai mic decat n - m
%                  2-daca urmatorul unui numar este mai mare decat n - m
%1->se genereaza toate posibilitatile de la "current" la n - m
% 2->nu avem posibilitati de a genera mai multe numere
my_create_list(N, M, Current, [Current|Rez]) :-
    Start is Current + M,
    Limit is N - M,
    Start =< Limit,!,
    my_generate(Start, Limit, R),
    my_create_list(N, M, R, Rez).
my_create_list(N, M, Current, [Current|Rez]) :-
    Next is Current + M,
    Next >= N - M,
    Next =< N,!,
    my_create_list(N, M, Next, Rez).
my_create_list(N, _, _, [N]):-!.

%apelarea cu datele de input, specificand ca se pleaca de la 0
main_create_list(N, M, Rez) :-
    my_create_list(N, M, 1, Rez).
































