from enum import Enum


class RuleCategory(Enum):
    """Catégories de règles utilisées par TDI."""

    STRUCTURE = "Structure"
    RISK = "Risk"
    CONFLUENCE = "Confluence"