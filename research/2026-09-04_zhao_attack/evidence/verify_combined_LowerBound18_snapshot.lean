import Std
set_option maxRecDepth 100000
set_option maxHeartbeats 40000000

-- e_i occur three times; A,D once and B,C twice.
abbrev isZero18 (x1 x2 x3 x4 : Fin 4) (a d : Fin 2) (b c : Fin 3) : Prop :=
  (x1.val + 4*a.val + b.val + c.val + 4*d.val) % 5 = 0 ∧
  (x2.val + a.val + 3*b.val + 3*c.val + 4*d.val) % 5 = 0 ∧
  (x3.val + b.val + d.val) % 5 = 0 ∧
  (x4.val + c.val + d.val) % 5 = 0

theorem noShortZero18 : ∀ x1 x2 x3 x4 : Fin 4, ∀ a d : Fin 2, ∀ b c : Fin 3,
    isZero18 x1 x2 x3 x4 a d b c →
    (x1.val+x2.val+x3.val+x4.val+a.val+b.val+c.val+d.val = 0 ∨
     14 ≤ x1.val+x2.val+x3.val+x4.val+a.val+b.val+c.val+d.val) := by
  decide

#print axioms noShortZero18
