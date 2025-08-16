(defun apartine(l x)
    (cond
        ((and (atom l)(equal l x)) (list T))
        ((atom l) nil)
        (T (mapcan #'(lambda(y) (apartine y x)) l))
    )
)

(defun my_or(l)
    (cond
        ((equal (car l) T) T)
        ((equal l nil) nil)
        (t (my_or (cdr l)))
        
    )
)

(defun main_apartine(l x)
    (my_or (apartine l x))
)
