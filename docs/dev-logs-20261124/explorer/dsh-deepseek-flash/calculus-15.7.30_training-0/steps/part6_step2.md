### Step 6.2 — One bound rule that produces all six limit sets

**Reason.** Six separate derivations hide a mistake. One rule that covers every order shows why the
six limit sets agree.

**Computation.** The solid has two kinds of surface. The planes fix $x$ between two constants, and
the cylinder relates $y$ and $z$ only to each other. Hence the rule: the bounds of $x$ are always
$-2$ and $2$; the bounds of $y$ are $-3$ and $3$, or the two halves of the cylinder at the fixed
value of $z$; the bounds of $z$ are $-3$ and $3$, or the two halves of the cylinder at the fixed
value of $y$. The variable of the pair $y,z$ that is integrated first takes the cylinder bound, and
the other one takes the constant bound.

**Result.** Applied to the six permutations, the rule gives the six limit sets of Step 5.2. In the
orders with $x$ outermost the inner limits depend on $y$ or on $z$. In the orders with $y$ or $z$
outermost the inner limits may depend on the outer variable.

**Verification.** The script `code/part6_verify.py` builds the six limit sets from this rule only. It
reports that each set accepts exactly the $15728$ points of $E$ in the random sample and rejects the
$4272$ points of the bounding box that lie outside $E$, and it reports $36\pi$ for $f=1$ in every
order.
