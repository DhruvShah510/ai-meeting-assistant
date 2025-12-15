import re
import json

def clean_transcript(text: str) -> str:
    """
    Cleans meeting transcript by removing timestamps, extra spaces,
    and normalizing line structure.
    """

    # Remove timestamps like [09:00 AM]
    text = re.sub(r"\[\d{1,2}:\d{2}\s?(AM|PM)\]", "", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n", "\n", text)

    return text.strip()


# def fix_json_output(model_output: str) -> dict:
#     """
#     Attempts to clean and parse the JSON output returned by the LLM.
#     Handles cases like:
#     - JSON wrapped inside ```json ... ```
#     - trailing commas
#     - formatting whitespace
#     """

#     # Remove markdown formatting
#     model_output = model_output.strip()
#     model_output = model_output.replace("```json", "").replace("```", "").strip()

#     # Remove trailing commas before closing objects/arrays
#     model_output = re.sub(r",\s*}", "}", model_output)
#     model_output = re.sub(r",\s*]", "]", model_output)

#     # Now try to load JSON safely
#     try:
#         return json.loads(model_output)
#     except json.JSONDecodeError:
#         # If still broken, attempt minor repairs
#         raise ValueError("LLM returned invalid JSON. Cleaning failed.")

def fix_json_output(model_output: str) -> dict:
    """
    Cleans, parses, and normalizes LLM JSON output
    so it ALWAYS matches the Pydantic schema.
    """

    # -----------------------------
    # 1. Remove markdown wrappers
    # -----------------------------
    model_output = model_output.strip()
    model_output = model_output.replace("```json", "").replace("```", "").strip()

    # -----------------------------
    # 2. Remove trailing commas (LLM safety)
    # -----------------------------
    model_output = re.sub(r",\s*}", "}", model_output)
    model_output = re.sub(r",\s*]", "]", model_output)

    # -----------------------------
    # 3. Parse JSON
    # -----------------------------
    try:
        data = json.loads(model_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM: {e}")

    # -----------------------------
    # 4. Normalize decisions → List[Decision]
    # -----------------------------
    normalized_decisions = []

    for d in data.get("decisions", []):
        # Case 1: decision is a string
        if isinstance(d, str):
            normalized_decisions.append({
                "decision": d,
                "made_by": "Unknown"
            })

        # Case 2: decision is already an object
        elif isinstance(d, dict):
            normalized_decisions.append({
                "decision": d.get("decision", "").strip(),
                "made_by": d.get("made_by", "Unknown").strip()
            })

    data["decisions"] = normalized_decisions

    return data
