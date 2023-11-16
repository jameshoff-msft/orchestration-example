from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class Database:
    @sk_function(
        description="Retrieves a value from a database based on the domain and customer information.  Returns the value in the context 'value'",
        name="getValue",
    )
    @sk_function_context_parameter(
        name="CUSTOMER",
        description="The name of the customer.",
    )
    @sk_function_context_parameter(
        name="DOMAIN",
        description="The name of the data domain. Example Domains are : Dividend Income, Taxes Paid, Unrealized Gains.",
    )
    def getValue(self, context: SKContext) -> str:
        if context["DOMAIN"] != None:
            if context["DOMAIN"] == "Dividend Income":
                context["VALUE"] = str(100.00)
                return str(100.00)
            elif context["DOMAIN"] == "Unrealized Gains":
                context["VALUE"] = str(50.00)
                return str(50.00)
            elif context["DOMAIN"] == "Taxes Paid":
                context["VALUE"] = str("No Value")
                return str("No Value")
        else:
            context["VALUE"] = str("No Value")
            return str("No Value")
        

    @sk_function(
        description="Retrieves the 'Trial Balance' from a database based on the domain and customer information.  Returns the value in the context 'trialBalance'",
        name="getTrialBalance",
    )
    @sk_function_context_parameter(
        name="CUSTOMER",
        description="The name of the customer.",
    )
    @sk_function_context_parameter(
        name="DOMAIN",
        description="The name of the data domain. Example Domains are : Dividend Income, Taxes Paid, Unrealized Gains.",
    )
    def getTrialBalance(self, context: SKContext) -> str:
        if context["DOMAIN"] != None:
            if context["DOMAIN"] == "Dividend Income":
                context["TRIAL_BALANCE"] = str(100.00)
                return str(100.00)
            elif context["DOMAIN"] == "Unrealized Gains":
                context["TRIAL_BALANCE"] = str(49.00)
                return str(49.00)
            elif context["DOMAIN"] == "Taxes Paid":
                context["TRIAL_BALANCE"] = str("No Value")
                return str("No Value")
        else:
            context["TRIAL_BALANCE"] = str("No Value")
            return str("No Value")

