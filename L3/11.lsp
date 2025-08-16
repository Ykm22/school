(defun delete_all_appearances(l e)
    (cond
        ((equal l e) nil)
        ((atom l) l)
        ;((atom l) (list l))
        (T (mapcar #'(lambda(x) (delete_all_appearances x e)) l))
        ;(T (mapcan #'(lambda(x) (delete_all_appearances x e)) l))

    )
)

(defun remove_nil(l)
    (cond
        ((equal l nil) nil)
        ((equal (car l) nil) (remove_nil (cdr l)))
        ((atom (car l)) (cons (car l) (remove_nil (cdr l))))
        (t (list (remove_nil (car l))))
    )
)