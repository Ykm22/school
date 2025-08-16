(defun nr_atoms(l)
    (cond
        ((atom l) 1)
        (t (apply '+ (mapcar #'nr_atoms l)))
    )
)