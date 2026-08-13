from tdi.graphical.scenario_transition import (
    ScenarioTransition,
    ScenarioTransitionAnalysis,
)
from tdi.graphical.transition_alert import (
    AlertLevel,
    TransitionAlert,
)


class TransitionAlertEngine:
    def analyze(
        self,
        transition: ScenarioTransitionAnalysis,
        target_side: str | None,
    ) -> TransitionAlert:

        if transition.transition == ScenarioTransition.UNCHANGED:
            return TransitionAlert(
                level=AlertLevel.NONE,
                active=False,
                message="Aucun changement significatif du scénario.",
                action="Continuer la surveillance normale.",
            )

        if transition.transition == ScenarioTransition.IMPROVING:
            side = target_side or "directionnel"

            return TransitionAlert(
                level=AlertLevel.INFO,
                active=True,
                message=(
                    f"Le scénario {side} s'améliore."
                ),
                action=(
                    "Surveiller les prochaines confirmations "
                    "sans anticiper l'entrée."
                ),
            )

        if transition.transition == ScenarioTransition.DETERIORATING:
            side = target_side or "directionnel"

            return TransitionAlert(
                level=AlertLevel.WARNING,
                active=True,
                message=(
                    f"Le scénario {side} se détériore."
                ),
                action=(
                    "Ne pas renforcer le scénario. "
                    "Attendre une nouvelle amélioration."
                ),
            )

        if transition.transition == ScenarioTransition.INVALIDATED:
            return TransitionAlert(
                level=AlertLevel.WARNING,
                active=True,
                message=(
                    "Le scénario directionnel précédent "
                    "est invalidé."
                ),
                action=(
                    "Abandonner le scénario précédent et "
                    "attendre une nouvelle configuration."
                ),
            )

        if transition.transition == ScenarioTransition.TRIGGERED:
            side = target_side or "directionnel"

            return TransitionAlert(
                level=AlertLevel.HIGH,
                active=True,
                message=(
                    f"Le scénario {side} atteint l'état Ready."
                ),
                action=(
                    "Vérifier le setup complet et la gestion "
                    "du risque avant toute entrée."
                ),
            )

        return TransitionAlert(
            level=AlertLevel.NONE,
            active=False,
            message="Aucune alerte.",
            action="Continuer la surveillance.",
        )
    