;l:list, F:int
;F - 0 if descending
;    1 if ascending
;comparing first 2 elements until list reaches 2 elements
;if E1 < E2 => ascending
;if E1 > E2 => descending
;reaching
(defun vale_aux(l F)
    (cond
        ((and (= (length l) 2) (< (car l) (cadr l))) T)
        ((and (= (length l) 2) (>= (car l) (cadr l))) nil)
        ((and (= F 0) (> (car l) (cadr l))) (vale_aux (cdr l) 0))
        ((and (< (car l) (cadr l))) (vale_aux (cdr l) 1))
        (T nil)
    )
)
;l - list
;validates if the list has > 2 numbers and first 2 are descending then
;calls auxiliary function with flag set to 0 (starting as descending)
(defun vale(l)
    (cond
        ((<= (length l) 2) nil)
        ((< (car l) (cadr l)) nil)
        (T (vale_aux l 0))
    )
)

(print '(t e s t - B))
(print (vale '(5 4 3 2 3 4 5)))
(print (vale '(1 2 3 2 3 4 5)))
(print (vale '(5 4 3 2 1)))
