;l - (root left-subtree right-subtree) tree type
;builds inorder traversal of l
(defun inordine(l) 
    (cond
        ((equal l nil) nil)
        (T (append (inordine (cadr l)) (cons (car l) (inordine (caddr l)))))
    )
)

(print (inordine '(1 (2 (3) (4)) (5))))
         ;1
        ;/ \
       ;2   5
      ;/ \
     ;3   4