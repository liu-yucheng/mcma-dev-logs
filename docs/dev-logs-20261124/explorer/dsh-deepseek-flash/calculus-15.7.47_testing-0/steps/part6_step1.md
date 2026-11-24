# Part 6. The check layer and the answer

## Step 6.1. Read the check tables

### Reason
Each part has one verification script, and each script prints one line for each comparison with the computed value, the expected value, and the tolerance. A page that publishes a value must also publish the check that supports the value.

### Computation
Every script compares a value that one method computes with a value that a different method computes. The pairs are two integration orders, two quadratures over the same region, a quadrature against an exact fraction, or a quadrature against a Monte Carlo mean within three standard errors.

### Result
The tables below give the count of checks of each part and the reason of each comparison.
