import Std
set_option maxRecDepth 100000
set_option maxHeartbeats 20000000

abbrev reprCore (x y z : Fin 5) (a b c t : Fin 4) : Prop :=
  (a.val + t.val) % 5 = x.val ∧
  (b.val + 2 * t.val) % 5 = y.val ∧
  (c.val + 3 * t.val) % 5 = z.val

theorem core_cover9 : ∀ x y z : Fin 5,
    (x.val = 1 ∧ y.val = 4 ∧ z.val = 2) ∨
    ∃ a b c t : Fin 4, reprCore x y z a b c t ∧
      a.val + b.val + c.val + t.val ≤ 9 := by
  decide

theorem core_cover8 : ∀ x y z : Fin 5,
    ((x.val = 1 ∧ y.val = 4 ∧ z.val = 2) ∨
     (x.val = 4 ∧ y.val = 0 ∧ z.val = 0) ∨
     (x.val = 0 ∧ y.val = 4 ∧ z.val = 0) ∨
     (x.val = 0 ∧ y.val = 0 ∧ z.val = 4) ∨
     (x.val = 4 ∧ y.val = 3 ∧ z.val = 2)) ∨
    ∃ a b c t : Fin 4, reprCore x y z a b c t ∧
      a.val + b.val + c.val + t.val ≤ 8 := by
  decide

#print axioms core_cover9
#print axioms core_cover8
