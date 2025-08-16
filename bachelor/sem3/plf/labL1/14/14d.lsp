;l - list, e - int, found_nr - {0, 1}
;get maximum nr of a linear list
;by comparing each number with e
;and updating it accordingly
;found_nr = 0 => no numbers found yet
;found_nr = 1 => found at least 1 number
(defun max_aux (l e found_nr)
    (cond 
        ((null l) e)

        ((and (= found_nr 0) (numberp (car l))) (max_aux (cdr l) (car l) 1))

        ((and (= found_nr 1) (numberp (car l)) (<= (car l) e)) (max_aux (cdr l) e 1))
        ((and (= found_nr 1) (numberp (car l)) (> (car l) e)) (max_aux (cdr l) (car l) 1))

        ((and (= found_nr 0) (atom e)) (max_aux (cdr l) (car l) 0))
        ((and (= found_nr 1) (atom e)) (max_aux (cdr l) e 1))
        (T (max_aux (cdr l) e found_nr))
    )
)
;l - list
;calling auxiliary function with 2nd argument as first number appearing in list
;and starting with found_nr flag = 0
(defun my_max (l)
    (max_aux (cdr l) (car l) 0)
)
;l - list, e - int
;deleting each appearance of e in l
(defun delete_aux(l e)
    (cond
        ((null l) nil)
        ((and (numberp (car l)) (= (car l) e)) (delete_aux (cdr l) e))
        (T (cons (car l) (delete_aux (cdr l) e)))
    )   
)
;l - list
;calling auxiliary function with 2nd argument as result of my_max(l) function 
(defun delete_main(l)
    (delete_aux l (my_max l))
)

(print '(t e s t - D))
(print (delete_main '(30 30 a b d 30 10 c d 20 30)))
(print (delete_main '(100 a b d 30 100 c d 220 30)))
(print (delete_main '(a b c d e f)))
