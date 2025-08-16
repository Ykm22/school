;l - arg (nr/atom/list)
;sum of all nr's in a list(including sublists)
(defun my_sum(l)
    (cond
        ((numberp l) l)
        ((atom l) 0)
        (T (apply #'+ (mapcar #'my_sum l)))
    )
)