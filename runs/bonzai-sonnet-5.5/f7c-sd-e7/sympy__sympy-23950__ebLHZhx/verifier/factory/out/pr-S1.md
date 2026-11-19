Fix CompoundDistribution dropping the last value of a finite/discrete random parameter

## Overview
A compound distribution whose parameter is a finite random variable (e.g. `Normal('N', Bernoulli('p', 3/4), 1)`) produced a density integrating to 0.75 instead of 1: the last cohort was omitted from the marginalisation.

## Details
`CompoundDistribution._marginalise` summed a discrete/finite parameter from `rv_dom._inf` to `rv_dom._sup - 1`. Sympy `Sum` limits are inclusive, so the final value (e.g. 1 for a Bernoulli) was never included. The upper limit is now `rv_dom._sup`. Infinite domains (Poisson) are unaffected since `oo - 1 == oo`.

Tests: added `test_finite_parameter_CompoundDist_normalised` (density equals the full 3/4, 1/4 mixture and integrates to 1). Existing `test_bernoulli_CompoundDist` (issue 8128: `Bernoulli(Bernoulli(1/2))` gave `{0: 1/2, 1: 0}`) also failed before and passes now.

## Verification
`python -m pytest sympy/stats/tests/test_compound_rv.py`: before fix 2 failed, 5 passed; after fix 7 passed. Full `sympy/stats/tests` run with the fix: all passed apart from my first draft of the new test (integrate() could not simplify erf+erfc, test then changed to a numeric integral).
