(defun my_reverse(l)
    (cond
        ((atom l) l)
        (t (mapcar #'my_reverse (reverse_for_list l)))
    )
)

(defun reverse_for_list(l)
    (cond
        ((equal l nil) nil)
        (t (append (reverse_for_list (cdr l)) (list (car l))))    
    )
)
