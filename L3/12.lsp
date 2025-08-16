(defun replace_vertex(l v replacement)
    (cond
        ((equal l v) replacement)
        ((atom l) l)
        (t (mapcar #'(lambda(x) (replace_vertex x v replacement)) l))
    )
)