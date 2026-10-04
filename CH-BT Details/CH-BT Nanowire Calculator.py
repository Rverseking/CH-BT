import math

# This Calculator Program was used to Calculate the Ballisticity of the Target Node, it does Not Gurantee it will work as Intended. It should be Properly Verified via printing or Supercomputers
# Note : [!] For Proper Safety Evaluation, Please use Professional Testing before Commercial Usage of Calculated Hardware.


# ============================================================
# MWCNT + h-BN Coaxial Node Calculator
#
# This is a theoretical screening model.
#
# The carbon core is treated as a multi-walled carbon nanotube
# (MWCNT)
#
# Important:
#   - MWCNT electrical properties depend on chirality.
#   - Different walls can be metallic or semiconducting.
#   - Real contacts, defects and fabrication can dominate
#     resistance.
#   - h-BN breakdown strength also depends on thickness,
#     defects and fabrication.
#
# This program is NOT a proper safety certification of Hardware Nodes in Consumer Devices.
# ============================================================


# ------------------------------------------------------------
# Fundamental constants
# ------------------------------------------------------------

h = 6.62607015e-34          # Planck constant, J*s
hbar = h / (2 * math.pi)

e = 1.602176634e-19         # Elementary charge, C
k_B = 1.380649e-23          # Boltzmann constant, J/K
eps_0 = 8.8541878128e-12    # Vacuum permittivity, F/m
m_0 = 9.1093837139e-31      # Electron rest mass, kg


# ------------------------------------------------------------
# MWCNT material parameters
# ------------------------------------------------------------

# Typical spacing between graphitic walls in a CNT.
wall_spacing_nm = 0.34

# Approximate graphene/CNT Fermi velocity.
# This is useful for a simple Dirac approximation.
v_f = 1.0e6                 # m/s

# Conservative mobility assumption.
# Actual CNT transport can differ greatly depending on
# tube quality, contacts, substrate and defects.
mobility_cm2_vs = 5000.0

# Each ideal metallic CNT has two conducting channels
# when spin degeneracy is included:
#
#     G0 = 4e^2/h
#
# This is the ideal ballistic limit.
channels_per_metallic_wall = 2


# ------------------------------------------------------------
# h-BN parameters
# ------------------------------------------------------------

epsilon_hbn = 3.76

# Approximate h-BN band gap.
#
# IMPORTANT:
# This is NOT automatically the graphene/CNT-hBN tunnel barrier.
hbn_bandgap_ev = 6.0

# Approximate electron effective mass used only for the
# simple WKB estimate.
hbn_effective_mass = 0.26


# ------------------------------------------------------------
# Conservative dielectric screening
# ------------------------------------------------------------

# Rough screening value rather than claiming a universal
# breakdown field.
hbn_screening_limit_mv_cm = 2.0

# Only use 50% of the screening value.
safety_margin = 0.50


# ============================================================
# USER PARAMETERS
# ============================================================

fermi_energy_ev = 1.3

# Diameter of the entire MWCNT carbon core.
mwcnt_diameter_nm = 8.4

# h-BN shell thickness.
hbn_thickness_nm = 4.8

# Active electrical length.
line_length_nm = 25.0

# Applied voltage.
bias_v = 0.8

temperature_k = 300.0


# ------------------------------------------------------------
# MWCNT wall assumptions
# ------------------------------------------------------------

# Approximate number of graphitic walls.
#
# For a real device, measure the wall count instead.
wall_count = max(
    1,
    round(
        mwcnt_diameter_nm
        / (2 * wall_spacing_nm)
    )
)

# We do NOT assume every wall is metallic.
#
# Instead, the user can provide the fraction of walls that
# are expected to contribute to conduction.
#
# 0.25 means roughly 25% of walls are treated as conducting.
#
# This is intentionally conservative because CNT chirality
# determines whether a particular wall is metallic.
metallic_wall_fraction = 0.25


# ------------------------------------------------------------
# Interface barrier
# ------------------------------------------------------------

# Leave False unless an experimentally appropriate
# CNT/h-BN interface barrier is known.
interface_barrier_known = False

interface_barrier_ev = None


# ============================================================
# Basic checks
# ============================================================

def validate_inputs():

    if fermi_energy_ev <= 0:
        raise ValueError(
            "Fermi energy must be greater than 0 eV."
        )

    if mwcnt_diameter_nm <= 0:
        raise ValueError(
            "MWCNT diameter must be greater than 0 nm."
        )

    if hbn_thickness_nm <= 0:
        raise ValueError(
            "h-BN thickness must be greater than 0 nm."
        )

    if line_length_nm <= 0:
        raise ValueError(
            "Line length must be greater than 0 nm."
        )

    if bias_v < 0:
        raise ValueError(
            "Bias voltage cannot be negative."
        )

    if temperature_k <= 0:
        raise ValueError(
            "Temperature must be greater than 0 K."
        )

    if not 0 <= metallic_wall_fraction <= 1:
        raise ValueError(
            "Metallic wall fraction must be between 0 and 1."
        )


# ============================================================
# CNT wall calculations
# ============================================================

def estimate_wall_count(diameter_nm):
    """
    Roughly estimate the number of graphitic walls.

    CNT wall spacing is approximately 0.34 nm.

    This is only a geometric estimate because real MWCNTs
    do not necessarily have perfectly uniform wall spacing.
    """

    return max(
        1,
        round(diameter_nm / (2 * wall_spacing_nm))
    )


def estimate_metallic_walls(total_walls):
    """
    Not every CNT wall is metallic.

    Metallic vs semiconducting behavior depends on chirality.

    Since chirality is not supplied, use a conservative
    user-defined fraction instead of pretending every wall
    conducts.
    """

    return max(
        0,
        round(
            total_walls
            * metallic_wall_fraction
        )
    )


# ============================================================
# CNT electronic structure
# ============================================================

def fermi_wavevector(energy_ev):

    energy_j = energy_ev * e

    return energy_j / (
        hbar * v_f
    )


# ============================================================
# CNT channels
# ============================================================

def calculate_channels(metallic_walls):
    """
    Ideal metallic CNT:

        G = 4e^2/h

    The factor 4 comes from spin + valley degeneracy.

    Here we calculate the ideal channel count from the number
    of assumed metallic walls.

    This is NOT the same as saying every wall will actually
    transmit perfectly.
    """

    return (
        metallic_walls
        * channels_per_metallic_wall
    )


# ============================================================
# Landauer transport
# ============================================================

def landauer_conductance(channels, transmission=1.0):

    quantum_conductance = (
        e ** 2 / h
    )

    return (
        quantum_conductance
        * channels
        * transmission
    )


# ============================================================
# Mean free path
# ============================================================

def estimate_mfp(energy_ev):

    """
    Simple mobility-based estimate.

    This is only an order-of-magnitude transport estimate.

    Real MWCNT mean free path can be strongly affected by:

        - defects
        - wall-to-wall scattering
        - contacts
        - phonons
        - impurities
        - substrate
        - tube quality
    """

    energy_j = energy_ev * e

    mobility_m2_vs = (
        mobility_cm2_vs
        * 1e-4
    )

    return (
        mobility_m2_vs
        * energy_j
        / (e * v_f)
    )


# ============================================================
# Coaxial electric field
# ============================================================

def coaxial_field(
    inner_radius_m,
    outer_radius_m,
    voltage
):

    return voltage / (
        inner_radius_m
        * math.log(
            outer_radius_m
            / inner_radius_m
        )
    )


# ============================================================
# Coaxial capacitance
# ============================================================

def coaxial_capacitance(
    inner_radius_m,
    outer_radius_m
):

    return (
        2
        * math.pi
        * eps_0
        * epsilon_hbn
        / math.log(
            outer_radius_m
            / inner_radius_m
        )
    )


# ============================================================
# WKB tunneling estimate
# ============================================================

def wkb_tunneling(
    barrier_ev,
    thickness_m
):

    if barrier_ev <= 0:
        return 1.0

    effective_mass = (
        hbn_effective_mass
        * m_0
    )

    exponent = (
        2
        * thickness_m
        * math.sqrt(
            2
            * effective_mass
            * barrier_ev
            * e
        )
        / hbar
    )

    if exponent > 745:
        return 0.0

    return math.exp(-exponent)


# ============================================================
# Main calculation
# ============================================================

def run_calc():

    validate_inputs()


    # --------------------------------------------------------
    # Geometry
    # --------------------------------------------------------

    mwcnt_radius_m = (
        mwcnt_diameter_nm / 2
    ) * 1e-9

    outer_radius_m = (
        mwcnt_radius_m
        + hbn_thickness_nm * 1e-9
    )

    total_diameter_nm = (
        2
        * outer_radius_m
        * 1e9
    )


    # --------------------------------------------------------
    # MWCNT walls
    # --------------------------------------------------------

    actual_wall_count = estimate_wall_count(
        mwcnt_diameter_nm
    )

    metallic_walls = estimate_metallic_walls(
        actual_wall_count
    )


    # --------------------------------------------------------
    # Electronic structure
    # --------------------------------------------------------

    k_f = fermi_wavevector(
        fermi_energy_ev
    )


    # --------------------------------------------------------
    # Conducting channels
    # --------------------------------------------------------

    channels = calculate_channels(
        metallic_walls
    )


    # --------------------------------------------------------
    # Ideal Landauer resistance
    # --------------------------------------------------------

    if channels > 0:

        conductance = landauer_conductance(
            channels,
            transmission=1.0
        )

        resistance = 1 / conductance

    else:

        conductance = 0.0
        resistance = math.inf


    # --------------------------------------------------------
    # Mean free path
    # --------------------------------------------------------

    mfp_m = estimate_mfp(
        fermi_energy_ev
    )

    device_length_m = (
        line_length_nm * 1e-9
    )

    length_to_mfp = (
        device_length_m / mfp_m
    )

    likely_ballistic = (
        length_to_mfp < 0.1
    )


    # --------------------------------------------------------
    # Electric field
    # --------------------------------------------------------

    max_field = coaxial_field(
        mwcnt_radius_m,
        outer_radius_m,
        bias_v
    )

    max_field_v_nm = (
        max_field * 1e-9
    )

    max_field_mv_cm = (
        max_field / 1e8
    )


    # --------------------------------------------------------
    # Conservative dielectric check
    # --------------------------------------------------------

    conservative_limit = (
        hbn_screening_limit_mv_cm
        * safety_margin
    )

    field_ok = (
        max_field_mv_cm
        < conservative_limit
    )


    # --------------------------------------------------------
    # Capacitance
    # --------------------------------------------------------

    capacitance_per_meter = (
        coaxial_capacitance(
            mwcnt_radius_m,
            outer_radius_m
        )
    )

    total_capacitance = (
        capacitance_per_meter
        * device_length_m
    )


    # --------------------------------------------------------
    # Tunneling
    # --------------------------------------------------------

    if interface_barrier_known:

        tunneling_probability = (
            wkb_tunneling(
                interface_barrier_ev,
                hbn_thickness_nm * 1e-9
            )
        )

    else:

        tunneling_probability = None


    # ========================================================
    # OUTPUT
    # ========================================================

    print()
    print("=" * 62)
    print("        MWCNT / h-BN COAXIAL NODE CALCULATOR")
    print("=" * 62)


    print()
    print("---------------- Geometry ----------------")

    print(
        f"MWCNT diameter       : "
        f"{mwcnt_diameter_nm:.2f} nm"
    )

    print(
        f"h-BN thickness       : "
        f"{hbn_thickness_nm:.2f} nm"
    )

    print(
        f"Total diameter       : "
        f"{total_diameter_nm:.2f} nm"
    )

    print(
        f"Device length        : "
        f"{line_length_nm:.2f} nm"
    )


    print()
    print("---------------- MWCNT ----------------")

    print(
        f"Estimated walls      : "
        f"{actual_wall_count}"
    )

    print(
        f"Assumed metallic     : "
        f"{metallic_walls}"
    )

    print(
        f"Metallic fraction    : "
        f"{metallic_wall_fraction * 100:.1f}%"
    )

    print(
        f"Fermi energy         : "
        f"{fermi_energy_ev:.3f} eV"
    )

    print(
        f"Fermi wavevector     : "
        f"{k_f:.3e} 1/m"
    )


    print()
    print("---------------- Transport ----------------")

    print(
        f"Ideal channels       : "
        f"{channels}"
    )

    if channels > 0:

        print(
            f"Ideal conductance    : "
            f"{conductance:.4e} S"
        )

        print(
            f"Ideal resistance     : "
            f"{resistance:.2f} Ohm"
        )

    else:

        print(
            "Ideal conductance    : "
            "0 S (no metallic walls assumed)"
        )

        print(
            "Ideal resistance     : "
            "Infinite in this simple model"
        )


    print(
        f"Assumed mobility     : "
        f"{mobility_cm2_vs:.0f} cm^2/Vs"
    )

    print(
        f"Estimated MFP        : "
        f"{mfp_m * 1e9:.1f} nm"
    )

    print(
        f"Length / MFP         : "
        f"{length_to_mfp:.3e}"
    )

    print(
        f"Ballistic assumption : "
        f"{'PLAUSIBLE' if likely_ballistic else 'QUESTIONABLE'}"
    )


    print()
    print("---------------- Electric Field ----------------")

    print(
        f"Bias                 : "
        f"{bias_v:.3f} V"
    )

    print(
        f"Maximum field        : "
        f"{max_field_v_nm:.4f} V/nm"
    )

    print(
        f"Maximum field        : "
        f"{max_field_mv_cm:.2f} MV/cm"
    )

    print(
        f"Conservative limit   : "
        f"{conservative_limit:.2f} MV/cm"
    )

    print(
        f"Field check          : "
        f"{'PASS' if field_ok else 'FAIL'}"
    )


    print()
    print("---------------- Capacitance ----------------")

    print(
        f"Capacitance / metre  : "
        f"{capacitance_per_meter * 1e12:.3f} pF/m"
    )

    print(
        f"Device capacitance   : "
        f"{total_capacitance * 1e15:.3f} fF"
    )


    print()
    print("---------------- Tunneling ----------------")

    print(
        f"h-BN band gap        : "
        f"~{hbn_bandgap_ev:.1f} eV"
    )

    if interface_barrier_known:

        print(
            f"Interface barrier    : "
            f"{interface_barrier_ev:.2f} eV"
        )

        print(
            f"WKB probability      : "
            f"{tunneling_probability:.3e}"
        )

    else:

        print(
            "Interface barrier    : UNKNOWN"
        )

        print(
            "WKB probability      : NOT CALCULATED"
        )

        print(
            "Reason               : "
            "h-BN band gap is not automatically "
            "the CNT/h-BN barrier."
        )


    # ========================================================
    # Final result
    # ========================================================

    print()
    print("---------------- Result ----------------")

    if field_ok and likely_ballistic:

        print(
            "Model result: Looks reasonable "
            "under the assumptions."
        )

    else:

        print(
            "Model result: Needs more engineering work."
        )


    print()
    print("---------------- Warnings ----------------")

    if not field_ok:

        print(
            "[!] Electric field is above the "
            "conservative screening limit."
        )

    if not likely_ballistic:

        print(
            "[!] Transport is not clearly ballistic "
            "under the assumed mobility."
        )

    print(
        "[!] CNT chirality was not specified, so the "
        "metallic-wall count is only an estimate."
    )

    print(
        "[!] Real MWCNT contacts can add substantial "
        "resistance."
    )

    print(
        "[!] The CNT/h-BN interface barrier is unknown."
    )

    print(
        "[!] Breakdown depends on defects, thickness "
        "and fabrication."
    )

    print(
        "[!] This program does not certify properly verified real hardware this is purley an Estimate."
    )

    print("=" * 62)


if __name__ == "__main__":
    run_calc()
