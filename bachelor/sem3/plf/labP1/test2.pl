%member(E:el, L:list)
%(i, i) - determinist
%(o, i) - nedeterminist

member(E, [ E | _ ]) :- !.
member(E, [ _ | L ]) :- member(E, L).

go2 :- member(1, [1,2,1,3,1,4]).


