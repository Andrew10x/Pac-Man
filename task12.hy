(import [pandas :as pd]
        math
)


(setv dataset (pd.read_csv "output.csv"))
(setv time (get dataset "time"))
(setv score (get dataset "score"))



(defn mathExpect[s]
       (/ (sum s ) (len s))
)

(defn disp [s]
      (setv av (mathExpect s))
      (mathExpect (list (map (fn [x] (** (- x av ) 2)) s)))
)     

(print "Mathematical expectation of time = " (mathExpect time))
(print "Dispersion of the score = " (disp score))