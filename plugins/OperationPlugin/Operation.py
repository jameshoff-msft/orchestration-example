from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion
)

import dotenv

dotenv.load_dotenv(".env")


class Operation:
    @sk_function(
        description="Returns a JSON array containing the operations that need to be run in the order that they need to be run.",
        name="getOperations",
    )
    @sk_function_context_parameter(
        name="goal",
        description="The ultimate goal that the list of operations must produce.",
    )
    def getOperations(self, context: SKContext) -> str:
        # Initialize the kernel
        kernel = sk.Kernel()
        kernel.add_chat_service(
            "chat_completion",
            AzureChatCompletion(
                dotenv.get_key(".env","AZURE_OPEN_AI__CHAT_COMPLETION_DEPLOYMENT_NAME"),
                dotenv.get_key(".env","AZURE_OPEN_AI__ENDPOINT"),
                dotenv.get_key(".env","AZURE_OPEN_AI__API_KEY"),
            ),
        )
        
        


