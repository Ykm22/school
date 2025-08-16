(defun find_depth_in_rez(depth rez)
    (cond
        ((equal rez nil) nil)
        ((equal (caar rez) depth) T)
        (T (find_depth_in_rez depth (cdr rez)))
    )
)

(defun add_to_rez(depth rez x)
    (cond
        ((not (equal (caar rez) depth)) (cons (car rez) (add_to_rez depth (cdr rez) x)))
        (T (cons (list (caar rez) (append (cadar rez) (list x))) (cdr rez) ))
    )
)
         ;1
        ;/ \
       ;/   \
      ;2     3
     ;/ \   / \
    ;4   5 6   7
;L = (1 (2 (4) (5)) (3 (6) (7)) ) )
;rez = ((0 (1)) (1 (2 3)) (2 (4 5 6 7)))

(defun find_depth (depth depth_list)
    (cond
        ((equal depth_list nil) nil)
        ((equal depth (car depth_list)) T)
        (T (find_depth depth (cdr depth_list)))
    )   
)

(defun build_rez(current_depth l rez depth_list)
    (cond
        ((equal l nil) )
        ((find_depth current_depth depth_list) (and
            (build_rez (+ current_depth 1) (cadr l) (add_to_rez current_depth rez (car l)) depth_list) 
            (build_rez (+ current_depth 1) (caddr l) (add_to_rez current_depth rez (car l)) depth_list)
                                                )
        )
        (T (and  

                ;s(print rez)
                ;(print (car l)) (print current_depth) 
                (build_rez (+ current_depth 1) (cadr l) (append rez (list (list current_depth (list (car l))))) (cons (car l) depth_list))
                ;(print rez) (print current_depth) (print (car l))
                (build_rez (+ current_depth 1) (caddr l) (append rez (list (list current_depth (list (car l))))) (cons (car l) depth_list))
                ;(print rez) (print current_depth) (print (car l)) 
            )
        )
    )
)