;l - list, k - int, n - int
;eliminating elements n by n from l
(defun elim_aux(l k n)
    (cond
        ((null l) nil)
        ((= k 1) (elim_aux (cdr l) n n))
        (T (cons (car l) (elim_aux (cdr l) (- k 1) n)))
    )   

)
;l - list, n - int
;calling auxiliary elim function with starting k as n
(defun elim(l n)
    (elim_aux l n n)    
)

(print '(t e s t - A))
(print (elim '(1 2 3 4 5 6 7 8) 3))
(print (elim '(1 2 3 4 a b c d) 3))
