from dataclasses import dataclass
from enum import Enum

from ..models import LeadState


@dataclass(frozen=True)
class Transition:
    from_state: LeadState.States
    to_state: LeadState.States


class Transitions(Enum):
    NEW_TO_IN_PROGRESS = Transition(LeadState.States.STATE_NEW.value,
                                    LeadState.States.STATE_IN_PROGRESS.value)
    IN_PROGRESS_TO_POSTPONED = Transition(LeadState.States.STATE_IN_PROGRESS.value,
                                          LeadState.States.STATE_POSTPONED.value)
    IN_PROGRESS_TO_DONE = Transition(LeadState.States.STATE_IN_PROGRESS.value,
                                     LeadState.States.STATE_DONE.value)
    POSTPONED_TO_IN_PROGRESS = Transition(LeadState.States.STATE_POSTPONED.value,
                                          LeadState.States.STATE_IN_PROGRESS.value)
    POSTPONED_TO_DONE = Transition(LeadState.States.STATE_POSTPONED.value,
                                   LeadState.States.STATE_DONE.value)
