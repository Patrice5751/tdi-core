from tdi.graphical.alert_deduplication_result import (
    AlertDeduplicationResult,
)
from tdi.graphical.alert_state import AlertState
from tdi.graphical.transition_alert import TransitionAlert


class AlertDeduplicationEngine:
    def analyze(
        self,
        current_alert: TransitionAlert,
        previous_alert: AlertState | None,
    ) -> AlertDeduplicationResult:
        if not current_alert.active:
            return AlertDeduplicationResult(
                alert=current_alert,
                is_new=False,
                reason=(
                    "Aucune alerte active à signaler."
                ),
            )

        if previous_alert is None:
            return AlertDeduplicationResult(
                alert=current_alert,
                is_new=True,
                reason=(
                    "Nouvelle alerte : aucune alerte "
                    "précédente enregistrée."
                ),
            )

        same_level = (
            previous_alert.level
            == current_alert.level.value
        )

        same_message = (
            previous_alert.message
            == current_alert.message
        )

        if same_level and same_message:
            return AlertDeduplicationResult(
                alert=current_alert,
                is_new=False,
                reason=(
                    "Cette alerte a déjà été signalée."
                ),
            )

        return AlertDeduplicationResult(
            alert=current_alert,
            is_new=True,
            reason=(
                "Nouvelle alerte ou modification "
                "significative de l'alerte précédente."
            ),
        )
    