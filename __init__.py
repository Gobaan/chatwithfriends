import azure.functions as func

async def main(context: func.Context, data: str) -> dict:
    action = {
        "actionName": "sendToAll",
        "data": f"[{context.binding_data['request']['connectionContext']['userId']}] {data}",
        "dataType": context.binding_data['dataType'],
    }
    # UserEventResponse directly return to caller
    response = { 
        "data": '[SYSTEM] ack.',
        "dataType" : "text",
    }
    context.bindings["actions"] = action
    return response
