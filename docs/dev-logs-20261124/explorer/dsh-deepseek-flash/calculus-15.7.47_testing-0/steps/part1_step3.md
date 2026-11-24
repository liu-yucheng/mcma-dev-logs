## Step 1.3. Write the order $dz\,dy\,dx$ and check the volume

### Reason
The limits of Step 1.1 put $z$ between two functions of $y$, and $y$ between two functions of $x$. The order $dz\,dy\,dx$ follows the nesting of the limits directly: the inner variable has limits that depend on the outer variables, the middle variable has limits that depend only on $x$, and the outer variable has constant limits.

### Computation
$$V = \int_{-1}^{1} \int_{x^{2}}^{1} \int_{0}^{1 - y} dz\,dy\,dx$$
The integral of $1$ over $z$ gives $1 - y$. The integral of $1 - y$ over $y$ from $x^{2}$ to $1$ gives $\frac{1}{2}(1 - x^{2})^{2}$. The integral of that expression over $x$ gives $\frac{8}{15}$.

### Result
The volume is {{p1_volume}}, and the exact value is $\frac{8}{15}$.
`code/part1_verify.py` computes the same volume in the order $dy\,dz\,dx$ and by a Monte Carlo mean of {{p1_volume_mc}} with standard error {{p1_volume_mc_se}}.
