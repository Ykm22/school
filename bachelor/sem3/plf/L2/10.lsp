;x - node, l - (root left-subtree right-subtree) type list
;finds a node x in the l tree
(defun my_traverse (x l current_depth)
    (cond 
        ((equal (car l) x) current_depth)
        ((equal (car l) nil) nil)
        (T (or (my_traverse x (cadr l) (+ current_depth 1)) (my_traverse x (caddr l) (+ current_depth 1))))
    )
)

;x - node, l - (root left-subtree right-subtree) type list
;finding depth of a node in l
;root considered depth = 0
(defun depth(x l)
    (my_traverse x l 0)
)

(print (depth 2 '(1 (3 (2) ()) (3))))
(print (depth 10 '(1 (3 (2) ()) (3 (4 () (10)) (5)))))
(print (depth 'd '(a (c (b) ()) (c (d () (z)) (f)))))