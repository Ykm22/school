(defun depth_14(l)
    (cond
        ((atom l) 0)
        (t (+ 1 (apply #'max (mapcar #'depth_14 l))))
    )
)