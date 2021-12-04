(import [math [inf]]
        [minimax [minimax GameState genTree]])


(setv maze 
[
[1 1 5 1 0]   
[1 0 0 1 1]   
[1 0 0 2 0]   
[1 1 6 0 0]   
[0 0 0 1 0]])

(setv state (GameState maze))
(setv tree (genTree state (, 2 3)))
(setv bestScore (minimax tree (* -1 inf) inf 2))
(print tree)
(print bestScore)