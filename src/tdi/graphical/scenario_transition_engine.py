from tdi.graphical.scenario_state import ScenarioState
from tdi.graphical.scenario_transition import (
    ScenarioTransition,
    ScenarioTransitionAnalysis,
)


class ScenarioTransitionEngine:
    def analyze(
        self,
        previous_state: ScenarioState,
        current_state: ScenarioState,
    ) -> ScenarioTransitionAnalysis:
        if previous_state == current_state:
            return ScenarioTransitionAnalysis(
                previous_state=previous_state,
                current_state=current_state,
                transition=ScenarioTransition.UNCHANGED,
                reason=(
                    f"Le scénario reste dans l'état "
                    f"{current_state.value}."
                ),
            )

        if current_state == ScenarioState.READY:
            return ScenarioTransitionAnalysis(
                previous_state=previous_state,
                current_state=current_state,
                transition=ScenarioTransition.TRIGGERED,
                reason=(
                    f"Le scénario passe de "
                    f"{previous_state.value} à Ready."
                ),
            )

        if current_state == ScenarioState.INVALID:
            return ScenarioTransitionAnalysis(
                previous_state=previous_state,
                current_state=current_state,
                transition=ScenarioTransition.INVALIDATED,
                reason=(
                    f"Le scénario passe de "
                    f"{previous_state.value} à Invalid."
                ),
            )

        if (
            previous_state == ScenarioState.DEGRADING
            and current_state == ScenarioState.BUILDING
        ):
            return ScenarioTransitionAnalysis(
                previous_state=previous_state,
                current_state=current_state,
                transition=ScenarioTransition.IMPROVING,
                reason=(
                    "Le scénario recommence à se construire."
                ),
            )

        if (
            previous_state == ScenarioState.INVALID
            and current_state == ScenarioState.BUILDING
        ):
            return ScenarioTransitionAnalysis(
                previous_state=previous_state,
                current_state=current_state,
                transition=ScenarioTransition.IMPROVING,
                reason=(
                    "Un scénario directionnel recommence "
                    "à émerger."
                ),
            )

        if (
            previous_state == ScenarioState.READY
            and current_state == ScenarioState.BUILDING
        ):
            return ScenarioTransitionAnalysis(
                previous_state=previous_state,
                current_state=current_state,
                transition=ScenarioTransition.DETERIORATING,
                reason=(
                    "Le scénario n'est plus immédiatement "
                    "prêt à être exécuté."
                ),
            )

        if current_state == ScenarioState.DEGRADING:
            return ScenarioTransitionAnalysis(
                previous_state=previous_state,
                current_state=current_state,
                transition=ScenarioTransition.DETERIORATING,
                reason=(
                    f"Le scénario passe de "
                    f"{previous_state.value} à Degrading."
                ),
            )

        return ScenarioTransitionAnalysis(
            previous_state=previous_state,
            current_state=current_state,
            transition=ScenarioTransition.UNCHANGED,
            reason=(
                "Le changement d'état ne modifie pas "
                "significativement la qualité du scénario."
            ),
        )
    