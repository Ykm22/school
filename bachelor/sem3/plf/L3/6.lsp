(defun produs(l)
    (cond
        ((numberp l) l)
        ((atom l) 1)
        (T (apply #'* (mapcar #'produs l)))
    )
)