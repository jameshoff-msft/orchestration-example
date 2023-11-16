import semantic_kernel as sk
from plugins.DatabasePlugin.Database import Database
from plugins.MathPlugin.Math import Math
# from semantic_kernel.planning.basic_planner import BasicPlanner
# from semantic_kernel.planning.sequential_planner import SequentialPlanner
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion
)
import json

import dotenv

dotenv.load_dotenv(".env")

async def processPlan(kernel, plan):
    db_plugin = kernel.import_skill(Database(), "DatabasePlugin")
    math_plugin = kernel.import_skill(Math(), "MathPlugin")

    output = None
    context = None
    for p in plan["steps"]:
        if p["operation"] == "error":
            print(p["reason"])
            return p["reason"]
        if p["operation"] == "getTrialBalance":
            if context is None:
                context = kernel.create_new_context()
            for pa in p["parameters"]:
                for key, value in pa.items():
                    context[key]=value
            output = await kernel.run_async(
                db_plugin["getTrialBalance"],
                input_context=context
            )
            print(output)
        if p["operation"] == "getValue":
            if context is None:
                context = kernel.create_new_context()
            for pa in p["parameters"]:
                for key, value in pa.items():
                    context[key]=value
            output = await kernel.run_async(
                db_plugin["getValue"],
                input_context=context
            )
            print(output)
        if p["operation"] == "processTieIn":
            if context is None:
                context = kernel.create_new_context()
            output = await kernel.run_async(
                math_plugin["processTieIn"],
                input_context=context
            )
            print(output)


    return output.result

async def doRequest(request):
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

    intent_plugin = kernel.import_semantic_skill_from_directory(
        "plugins", "IntentPlugin"
    )

    intent_result = await kernel.run_async(intent_plugin["Intent"], input_str=request)
    intent_result = intent_result.result.replace('<stop>','')
    print(intent_result)

    if intent_result == "TIEIN_REQUEST":
        test_plugin = kernel.import_semantic_skill_from_directory(
            "plugins", "TestPlugin"
        )

        result = await kernel.run_async(test_plugin["MyTestPlugin"], input_str=request)
        print(result)
        plan = json.loads(result.result.replace('<stop>',''))
        return await processPlan(kernel, plan)
    elif intent_result == "RELEVANT_QUESTION":
        test_plugin = kernel.import_semantic_skill_from_directory(
            "plugins", "TestPlugin"
        )

        result = await kernel.run_async(test_plugin["MyTestPlugin"], input_str=request)
        print(result)
        return result.result
    else:
        pt_plugin = kernel.import_semantic_skill_from_directory(
            "plugins", "PassthroughPlugin"
        )

        result = await kernel.run_async(pt_plugin["Passthrough"], input_str=request)
        print(result)
        return result.result
    

async def main():
    while True:
        try:
            request = input ("What is your request ?").strip()
            print("Final Result: " + await doRequest(request))
        except ValueError:
            print ("Sorry, my only purpose is to talk to N and A")

# Run the main function
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
