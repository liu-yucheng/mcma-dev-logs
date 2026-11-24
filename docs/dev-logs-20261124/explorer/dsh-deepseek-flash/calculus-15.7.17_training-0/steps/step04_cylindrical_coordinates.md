# Step 4 — Use cylindrical coordinates about the $x$ axis

## Reason

The disk $D$ has a polar description, and the integrand of the inner integral depends on $y^{2} + z^{2}$ only. Polar coordinates for $(y, z)$ therefore turn the disk into a rectangle in $(r, \theta)$ and turn the integrand into a function of $r$ alone.

The axis of the solid is the $x$ axis, so the rotation is about $x$. Do not use the $z$ axis here: the paraboloid is not a surface of revolution about $z$.

## Computation

Put

$$
y = r\cos\theta, \qquad z = r\sin\theta, \qquad x = x,
$$

with $r \ge 0$ and $0 \le \theta \le 2\pi$. Then $y^{2} + z^{2} = r^{2}$ and the area element of the disk is

$$
dA = r \, dr \, d\theta .
$$

The factor $r$ is the Jacobian of the map $(r, \theta) \mapsto (y, z)$. The volume element is

$$
dV = r \, dx \, dr \, d\theta .
$$

The bounds become

$$
0 \le \theta \le 2\pi, \qquad 0 \le r \le 1, \qquad 4r^{2} \le x \le 4.
$$

## Result

$$
\iiint_{E} x \, dV
= \int_{0}^{2\pi} \int_{0}^{1} \int_{4r^{2}}^{4} x \, r \; dx \, dr \, d\theta .
$$

## Verification

`code/part2_verify.py` computes the volume of $E$ twice. With the factor $r$ it reports $6.283185307180$, which equals $2\pi$. Without the factor $r$ it reports $16.755160819146$, which is wrong. The factor $r$ is necessary.
