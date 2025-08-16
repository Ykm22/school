;l - tree with n children: (root (child_1) (child_2) .. (child_n))
;current_depth - depth in tree to check equality with
;depth - number of atoms wanted by this depth  
(defun vertexes_at_depth (l current_depth depth)
    (cond
        ((and (atom l) (= current_depth depth)) 1)
        ((atom l) 0)
        (t (apply '+ (mapcar #'(lambda(x) (vertexes_at_depth x (+ 1 current_depth) depth)) l)))
    )
)

;main function to call auxiliary one, assuming root is depth 0
(defun main_vertexes_at_depth (l depth)
    (vertexes_at_depth l -1 depth)
)

;depth
;0                1
;                / \
;               /   \
;1             2     5
;             / \   / \
;2           3   4 6   7
(print (main_vertexes_at_depth '(1 (2 (3) (4)) (5 (6) (7))) 2))
(print (main_vertexes_at_depth '(1 (2 (3) (4)) (5 (6) (7))) 3))

;depth
;0            ---------a---------
;             |        |        |
;1            b        e        h
;            / \      / \      /
;           /   \    /   \    /
;2         c     d  f     g  i
;                           /
;3                         j
(print (main_vertexes_at_depth '(a (b (c) (d)) (e (f) (g)) (h (i (j)))) 1))
(print (main_vertexes_at_depth '(a (b (c) (d)) (e (f) (g)) (h (i (j)))) 2))
(print (main_vertexes_at_depth '(a (b (c) (d)) (e (f) (g)) (h (i (j)))) 3))
