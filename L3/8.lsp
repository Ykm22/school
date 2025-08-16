(defun max_numeric (l)
    (cond
        ((numberp l) l)
        ((atom l) -10000000000)
        (T (apply #'max (mapcar #'max_numeric l)))
    )
)