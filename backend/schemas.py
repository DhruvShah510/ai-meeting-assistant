from typing import List
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class TranscriptRequest(BaseModel):
    """
    Request model for the meeting summarization API.
    """

    transcript_text: Annotated[
        str,
        Field(
            ...,
            description="Raw transcript text from a meeting. Can be messy; preprocessing will be applied.",
            example="John: Good morning everyone. Let's begin today's meeting..."
        )
    ]


class ActionItem(BaseModel):
    """
    Represents a single actionable task extracted from the meeting.
    """

    task: Annotated[
        str,
        Field(
            ...,
            description="Description of the task to be completed.",
            example="Fix minor bugs in the password reset flow"
        )
    ]

    assigned_to: Annotated[
        str,
        Field(
            ...,
            description="Person responsible for completing the task.",
            example="Priya"
        )
    ]

    assigned_by: Annotated[
        str,
        Field(
            ...,
            description="Person who assigned the task. If unclear, marked as 'Unknown'.",
            example="Ahmed"
        )
    ]


class Decision(BaseModel):
    """
    Represents a decision made during the meeting.
    """

    decision: Annotated[
        str,
        Field(
            ...,
            description="Decision taken during the meeting.",
            example="Dashboard deadline remains Friday"
        )
    ]

    made_by: Annotated[
        str,
        Field(
            ...,
            description="Person who proposed or finalized the decision.",
            example="John"
        )
    ]


class SummaryResponse(BaseModel):
    """
    Response model returned by the meeting summarization system.
    """

    summary: Annotated[
        str,
        Field(
            ...,
            description="Concise 10–12 line summary of the meeting."
        )
    ]

    action_items: Annotated[
        List[ActionItem],
        Field(
            ...,
            description="List of extracted tasks with assignee and assigner."
        )
    ]

    decisions: Annotated[
        List[Decision],
        Field(
            ...,
            description="Structured list of decisions with decision maker."
        )
    ]

    follow_up_email: Annotated[
        str,
        Field(
            ...,
            description="Professional follow-up email summarizing the meeting."
        )
    ]
