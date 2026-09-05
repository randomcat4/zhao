import Std

-- Only the integer arithmetic after projection and x+k=n is formalized.
-- The group argument and cited external theorems are not encoded here.
theorem paired_length_lower (n r j x k : Nat)
    (hn : r ≤ n) (hj : j < r)
    (hx : x ≤ n - 1 - j) (hs : x + k = n) :
    n + j + 1 ≤ x + 2 * k := by
  omega

theorem paired_sum_range (n r j x k : Nat)
    (hn : r ≤ n) (hj : j < r)
    (hx : x ≤ n - 1 - j) (hk : k ≤ r) (hp : 1 ≤ k) :
    0 < x + k ∧ x + k < 2 * n := by
  omega

#print axioms paired_length_lower
#print axioms paired_sum_range
