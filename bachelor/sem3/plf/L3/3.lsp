(defun my_contains (l x)
    (cond
        ((equal l x) (list T))
        ((atom l) nil)
        (T (mapcan #'(lambda(y) (my_contains y x)) l))
    )
)

(defun my_or(l)
    (cond
        ((equal (car l) T) T)
        ((equal l nil) nil)
        (t (my_or (cdr l)))
        
    )
)

(defun main_contains(l x)
    (my_or (my_contains l x ))
)
