(defun left-tree-aux(l v e)
    (cond
        ((= (+ 1 e) v) nil)
        ((null l) nil)
        (t (cons (car l) (cons (cadr l) (left-tree-aux (cddr l) (+ 1 v) (+ (cadr l) e)))))
    )
)

(defun left-tree(l)
    (left-tree-aux (cddr l) 0 0)
)

(defun right-tree-aux(l v e)    
    (cond
        ((= (+ 1 e) v) l)
        ((null l) nil)
        (t (right-tree-aux (cddr l) (+ 1 v) (+ (cadr l) e)))
    )
)

(defun right-tree(l)
    (right-tree-aux (cddr l) 0 0)
)

(defun my_find(l v)
    (cond
        ((equal l nil) nil)
        ((equal (car l) v) T)
        (t (or (my_find (left-tree l) v) (my_find (right-tree l) v)))
    )
)

(defun depth-aux(l v current-depth)
    (cond
        ((equal (car l) v) current-depth)
        ((my_find (left-tree l) v) (depth-aux (left-tree l) v (+ current-depth 1)))
        ((my_find (right-tree l) v) (depth-aux (right-tree l) v (+ current-depth 1)))
    )
)

;depth of a vertex with root having depth 0
;type of tree (a 2 b 0 c 1 d 1 e 0)
;       a
;     /  \
;    b    c
;        /
;       d
;      /
;     e
(defun depth(l v)
    (depth-aux l v 0)
)

