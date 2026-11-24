## Step 5.1 — Cross-check every quantity and read the three answers

**Reason.** The statement asks for three decimal places, so each answer must be safe in its third decimal. A single integration route cannot show that, because a wrong set of limits or a wrong power would pass through one route unnoticed. The lesson of Step 2.2 shows the danger: the wrong limit on $x$ gives a mass of ${{mass_without_plane}}$, and only a second route, or a wrong-value check, shows that this value cannot be the mass. A reader may take the printed value of a script for the answer, but the answer needs a second route that uses different limits and a sample that uses no limits at all. The script `code/part5_verify.py` builds both.

**Computation.** The script reads the values that the earlier scripts wrote, recomputes every integral in the order $dz\,dy\,dx$, and draws a fresh uniform sample of the box. For each quantity it prints the printed value, the value of the second order, the value of the sample, and the deviation of the sample in standard errors. The printed rows are

{{table:final}}

Every relative difference between the printed value and the second order is below ${{relative_difference_limit_latex}}$, and every sample value lies within four standard errors of the printed value. The largest relative difference of the five rows is ${{worst_relative_difference_latex}}$. The largest deviation is ${{worst_sigma}}$ standard errors.

**Verification.** The scripts of the five parts report the following check counts.

{{table:checks}}

The four earlier parts print ${{earlier_check_total}}$ checks, and `code/part5_verify.py` adds its own rows, so the tutorial rests on ${{total_checks}}$ checks in total. Every check compares a value that one method computes with a value that a different method computes.

**Result.** The three answers, to three decimal places, are

$$ \text{(a)}\quad M = {{final_mass}}, \qquad \text{(b)}\quad \left(\bar{x}, \bar{y}, \bar{z}\right) = \left({{final_x}},\ {{final_y}},\ {{final_z}}\right), \qquad \text{(c)}\quad I_{z} = {{final_iz}} . $$
