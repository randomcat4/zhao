import Std

-- Only exact arithmetic certificates in the analytic proof are formalized.
-- This file does NOT formalize the entropy, coding, or zero-sum theorems.
example : (5 : Nat)^25 > 2^58 := by decide
example : (10 : Nat)^70 > 2^60 * 3^21 * 7^49 := by decide
example : (223 : Nat) * (8192 + 1) < 2^21 := by decide
example : (8192 : Nat) > 200 * (4 + 21) := by decide
example : (17 : Nat) * 223 > 3775 := by decide
