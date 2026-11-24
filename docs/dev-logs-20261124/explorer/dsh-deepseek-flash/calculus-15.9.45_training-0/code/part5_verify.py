"""Check Part 5: the position of the bumps, the extreme radii, and the numbers of Figure 1.

The check reads the marked directions from :mod:`bumpy_sphere`, which the figure also reads, so
the coordinates that a step quotes and the coordinates that the figure draws come from one place.
Every count is compared with a count that a scan of the surface produces, and every extreme radius
is compared with the exact rational value of the surface.
"""

import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import bumpy_sphere
from verification_report import CheckLog

SCAN_SAMPLE_COUNT = 40001
"""Number of sample points along one angle for the counting scans."""

BAND_TOLERANCE = 1.0e-9
"""Distance from an exact extreme of a sine that still counts as that extreme."""

GRID_RESOLUTION_TOLERANCE = 1.0e-3
"""Largest accepted gap between a grid extreme and the exact extreme of the surface."""

CONTOUR_LEVEL_COUNT = 13
"""Number of filled contour levels of the radius map of Figure 1."""

DRAWN_GRID_COUNT = 541
"""Number of sample lines that the figure uses along each angle."""


def peak_radii() -> list[float]:
    """Return the radius of the surface at every direction of a bump peak.

    Returns:
        One radius for each direction of :func:`bumpy_sphere.peak_directions`.
    """
    return [bumpy_sphere.radius(theta, phi)
            for theta, phi in bumpy_sphere.peak_directions()]


def polar_bands(sign: float) -> list[float]:
    """Return the polar angles of a scan where ``sin(5 varphi)`` equals one sign.

    Args:
        sign: Either ``1.0`` or ``-1.0``.

    Returns:
        The polar angles of the bands, grouped so that one band appears once.
    """
    phi = np.linspace(0.0, math.pi, SCAN_SAMPLE_COUNT)
    values = np.sin(bumpy_sphere.PHI_WAVE * phi)
    selected = phi[np.abs(values - sign) < BAND_TOLERANCE]
    if selected.size == 0:
        return []
    groups = [float(selected[0])]
    for angle in selected[1:]:
        if abs(float(angle) - groups[-1]) > 1.0e-3:
            groups.append(float(angle))
    return groups


def equator_maximum_count() -> int:
    """Return the number of bump maxima along the equator ``varphi = pi / 2``.

    Returns:
        The number of local maxima of the radius along one full turn of the azimuthal angle.
    """
    theta = np.linspace(0.0, 2.0 * math.pi, SCAN_SAMPLE_COUNT, endpoint=False)
    values = bumpy_sphere.radius_array(theta, np.full_like(theta, math.pi / 2.0))
    left = np.roll(values, 1)
    right = np.roll(values, -1)
    peaks = (values > left) & (values > right)
    return int(np.count_nonzero(peaks))


def drawn_map_numbers() -> dict[str, float]:
    """Return the numbers that the radius map of Figure 1 shows.

    Returns:
        The smallest radius, the largest radius, and the radius at the four corners of the drawn
        parameter window.
    """
    theta = np.linspace(0.0, 2.0 * math.pi, DRAWN_GRID_COUNT)
    phi = np.linspace(0.0, math.pi, DRAWN_GRID_COUNT)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    values = bumpy_sphere.radius_array(theta_grid, phi_grid)
    corners = {
        "corner_theta_0_phi_0": float(bumpy_sphere.radius(0.0, 0.0)),
        "corner_theta_0_phi_pi": float(bumpy_sphere.radius(0.0, math.pi)),
        "corner_theta_2pi_phi_0": float(bumpy_sphere.radius(2.0 * math.pi, 0.0)),
        "corner_theta_2pi_phi_pi": float(bumpy_sphere.radius(2.0 * math.pi, math.pi)),
    }
    numbers = {
        "minimum": float(values.min()),
        "maximum": float(values.max()),
        "theta_step": float(theta[1] - theta[0]),
        "phi_step": float(phi[1] - phi[0]),
    }
    numbers.update(corners)
    return numbers


def main() -> None:
    """Run the checks of Part 5 and write the summary of the part."""
    log = CheckLog("part5")

    radii = peak_radii()
    deviation = max(abs(value - float(bumpy_sphere.RADIUS_MAXIMUM)) for value in radii)
    log.record("radius at every bump peak against 6/5", deviation, 0.0, deviation,
               deviation < 1.0e-12)

    peak_bands = polar_bands(1.0)
    valley_bands = polar_bands(-1.0)
    distinct_peak_polar = len({round(phi, 9) for _theta, phi in bumpy_sphere.peak_directions()})
    log.record("polar bands of a bump peak: scan against the list of peak directions",
               float(len(peak_bands)), float(distinct_peak_polar),
               float(abs(len(peak_bands) - distinct_peak_polar)),
               len(peak_bands) == distinct_peak_polar)
    expected_valley_bands = bumpy_sphere.PHI_WAVE - len(peak_bands)
    log.record("polar bands of a valley: scan against the remaining bands",
               float(len(valley_bands)), float(expected_valley_bands),
               float(abs(len(valley_bands) - expected_valley_bands)),
               len(valley_bands) == expected_valley_bands)

    marked = bumpy_sphere.marked_points()
    peak_norm = math.dist(marked["peak"], (0.0, 0.0, 0.0))
    valley_norm = math.dist(marked["valley"], (0.0, 0.0, 0.0))
    log.record("length of the marked peak point against 6/5", peak_norm,
               float(bumpy_sphere.RADIUS_MAXIMUM), abs(peak_norm - float(
                   bumpy_sphere.RADIUS_MAXIMUM)),
               abs(peak_norm - float(bumpy_sphere.RADIUS_MAXIMUM)) < 1.0e-15)
    log.record("length of the marked valley point against 4/5", valley_norm,
               float(bumpy_sphere.RADIUS_MINIMUM), abs(valley_norm - float(
                   bumpy_sphere.RADIUS_MINIMUM)),
               abs(valley_norm - float(bumpy_sphere.RADIUS_MINIMUM)) < 1.0e-15)

    peak_residual = abs(peak_norm - bumpy_sphere.radius(
        bumpy_sphere.LOBE_THETA, bumpy_sphere.LOBE_PHI))
    valley_residual = abs(valley_norm - bumpy_sphere.radius(
        bumpy_sphere.VALLEY_THETA, bumpy_sphere.VALLEY_PHI))
    log.record("marked peak point on the surface: length of the point against its radius",
               peak_residual, 0.0, peak_residual, peak_residual < 1.0e-15)
    log.record("marked valley point on the surface: length of the point against its radius",
               valley_residual, 0.0, valley_residual, valley_residual < 1.0e-15)

    maxima = equator_maximum_count()
    log.record("bump peaks along the equator against the statement parameter m",
               float(maxima), float(bumpy_sphere.THETA_WAVE),
               float(abs(maxima - bumpy_sphere.THETA_WAVE)),
               maxima == bumpy_sphere.THETA_WAVE)

    numbers = drawn_map_numbers()
    log.record("smallest radius on the drawn map grid against 4/5", numbers["minimum"],
               float(bumpy_sphere.RADIUS_MINIMUM),
               abs(numbers["minimum"] - float(bumpy_sphere.RADIUS_MINIMUM)),
               abs(numbers["minimum"] - float(bumpy_sphere.RADIUS_MINIMUM))
               < GRID_RESOLUTION_TOLERANCE)
    log.record("largest radius on the drawn map grid against 6/5", numbers["maximum"],
               float(bumpy_sphere.RADIUS_MAXIMUM),
               abs(numbers["maximum"] - float(bumpy_sphere.RADIUS_MAXIMUM)),
               abs(numbers["maximum"] - float(bumpy_sphere.RADIUS_MAXIMUM))
               < GRID_RESOLUTION_TOLERANCE)

    log.require_all_passed()
    log.write()

    print(f"peak directions {len(bumpy_sphere.peak_directions())}, "
          f"peak polar bands {len(peak_bands)}, valley polar bands {len(valley_bands)}", flush=True)
    print("peak polar bands at " + ", ".join(f"{value:.6f}" for value in peak_bands), flush=True)
    print("valley polar bands at " + ", ".join(f"{value:.6f}" for value in valley_bands),
          flush=True)
    print(f"marked peak ({marked['peak'][0]:.6f}, {marked['peak'][1]:.6f}, "
          f"{marked['peak'][2]:.6f})", flush=True)
    print(f"marked valley ({marked['valley'][0]:.6f}, {marked['valley'][1]:.6f}, "
          f"{marked['valley'][2]:.6f})", flush=True)
    print(f"equator peaks {maxima}, contour levels {CONTOUR_LEVEL_COUNT}, "
          f"drawn grid {DRAWN_GRID_COUNT} lines per angle", flush=True)
    print("drawn map: minimum {minimum:.6f}, maximum {maximum:.6f}, "
          "corner radii {corner_theta_0_phi_0:.6f} at (0, 0), "
          "{corner_theta_0_phi_pi:.6f} at (0, pi), {corner_theta_2pi_phi_0:.6f} at (2 pi, 0), "
          "{corner_theta_2pi_phi_pi:.6f} at (2 pi, pi)".format(**numbers), flush=True)


if __name__ == "__main__":
    main()
