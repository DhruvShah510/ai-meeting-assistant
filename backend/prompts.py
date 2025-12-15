def build_prompt(clean_text: str) -> str:
    """
    Builds the LLM prompt used to extract summary, action items,
    decisions, and follow-up email from a meeting transcript.
    """

    return f"""
    You are an AI Meeting Assistant.
    You will receive a meeting transcript and must extract structured information.

    Transcript:
    \"\"\"
    {clean_text}
    \"\"\"

    Your tasks:
    1. Provide a concise summary (10–12 lines)
    2. Extract a list of action items.
        Each item must include:
            - task (string)
            - assigned_to (string)
            - assigned_by (string or "Unknown")
    3. Extract all decisions taken during the meeting.
    4. Generate a professional follow-up email summarizing the meeting.

    Return ONLY valid JSON with the following keys:
    - summary
    - action_items
    - decisions
    - follow_up_email

    The JSON must be valid and parseable.
    Do NOT include any text outside the JSON object.
    """
