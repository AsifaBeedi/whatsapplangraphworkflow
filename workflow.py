from w_crew import whatsapp_crew

async def process_message_node(message: str):
    # Initialize state with the message
    initial_state = {
        "message": message,
        "processed_message": "",
        "wiki_info": "",
        "final_response": ""
    }
    
    # Run the workflow and await the result
    final_state = await whatsapp_crew.ainvoke(initial_state)
    
    # Return just the string response
    return final_state["final_response"]
