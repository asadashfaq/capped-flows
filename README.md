Capped-flows and export schemes
============
Comparison of different different export schemes on the European grid:
linear, square, martin, rolando (old capped) and an ensemble of randomised
hours with the rolando scheme.

Now working on generalised flow tracing with vector coloring for each country.

Files:
------
- grid.py: Create a EU grid with all alphas set to 0.7.
- solving.py: solving and plotting of Bc vs. Tc.
- ensemble.py: solving a randomised ensemble of the old capped flow.
- plots.py: Old plotting. Should not be used.
- adv_plotting.py: Making a lot of pretty figures for Martin's paper
- tracer.py: vectorised flow tracing (work in progress)
