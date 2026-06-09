# persona/router.py
"""
MVQueen Persona Router — Enterprise Edition
-------------------------------------------

Routes detection outputs to the correct persona profile.

Inputs:
- vibe
- trend
- silhouette
- material
- season
- product type

Outputs:
- persona key (string)
"""

from typing import Dict
from .persona_rules import apply_persona_rules
from .profiles import PERSONA_PROFILES


# ------------------------------------------------------------
# MAIN ROUTER — Determines persona key
# ------------------------------------------------------------
def route_persona(product_profile: Dict) -> Dict:
    """
    Routes a product detection profile to the correct persona profile.
    """

    # Step 1: Determine persona key using rule engine
    persona_key = apply_persona_rules(product_profile)

    # Ensure persona_key is always a string
    if isinstance(persona_key, dict): persona_key = persona_key.get("key", "editorial")

    return PERSONA_PROFILES.get(persona_key,PERSONA_PROFILES["editorial"])


__all__ = ["route_persona"]