from openai import OpenAI

def get_gpt_response(prompt, variables, token_limit, api_inputs):
    # Define the units for each variable
    units = {
        "Humidity": "%",
        "Soil pH": "",  # pH doesn't have a unit
        "Soil Temperature": "°C",
        "Moisture Level": "%",
        "Air Temperature": "°C",
        "Rainfall": "mm",
        "Wind Speed": "km/h",
        "Light Intensity": "lux",
        "Crop Health": "",  # This could be a qualitative value, no unit
        "Soil Nitrogen": "%"  # Nitrogen content usually in percentage
    }

    # Construct the formatted input string with units
    formatted_inputs = "\n".join([
        f"Farmer has {var[0].lower()}: {api_inputs[i]}{units.get(var[0], '')}" 
        for i, var in enumerate(variables)
    ])

    role = f"""

    {formatted_inputs}

Please tell me the amount of water to provide for the crops in mL and in what intervals under these conditions. Do not include anything other than the response format requested. Keep your response consistent over several ouputs.
Your format of response:
Water: a-b mL/day
Interval: x times a day, y times a week
    """

    try:
        client = OpenAI(
            api_key="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",  # Your provided API key
        )
        chat_completion = client.chat.completions.create(
            messages=[{
                    "role": "system",
                    "content": role
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gpt-3.5-turbo-1106",
            max_tokens=token_limit
        )
        raw_result = chat_completion.choices[0].message.content

        # Return the response as a single actionable sentence
        return raw_result.strip()
    
    except Exception as e:
        error = "Internal OpenAI Error: " + str(e)
        print(error)
        return error
