Fix CompoundDistribution dropping the last value of a finite/discrete random parameter

## Overview
A compound distribution whose parameter is a finite or discrete random variable lost the last value of that parameter's support, so the density no longer integrated to 1. For `Normal('Y', Bernoulli('X', 1/4), 1)` the `X=1` cohort vanished and the density integrated to 3/4.

## Cause
`CompoundDistribution._marginalise` summed over `(rv, rv_dom._inf, rv_dom._sup - 1)`. For finite/discrete domains `_sup` is already the largest value, so `- 1` excluded it. The continuous branch correctly uses `_sup`.

## Fix
Use `rv_dom._sup` as the upper limit of the Sum.

## Verification
- Added `test_finite_param_CompoundDist_normalised` (Bernoulli and Die means: exact density for the Bernoulli case, integral of density is 1).
- `python -m pytest sympy/stats/tests/test_compound_rv.py -q -p no:warnings`: before the fix 2 failed (new test and existing `test_bernoulli_CompoundDist`), after: 7 passed.
- Before the fix the Bernoulli density was `3*sqrt(2)*exp(-x**2/2)/(8*sqrt(pi))` (integral 0.75); after it also has the `sqrt(2)*exp(-(x-1)**2/2)/(8*sqrt(pi))` term (integral 1.0).
