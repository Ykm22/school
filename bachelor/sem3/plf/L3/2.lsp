(defun delist(l)
    (cond 
        ((atom l) (list l))
        (t (mapcan #'delist l))
    )
)