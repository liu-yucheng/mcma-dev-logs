"""The text of every step of the tutorial, and the figure and verification records.

The module holds one entry for each step. A step gives its reason before its computation and
states its result. Each part names the figure that helps the reader and the script that
verifies the part. The composed page and the step files read the same text, so the page and
the files cannot disagree.
"""

from __future__ import annotations

# The statement of the problem, quoted from the source image.
STATEMENT = (
    "Express the integral $\\iiint_E f(x, y, z)\\, dV$ as an iterated integral in six "
    "different ways, where $E$ is the solid bounded by the given surfaces, "
    "$y = 4 - x^{2} - 4z^{2}$ and $y = 0$."
)

# The note about the figures.
FIGURE_NOTE = (
    "The source image holds no figure. Every figure of this page is a product of this "
    "workspace, and every figure was drawn by the script that the page names."
)

# One entry for each part.
PARTS = (
    {
        "number": 1,
        "title": "Read the solid from the two equations",
        "goal": (
            "Turn the two surface equations into one inequality chain, then read the base and "
            "the top of the solid from that chain. No figure takes part in this reading."
        ),
        "verify_script": "code/part1_verify.py",
        "figures": (("part1_figure1.png", "Figure 1. The body, and the section at $z = 0$."),),
        "steps": (
            {
                "number": "1.1",
                "title": "The inequality chain on $y$",
                "reason": (
                    "Both surfaces have the form $y = g(x, z)$. A vertical line therefore "
                    "meets the solid once, between the lower surface and the upper surface. "
                    "The chain follows from the two equations alone."
                ),
                "computation": (
                    "The upper surface is $y = 4 - x^{2} - 4z^{2}$ and the lower surface is "
                    "$y = 0$. A point belongs to $E$ when its height lies between them:\n\n"
                    "$$E = \\{(x, y, z) : 0 \\leq y \\leq 4 - x^{2} - 4z^{2}\\}.$$\n\n"
                    "The coefficient on $z^{2}$ is $4$, not $1$. The chain is not empty: "
                    "$x^{2} + 4z^{2} \\geq 0$, so the upper bound is never below the lower "
                    "bound, and the point $(0, 0, 0)$ belongs to $E$."
                ),
                "result": (
                    "Every bound of every order comes from this one chain. The chain is the "
                    "single source of the six answers."
                ),
                "verify": (
                    "`code/part1_verify.py` compares two membership tests: the direct chain, "
                    "and the substitution $x = 2u$, $z = w$, $y = 4s$, which maps $E$ onto the "
                    "unit disk times the unit interval. On 200 000 random points the two tests "
                    "give 0 disagreements."
                ),
            },
            {
                "number": "1.2",
                "title": "The trace on the plane $y = 0$",
                "reason": (
                    "The lower wall is the plane $y = 0$. A point of that plane belongs to the "
                    "solid exactly when the upper bound at its position is not negative."
                ),
                "computation": (
                    "Set $y = 0$ in the chain: $0 \\leq 4 - x^{2} - 4z^{2}$, which is the same "
                    "statement as\n\n"
                    "$$x^{2} + 4z^{2} \\leq 4.$$\n\n"
                    "This is an ellipse with semi-axis $2$ along $x$ and semi-axis $1$ along "
                    "$z$. Its area is $\\pi \\cdot 2 \\cdot 1 = 2\\pi = 6.283185307$. The four "
                    "extreme points are $(\\pm 2, 0, 0)$ and $(0, 0, \\pm 1)$."
                ),
                "result": (
                    "The base of the solid is a filled ellipse of area $2\\pi$. The solid stands "
                    "on the plane $y = 0$."
                ),
                "verify": (
                    "`code/part1_verify.py` compares a quadrature of the base area with the "
                    "product of the two semi-axes, and both with a Monte Carlo estimate that "
                    "carries its standard error. The three values agree within one standard "
                    "error."
                ),
            },
            {
                "number": "1.3",
                "title": "The top of the solid, and the closure of the boundary",
                "reason": (
                    "The statement names two surfaces. A reader must check from the equations "
                    "that no third wall exists, and must find the largest height."
                ),
                "computation": (
                    "The upper bound $4 - x^{2} - 4z^{2}$ is largest where $x = 0$ and $z = 0$. "
                    "There it equals $4$. So the largest height is $y = 4$, at the single point "
                    "$(0, 4, 0)$.\n\n"
                    "The boundary closes because the upper bound falls to $0$ on the ellipse "
                    "$x^{2} + 4z^{2} = 4$, where the paraboloid meets the base. Above that "
                    "ellipse the upper bound is negative, so no point of the solid lies there."
                ),
                "result": (
                    "The solid has exactly two pieces of boundary: the paraboloid, and the "
                    "filled ellipse on the plane $y = 0$. Its largest height is $4$, reached at "
                    "one point."
                ),
                "verify": (
                    "`code/part1_verify.py` casts 400 rays from interior points and records "
                    "where each ray leaves the solid. Every exit lies on the plane $y = 0$ or "
                    "on the paraboloid, with a residual below $1.4 \\times 10^{-15}$. No ray "
                    "leaves through a third surface. The same script compares the largest "
                    "height of a grid with the value $4$ of the apex."
                ),
            },
        ),
    },
    {
        "number": 2,
        "title": "The projection on the plane $y = 0$ and the sections at a fixed height",
        "goal": (
            "Describe the projection that the two orders with an outer integral in $x$ or in "
            "$z$ need, and describe the section at a fixed height."
        ),
        "verify_script": "code/part2_verify.py",
        "figures": (
            ("part2_figure1.png",
             "Figure 2. The projection $D$ on the plane $y = 0$, and three sections at fixed "
             "heights."),
            ("part2_figure2.png",
             "Figure 3. The corner list of each section, which decides its shape."),
        ),
        "steps": (
            {
                "number": "2.1",
                "title": "The outline of the projection",
                "reason": (
                    "A projection drops the coordinate that the plane does not keep. Here the "
                    "coordinate $y$ drops. A position $(x, z)$ belongs to the projection when "
                    "at least one height $y$ belongs to the solid at that position."
                ),
                "computation": (
                    "The chain allows a height at $(x, z)$ exactly when $4 - x^{2} - 4z^{2} "
                    "\\geq 0$. So the projection is\n\n"
                    "$$D = \\{(x, z) : x^{2} + 4z^{2} \\leq 4\\}$$\n\n"
                    "on the plane $y = 0$, with area $2\\pi$. The projection keeps the "
                    "coordinates $x$ and $z$, so its plane is $y = 0$."
                ),
                "result": (
                    "The projection is one filled ellipse. It is the same set as the base, "
                    "because the tallest wall stands directly above the base."
                ),
                "verify": (
                    "`code/part2_verify.py` compares three descriptions of $D$: the inequality, "
                    "a sweep in $x$, and a sweep in $z$. On 200 000 random points of the plane "
                    "$y = 0$ the three descriptions give 0 disagreements."
                ),
            },
            {
                "number": "2.2",
                "title": "The section at a fixed height",
                "reason": (
                    "At a fixed height $y$ the section is the set of positions where the upper "
                    "bound reaches at least that height. The section is a set in a plane of "
                    "constant $y$, so it keeps the coordinates $x$ and $z$."
                ),
                "computation": (
                    "Set $y$ to a constant in the chain: $x^{2} + 4z^{2} \\leq 4 - y$. This is a "
                    "filled ellipse with semi-axes $\\sqrt{4 - y}$ and $\\frac{1}{2}\\sqrt{4 - "
                    "y}$, so its area is\n\n"
                    "$$A(y) = \\pi \\cdot \\sqrt{4 - y} \\cdot \\frac{\\sqrt{4 - y}}{2} = "
                    "\\frac{\\pi (4 - y)}{2}.$$\n\n"
                    "The section is filled, not a ring: the inequality has the form "
                    "$x^{2} + 4z^{2} \\leq$ a number, so it holds at the center $(0, y, 0)$ and "
                    "along every radial line from the center to the outline."
                ),
                "result": (
                    "The area falls from $2\\pi = 6.283185307$ at $y = 0$ to $0$ at $y = 4$. At "
                    "$y = 2$ the area is $\\pi = 3.141592654$."
                ),
                "verify": (
                    "`code/part2_verify.py` measures the area at seven heights by three methods: "
                    "a quadrature of the half width, the ellipse formula with the measured "
                    "semi-axes, and the closed form $\\pi (4 - y)/2$. The largest difference is "
                    "below $1.1 \\times 10^{-14}$. The same script walks 720 radial directions "
                    "at the heights $0$, $2$, and $3.9$ and tests a point at half the radius: a "
                    "ring would fail that test, and it never fails."
                ),
            },
            {
                "number": "2.3",
                "title": "The section at each boundary value of $y$",
                "reason": (
                    "A formula for the semi-axes returns $0$ at $y = 4$. A reader must read the "
                    "printed corner list before naming any shape, because a shape with equal "
                    "corners is not an ellipse."
                ),
                "computation": (
                    "The script prints the four extreme points of the section at each height.\n\n"
                    "At $y = 0$ the corners are $(2, 0, 0)$, $(-2, 0, 0)$, $(0, 0, 1)$, and "
                    "$(0, 0, -1)$: four distinct positions, so the section is a filled "
                    "ellipse.\n\n"
                    "At $y = 2$ the corners are $(\\sqrt{2}, 2, 0)$, $(-\\sqrt{2}, 2, 0)$, "
                    "$(0, 2, \\sqrt{2}/2)$, and $(0, 2, -\\sqrt{2}/2)$: four distinct positions, "
                    "so the section is a filled ellipse.\n\n"
                    "At $y = 4$ the four corners coincide at $(0, 4, 0)$: one position, so the "
                    "section is a single point."
                ),
                "result": (
                    "The section is a filled ellipse for $0 \\leq y < 4$, and a single point at "
                    "$y = 4$. The collapse happens first at the top of the solid, and nowhere "
                    "else."
                ),
                "verify": (
                    "`code/part2_verify.py` prints the corner list of each section and counts "
                    "the distinct positions. It also counts the points of a grid of $2001$ by "
                    "$2001$ positions at $y = 4$ that belong to the section, and the count is "
                    "exactly $1$."
                ),
            },
        ),
    },
    {
        "number": 3,
        "title": "The two orders with the inner integral in $y$",
        "goal": (
            "Write the two orders whose innermost differential is $dy$, and check each one "
            "against the exact value of a test integral."
        ),
        "verify_script": "code/part3_verify.py",
        "figures": (),
        "steps": (
            {
                "number": "3.1",
                "title": "The order $dy\\,dz\\,dx$",
                "reason": (
                    "The chain gives the limits in $y$ at once, for each position in the "
                    "projection. The remaining two integrals run over the projection $D$, and "
                    "the outer one is the widest."
                ),
                "computation": (
                    "At a fixed $(x, z)$ the chain reads $0 \\leq y \\leq 4 - x^{2} - 4z^{2}$. "
                    "Then $(x, z)$ runs over $D$, where $x$ is the widest variable: $x$ from "
                    "$-2$ to $2$, and at a fixed $x$ the variable $z$ runs from "
                    "$-\\frac{1}{2}\\sqrt{4 - x^{2}}$ to $\\frac{1}{2}\\sqrt{4 - x^{2}}$. Hence\n\n"
                    "$$\\iiint_E f\\, dV = \\int_{-2}^{2} \\int_{-\\sqrt{4 - x^{2}}/2}^{"
                    "\\sqrt{4 - x^{2}}/2} \\int_{0}^{4 - x^{2} - 4z^{2}} f(x, y, z)\\, dy\\, dz"
                    "\\, dx.$$\n\n"
                    "The order is not the order $dz\\,dy\\,dx$: here the innermost integral is "
                    "the one in $y$, and the outermost is the one in $x$."
                ),
                "result": (
                    "The first form. For $f = 1$ its value is $4\\pi = 12.566370614$."
                ),
                "verify": (
                    "`code/part3_verify.py` compares the adaptive quadrature of this form with "
                    "the exact value $4\\pi$ from `code/exact_integrals.py`, and with the exact "
                    "value $16\\pi/3$ of the integral of $f = y$. It also compares the printed "
                    "limits with the defining inequality in both directions."
                ),
            },
            {
                "number": "3.2",
                "title": "The order $dy\\,dx\\,dz$",
                "reason": (
                    "The inner integral still runs in $y$, so its limits do not change. Only the "
                    "two outer integrals change place, and the wider of the two variables must "
                    "be the outer one."
                ),
                "computation": (
                    "The projection is $x^{2} + 4z^{2} \\leq 4$. Sweep $z$ first: $z$ lies "
                    "between $-1$ and $1$, and at a fixed $z$ the variable $x$ runs between "
                    "$-2\\sqrt{1 - z^{2}}$ and $2\\sqrt{1 - z^{2}}$. Hence\n\n"
                    "$$\\iiint_E f\\, dV = \\int_{-1}^{1} \\int_{-2\\sqrt{1 - z^{2}}}^{"
                    "2\\sqrt{1 - z^{2}}} \\int_{0}^{4 - x^{2} - 4z^{2}} f(x, y, z)\\, dy\\, dx"
                    "\\, dz.$$"
                ),
                "result": (
                    "The second form. Its value for $f = 1$ is $4\\pi$, the same as the first "
                    "form."
                ),
                "verify": (
                    "`code/part3_verify.py` compares this form with the exact values $4\\pi$ and "
                    "$16\\pi/3$, and compares its limits with the defining inequality in both "
                    "directions."
                ),
            },
        ),
    },
    {
        "number": 4,
        "title": "The two orders with the inner integral in $z$",
        "goal": (
            "Write the two orders whose innermost differential is $dz$, and decide whether the "
            "outer range needs a split."
        ),
        "verify_script": "code/part4_verify.py",
        "figures": (
            ("part4_figure1.png",
             "Figure 4. The shadow of the solid on a plane of constant $z$."),
        ),
        "steps": (
            {
                "number": "4.1",
                "title": "The interval in $z$, and the question of a split",
                "reason": (
                    "When the innermost integral is the one in $z$, the limits follow from the "
                    "chain solved for $z$. A split is necessary only when the remaining region "
                    "has two separate pieces at one value of the outer variable."
                ),
                "computation": (
                    "Solve the chain for $z$: $4z^{2} \\leq 4 - x^{2} - y$, so\n\n"
                    "$$-\\frac{1}{2}\\sqrt{4 - x^{2} - y} \\leq z \\leq \\frac{1}{2}"
                    "\\sqrt{4 - x^{2} - y}.$$\n\n"
                    "The full width in $z$ is $\\sqrt{4 - x^{2} - y}$. The remaining variables "
                    "$(x, y)$ run over the set $0 \\leq y \\leq 4 - x^{2}$. At a fixed $x$ that "
                    "set is one interval in $y$, so no split is needed."
                ),
                "result": (
                    "The interval in $z$ is one interval, and the region of $(x, y)$ is one "
                    "piece at every $x$. Neither of the two orders needs a split."
                ),
                "verify": (
                    "`code/part4_verify.py` finds the half width in $z$ by a root search on the "
                    "upper surface and compares it with the closed form "
                    "$\\sqrt{4 - x^{2} - y}/2$ at five positions. It then walks a line across "
                    "the region of $(x, y)$ at 41 positions of $x$ and counts the separate runs: "
                    "the count is $1$ everywhere."
                ),
            },
            {
                "number": "4.2",
                "title": "The order $dz\\,dy\\,dx$",
                "reason": (
                    "The inner limits come from step 4.1. The middle integral runs in $y$ at a "
                    "fixed $x$, and the outer integral runs in $x$ over the widest range."
                ),
                "computation": (
                    "For a fixed $x$ the variable $y$ runs from $0$ to $4 - x^{2}$. Hence\n\n"
                    "$$\\iiint_E f\\, dV = \\int_{-2}^{2} \\int_{0}^{4 - x^{2}} "
                    "\\int_{-\\sqrt{4 - x^{2} - y}/2}^{\\sqrt{4 - x^{2} - y}/2} f(x, y, z)\\, dz"
                    "\\, dy\\, dx.$$"
                ),
                "result": (
                    "The third form. Its value for $f = 1$ is $4\\pi$. For $f = x^{2}$ its "
                    "value is $8\\pi/3 = 8.377580410$."
                ),
                "verify": (
                    "`code/part4_verify.py` compares this form with the exact values $4\\pi$ and "
                    "$8\\pi/3$ from `code/exact_integrals.py`, and compares its limits with the "
                    "defining inequality in both directions."
                ),
            },
            {
                "number": "4.3",
                "title": "The order $dz\\,dx\\,dy$",
                "reason": (
                    "The inner integral still runs in $z$. The outer variable is now $y$, "
                    "because $y$ runs over the full height of the solid and $x$ is narrower at "
                    "each height."
                ),
                "computation": (
                    "The height runs from $0$ to $4$. At a fixed height the variable $x$ runs "
                    "from $-\\sqrt{4 - y}$ to $\\sqrt{4 - y}$. Hence\n\n"
                    "$$\\iiint_E f\\, dV = \\int_{0}^{4} \\int_{-\\sqrt{4 - y}}^{\\sqrt{4 - y}} "
                    "\\int_{-\\sqrt{4 - y - x^{2}}/2}^{\\sqrt{4 - y - x^{2}}/2} f(x, y, z)\\, dz"
                    "\\, dx\\, dy.$$"
                ),
                "result": (
                    "The fourth form. Its value for $f = 1$ is $4\\pi$, the same as the third "
                    "form."
                ),
                "verify": (
                    "`code/part4_verify.py` compares this form with the exact values $4\\pi$ and "
                    "$8\\pi/3$, and compares its limits with the defining inequality in both "
                    "directions."
                ),
            },
        ),
    },
    {
        "number": 5,
        "title": "The two orders with the inner integral in $x$",
        "goal": (
            "Write the two orders whose innermost differential is $dx$, and decide whether the "
            "outer range needs a split."
        ),
        "verify_script": "code/part5_verify.py",
        "figures": (
            ("part5_figure1.png",
             "Figure 5. The shadow of the solid on a plane of constant $x$."),
        ),
        "steps": (
            {
                "number": "5.1",
                "title": "The interval in $x$, and the question of a split",
                "reason": (
                    "When the innermost integral is the one in $x$, the limits follow from the "
                    "chain solved for $x$. A split is necessary only when the remaining region "
                    "has two separate pieces at one value of the outer variable."
                ),
                "computation": (
                    "Solve the chain for $x$: $x^{2} \\leq 4 - y - 4z^{2}$, so\n\n"
                    "$$-\\sqrt{4 - y - 4z^{2}} \\leq x \\leq \\sqrt{4 - y - 4z^{2}}.$$\n\n"
                    "The full width in $x$ is $2\\sqrt{4 - y - 4z^{2}}$. The remaining "
                    "variables $(y, z)$ run over the set $0 \\leq y \\leq 4 - 4z^{2}$ and "
                    "$-1 \\leq z \\leq 1$. At a fixed $z$ that set is one interval in $y$, so no "
                    "split is needed."
                ),
                "result": (
                    "The interval in $x$ is one interval, and the region of $(y, z)$ is one "
                    "piece at every $z$. Neither of the two orders needs a split."
                ),
                "verify": (
                    "`code/part5_verify.py` finds the half width in $x$ by a root search on the "
                    "upper surface and compares it with the closed form "
                    "$\\sqrt{4 - y - 4z^{2}}$ at six positions. It then walks a line across the "
                    "region of $(y, z)$ at 41 positions and counts the separate runs: the count "
                    "is $1$ everywhere."
                ),
            },
            {
                "number": "5.2",
                "title": "The order $dx\\,dz\\,dy$",
                "reason": (
                    "The inner limits come from step 5.1. The middle integral runs in $z$ at a "
                    "fixed height, and the outer integral runs in $y$ over the full height."
                ),
                "computation": (
                    "At a fixed height $y$ the variable $z$ runs from "
                    "$-\\frac{1}{2}\\sqrt{4 - y}$ to $\\frac{1}{2}\\sqrt{4 - y}$. Hence\n\n"
                    "$$\\iiint_E f\\, dV = \\int_{0}^{4} \\int_{-\\sqrt{4 - y}/2}^{"
                    "\\sqrt{4 - y}/2} \\int_{-\\sqrt{4 - y - 4z^{2}}}^{\\sqrt{4 - y - 4z^{2}}} "
                    "f(x, y, z)\\, dx\\, dz\\, dy.$$"
                ),
                "result": (
                    "The fifth form. Its value for $f = 1$ is $4\\pi$. For $f = z^{2}$ its "
                    "value is $2\\pi/3 = 2.094395102$."
                ),
                "verify": (
                    "`code/part5_verify.py` compares this form with the exact values $4\\pi$ and "
                    "$2\\pi/3$ from `code/exact_integrals.py`, and compares its limits with the "
                    "defining inequality in both directions."
                ),
            },
            {
                "number": "5.3",
                "title": "The order $dx\\,dy\\,dz$",
                "reason": (
                    "The inner integral still runs in $x$. The outer variable is now $z$, "
                    "because $z$ runs over the full width of the base and $y$ is narrower at "
                    "each $z$."
                ),
                "computation": (
                    "The variable $z$ runs from $-1$ to $1$. At a fixed $z$ the height $y$ runs "
                    "from $0$ to $4 - 4z^{2}$. Hence\n\n"
                    "$$\\iiint_E f\\, dV = \\int_{-1}^{1} \\int_{0}^{4 - 4z^{2}} "
                    "\\int_{-\\sqrt{4 - 4z^{2} - y}}^{\\sqrt{4 - 4z^{2} - y}} f(x, y, z)\\, dx"
                    "\\, dy\\, dz.$$"
                ),
                "result": (
                    "The sixth form. Its value for $f = 1$ is $4\\pi$, the same as the fifth "
                    "form."
                ),
                "verify": (
                    "`code/part5_verify.py` compares this form with the exact values $4\\pi$ and "
                    "$2\\pi/3$, and compares its limits with the defining inequality in both "
                    "directions."
                ),
            },
        ),
    },
    {
        "number": 6,
        "title": "The six forms in one table",
        "goal": (
            "Collect the six forms, then check that all six agree for five test functions with "
            "an exact value."
        ),
        "verify_script": "code/part6_verify.py",
        "figures": (
            ("part6_figure1.png",
             "Figure 6. The nesting of the six orders. Every limit string comes from the "
             "docstring of the function that evaluates that order."),
        ),
        "steps": (
            {
                "number": "6.1",
                "title": "The table of the six forms",
                "reason": (
                    "A table lets the reader compare the six orders. The innermost integral "
                    "always reads the chain; the outer two integrals read the projection or the "
                    "height range."
                ),
                "computation": (
                    "The six forms, with the innermost integral first in each label:\n\n"
                    "$$\\begin{aligned}"
                    "dy\\,dz\\,dx &: \\int_{-2}^{2} \\int_{-\\frac{1}{2}\\sqrt{4 - x^{2}}}^{"
                    "\\frac{1}{2}\\sqrt{4 - x^{2}}} \\int_{0}^{4 - x^{2} - 4z^{2}} f\\, dy\\, dz"
                    "\\, dx,\\\\"
                    "dy\\,dx\\,dz &: \\int_{-1}^{1} \\int_{-2\\sqrt{1 - z^{2}}}^{2\\sqrt{1 - "
                    "z^{2}}} \\int_{0}^{4 - x^{2} - 4z^{2}} f\\, dy\\, dx\\, dz,\\\\"
                    "dz\\,dy\\,dx &: \\int_{-2}^{2} \\int_{0}^{4 - x^{2}} \\int_{-\\frac{1}{2}"
                    "\\sqrt{4 - x^{2} - y}}^{\\frac{1}{2}\\sqrt{4 - x^{2} - y}} f\\, dz\\, dy"
                    "\\, dx,\\\\"
                    "dz\\,dx\\,dy &: \\int_{0}^{4} \\int_{-\\sqrt{4 - y}}^{\\sqrt{4 - y}} "
                    "\\int_{-\\frac{1}{2}\\sqrt{4 - y - x^{2}}}^{\\frac{1}{2}\\sqrt{4 - y - "
                    "x^{2}}} f\\, dz\\, dx\\, dy,\\\\"
                    "dx\\,dz\\,dy &: \\int_{0}^{4} \\int_{-\\frac{1}{2}\\sqrt{4 - y}}^{"
                    "\\frac{1}{2}\\sqrt{4 - y}} \\int_{-\\sqrt{4 - y - 4z^{2}}}^{\\sqrt{4 - y - "
                    "4z^{2}}} f\\, dx\\, dz\\, dy,\\\\"
                    "dx\\,dy\\,dz &: \\int_{-1}^{1} \\int_{0}^{4 - 4z^{2}} \\int_{-\\sqrt{4 - "
                    "4z^{2} - y}}^{\\sqrt{4 - 4z^{2} - y}} f\\, dx\\, dy\\, dz."
                    "\\end{aligned}$$"
                ),
                "result": (
                    "Six forms, one for each order of the three differentials. No form uses a "
                    "split, because every outer region is one piece."
                ),
                "verify": (
                    "`code/part6_verify.py` evaluates all six forms for five test functions. "
                    "`code/figures/part6_figure1.png` prints the same six limit sets as a "
                    "picture, and every string of that picture is copied from the docstring of "
                    "the matching function."
                ),
            },
            {
                "number": "6.2",
                "title": "The check that the six forms agree",
                "reason": (
                    "A single order with a wrong limit can still look right. Six orders that "
                    "disagree would show the fault at once, so the six values of one test "
                    "function must agree with each other and with the exact value."
                ),
                "computation": (
                    "The exact value of the integral of $x^{a} y^{b} z^{c}$ over $E$ follows by "
                    "the substitution $x = 2u$, $z = w$, $y = 4s$, which maps $E$ onto the unit "
                    "disk times the unit interval and multiplies the volume element by $8$. The "
                    "result is a rational multiple of $\\pi$.\n\n"
                    "The five test functions give: $f = 1$ gives $4\\pi = 12.566370614$; $f = y$ "
                    "gives $16\\pi/3 = 16.755160819$; $f = z$ gives $0$; $f = x^{2}$ gives "
                    "$8\\pi/3 = 8.377580410$; $f = z^{2}$ gives $2\\pi/3 = 2.094395102$."
                ),
                "result": (
                    "Every order gives the exact value of every test function. The largest "
                    "difference over the 30 pairs is below $7 \\times 10^{-13}$, and the largest "
                    "spread over the six orders of one function is below $8 \\times 10^{-14}$. "
                    "The six forms are equal."
                ),
                "verify": (
                    "`code/part6_verify.py` compares each of the 30 values with the exact "
                    "rational multiple of $\\pi$ from `code/exact_integrals.py`, and compares "
                    "the six values of each function with each other."
                ),
            },
        ),
    },
)

# The final answer of the whole problem, one line for each part.
FINAL_ANSWERS = (
    ("Part 1", "The solid is $E = \\{(x, y, z) : 0 \\leq y \\leq 4 - x^{2} - 4z^{2}\\}$, with "
               "base area $2\\pi$ and largest height $4$."),
    ("Part 2", "The projection on the plane $y = 0$ is $x^{2} + 4z^{2} \\leq 4$. The section "
               "at a height $y$ is a filled ellipse of area $\\pi(4 - y)/2$, and it is a "
               "single point at $y = 4$."),
    ("Part 3", "The two orders with the inner integral in $y$ are $dy\\,dz\\,dx$ and "
               "$dy\\,dx\\,dz$."),
    ("Part 4", "The two orders with the inner integral in $z$ are $dz\\,dy\\,dx$ and "
               "$dz\\,dx\\,dy$. Neither needs a split."),
    ("Part 5", "The two orders with the inner integral in $x$ are $dx\\,dz\\,dy$ and "
               "$dx\\,dy\\,dz$. Neither needs a split."),
    ("Part 6", "The six forms are equal for every integrand $f$ that is continuous on $E$."),
)
