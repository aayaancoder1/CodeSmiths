from enum import Enum

from .confirmation_errors import InvalidConfirmationStateError
from .confirmation_models import ConfirmationState


def validate_confirmation_state(state: str) -> ConfirmationState:
    """Validate that *state* is a member of :class:`ConfirmationState`.

    Raises:
        InvalidConfirmationStateError: If *state* is not a valid confirmation state.
    """
    try:
        return ConfirmationState(state)
    except ValueError as exc:
        raise InvalidConfirmationStateError(f"Invalid confirmation state: {state}") from exc
