;l - list of atoms(and of possible other lists), found_nr - int
;get first number from left to right
;found_nr = 0 => haven't found nr yet
;found_nr won't take other values, function stops at first number found
;   but in case we don't find any numbers answer will be NIL
(defun getfirstnr (l found_nr)
    (cond
        ((and (null l) (= found_nr 0)) nil)
        ((numberp (car l)) (car l))
        ((atom (car l)) (getfirstnr (cdr l) found_nr))
        (T (getfirstnr (car l) found_nr))
    )
)

;l - list of atoms, e - int
;get minimum nr of a list of lists
;by comparing each number with e
;and updating it accordingly
(defun min_aux (l e)
    (cond 
        ((null l) e)
        ((listp (car l)) (min_aux (cdr l) (min_aux (car l) e)))
        ((and (numberp (car l)) (>= (car l) e)) (min_aux (cdr l) e))
        ((and (numberp (car l)) (< (car l) e)) (min_aux (cdr l) (car l)))
        (T (min_aux (cdr l) e))
    )
)
;l - list of atoms
;calling auxiliary function with 2nd argument as first number appearing in list
(defun my_min (l)
    (min_aux l (getfirstnr l 0))
)

(print '(t e s t - c))
(print (my_min '((1 (-1 -100 d c f -1000)) (2 3 a) 5 6)))
(print (my_min '(10 20 30 (-10 -20 -30 a))))
(print (my_min '(10 20 30 (-10 -20 -30 a) (-4000 b c d))))
(print (my_min '(10 20 30 (10 20 30 a) ((((0)))))))
(print (my_min '((a b c d (a (b c d e))))))
