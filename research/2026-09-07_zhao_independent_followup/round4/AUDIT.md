# Fourth independent audit: weighted-shadow shortcut

Date: 2026-09-07

Scope: independent audit of the proposed shortcut `theta=-1 => sigma(R)=0` in the `A_p`, `h=p-4` branch. The shortcut itself was withdrawn after audit; this note preserves only the valid identities and the exact failure point.

## Verdict

The shortcut is not valid. The reliable height conclusion remains `h(S) <= p-4`.

Let `R=(g_1,...,g_{4p})`, let `x_j=Z_{3p+j}(R)` for `0<=j<=4`, and assume

`(x_0,x_1,x_2,x_3,x_4) = (1+theta,4theta,6theta,4theta,theta) mod p`.

For each four-position set `B`, define `omega_B in F_p` by

`prod_{i notin B}(1-X^{g_i}) = omega_B J_G`,

and set `W_i = sum_{B contains i} omega_B`.

The valid identities are

- `sum_B omega_B = -theta`;
- `W_i = d_3(i)-4d_4(i) = alpha_i-beta_i`;
- `sum_i W_i = -4 theta`;
- `sum_i W_i g_i = 0` in `F_p^4`.

Thus for `theta=-1`,

`sum_i W_i = 4`, not `0`.

Consequently `theta=-1` cannot imply `W_i=1` for all `i`, because `4p` copies of `1` sum to `0` in `F_p` while the exact shadow identity gives `4`.

If one augments the vectors to `(1,g_i)`, the correct relation is

`sum_i W_i (1,g_i) = (4,0)`,

not zero.

The auxiliary truncation with `z^5=0` does not permit differentiation in the `z` direction for `p>=7`, since `d(z^5)/dz = 5 z^4 != 0` in the quotient. Differentiation in the original group-algebra coordinates remains legitimate.

Finally, the implication

`sigma(R)=0 => contradiction`

is valid: Davenport gives a proper nonempty zero-sum subset of `R`, and its complement is also nonempty zero-sum, so one of the two has length at most `2p <= 3p-2`.

## Generalization to h=p-5

For `r=5`, with

`x_j = 1_{j=0} + theta_0 C(5,j) + theta_1 C(5,j-1) mod p`, 

the analogous top weighted shadow sees only

`c = theta_1-theta_0`,

and the point weight has the form

`W_i = alpha_i-beta_i+gamma_i`.

Therefore a single top shadow loses one global parameter direction and two local directions; it cannot by itself close the two-parameter branch.
