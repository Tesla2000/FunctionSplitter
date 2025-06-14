from __future__ import annotations

from typing import Final

EXAMPLE: Final[str] = (
    "\nEXAMPLE:"
    + """\n\nBefore:
async def _execute(self, state: "State") -> "State":
    from utils.model_manager import ModelManager

    model_manager = ModelManager()
    if not state.context.financial_survey.is_finished():
        state.context.navigation.push("retirement_accounts")
        messages = (
            [
                mark_action_plan_message(
                    AIMessage(FINANCIAL_SURVEY_REDIRECTION_MESSAGE),
                    "employer_401k_match",
                )
            ]
            if state.context.financial_survey.first_question_asked
            else []
        )
        return state.updated_state(
            messages=messages,
            phase="financial_survey",
        )
    response = await self.generate_retirement_response(
        state, model_manager
    )
    if not isinstance(response, AIMessage):
        return response
    phase = "retirement_accounts"
    if self.walkthrough_completion == 1:
        phase = state.context.navigation.pop()
    return state.updated_state(
        **{
            "messages": [response],
            "phase": phase,
        }
    )
"""
    + """\n\nAfter:
class ExecuteTemplateMethod:
    _retirement_accounts: "RetirementAccounts"
    _state: "State"
    _model_manager: ModelManager

    def __init__(
        self, retirement_accounts: "RetirementAccounts", state: "State"
    ):
        self.retirement_accounts: "RetirementAccounts" = retirement_accounts
        self.state: "State" = state

    async def execute(self) -> "State":
        self._initialize_model_manager()
        self._retirement_accounts = self.retirement_accounts
        self._state = self.state

        if not self._check_financial_survey_completion():
            return self._handle_incomplete_survey()

        response = await self._generate_retirement_response()
        if not isinstance(response, AIMessage):
            return response

        phase = self._determine_phase()
        return self._create_updated_state(response, phase)

    def _initialize_model_manager(self) -> None:
        from utils.model_manager import ModelManager

        self._model_manager = ModelManager()

    def _check_financial_survey_completion(self) -> bool:
        return self._state.context.financial_survey.is_finished()

    def _handle_incomplete_survey(self) -> "State":
        self._state.context.navigation.push("retirement_accounts")
        messages = (
            [
                mark_action_plan_message(
                    AIMessage(FINANCIAL_SURVEY_REDIRECTION_MESSAGE),
                    "employer_401k_match",
                )
            ]
            if self._state.context.financial_survey.first_question_asked
            else []
        )
        return self._state.updated_state(
            messages=messages,
            phase="financial_survey",
        )

    async def _generate_retirement_response(self) -> "AIMessage | State":
        return await self._retirement_accounts.generate_retirement_response(
            self._state, self._model_manager
        )

    def _determine_phase(self) -> str:
        phase = "retirement_accounts"
        if self._retirement_accounts.walkthrough_completion == 1:
            phase = self._state.context.navigation.pop()
        return phase

    def _create_updated_state(
        self, response: "AIMessage", phase: str
    ) -> "State":
        return self._state.updated_state(messages=[response], phase=phase)"""
)
