;x - node, l - (root left-subtree right-subtree) type list
;finds a node x in the l tree
(defun my_find (x l)
    (cond 
        ((equal (car l) x) T)
        ((equal (car l) nil) nil)
        (T (or (my_find x (cadr l)) (my_find x (caddr l))))
    )
)

;x - node, l - (root left-subtree right-subtree) type list
;builds the path from root to node x
;tries to find the node in either left or right sub-tree
;and proceeds with building accordingly
(defun cale (x l)
    (cond
        ((equal (car l) x) (list x))
        ((my_find x (cadr l)) (cons (car l) (cale x (cadr l))))
        ((my_find x (caddr l)) (cons (car l) (cale x (caddr l))))
    )
)
         ;A
        ;/ \
       ;B   E
      ;/ \
     ;F   D
      ;\
      ; C
(print (cale 'd '(a (b (f () (c)) (d)) (e))))
(print (cale 'c '(a (b (f () (c)) (d)) (e))))
(print (cale 'z '(a (b (f () (c)) (d)) (e))))   
         ;1
        ;/ \
       ;2   5
      ;/ \
     ;6   4
      ;\
      ; 3
(print (cale 3 '(1 (2 (6 () (3)) (4)) (5))))
