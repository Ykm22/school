(defun my_substitute (l x y)
    (cond
        ((equal l x) y)
        ((atom l) l)
        (t (mapcar #'(lambda(l) (my_substitute l x y)) l))
    )
)