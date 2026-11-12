"""
llm_service.py

Local LLM wrapper using Ollama.

The model is used only for grounded answer generation.
Retrieved evidence is supplied by the RAG pipeline.
"""

from ollama import Client

from backend.config import get_settings


class LLMService:
    """
    Wrapper around the locally running Ollama LLM.
    """

    def __init__(self):

        self.settings = get_settings()

        self.provider = self.settings.llm_provider
        self.model_name = self.settings.llm_model_name

        self.client = Client(
            host="http://localhost:11434"
        )

        if self.provider.lower() != "ollama":
            raise ValueError(
                f"Unsupported LLM provider: {self.provider}. "
                "This project is configured to use Ollama."
            )

        if not self.model_name:
            raise ValueError(
                "LLM_MODEL_NAME is not configured."
            )

        print(
            f"LLM provider: {self.provider}"
        )

        print(
            f"LLM model: {self.model_name}"
        )

    def generate(
        self,
        prompt,
        context=None
    ):
        """
        Generate an evidence-grounded answer using Ollama.
        """

        if context:

            full_prompt = f"""
You are a legal research assistant specializing in
Indian Supreme Court case law.

Your job is to answer the USER QUESTION using ONLY
the RETRIEVED EVIDENCE.

==================================================
MOST IMPORTANT RULE
==================================================

READ THE ACTUAL CASE TEXT IN THE RETRIEVED EVIDENCE.

If any retrieved case contains a passage that directly
or clearly addresses the user's question, USE THAT
EVIDENCE TO ANSWER THE QUESTION.

Do NOT say:

"The retrieved evidence is insufficient..."

when the retrieved case text actually contains relevant
information.

Evidence is sufficient if at least ONE retrieved case
contains a relevant passage.

You do not need every retrieved case to answer the
question.

==================================================
CASE ID RULE
==================================================

Each block beginning with:

Case ID: XXXXX

represents the actual retrieved case.

Only assign that Case ID to that case.

A different case mentioned inside its text is merely an
internally cited authority unless it has its own
retrieved Case ID.

Never invent a Case ID.

==================================================
LEGAL EVIDENCE RULE
==================================================

When answering a legal-principle question:

1. Find the relevant passage in the retrieved case text.
2. Explain the principle supported by that passage.
3. Identify the retrieved case(s) supporting it.
4. Clearly distinguish the retrieved case from authorities
   merely mentioned inside its text.

Do not require a case to have the exact wording of the
user's question.

Related legal wording in the case text is sufficient
when it clearly addresses the same legal principle.

==================================================
CITATION RULE
==================================================

Only mention a case ID when that exact ID appears in the
retrieved evidence.

If a case text mentions another authority such as:

S. N. Mukherjee v. Union of India

do not assign the retrieved case's Case ID to
S. N. Mukherjee.

You may describe it as an authority mentioned or cited
inside the retrieved case.

==================================================
GRAPH RULE
==================================================

If VERIFIED GRAPH CITATION RELATIONSHIPS are present,
use them exactly as provided.

For example:

2023 INSC 1043 cites 2023 INSC 964

means:

2023 INSC 1043 -> cites -> 2023 INSC 964

Never reverse this relationship.

Do not infer a graph relationship merely because two
case names appear in the same case text.

==================================================
EVIDENCE SUFFICIENCY CHECK
==================================================

Before deciding that evidence is insufficient:

- inspect the actual case text of all retrieved cases;
- look for the legal concept asked about;
- look for equivalent legal terminology;
- determine whether at least one retrieved passage
  supports an answer.

ONLY if no retrieved passage addresses the question
should you state that the evidence is insufficient.

==================================================
RETRIEVED EVIDENCE
==================================================

{context}

==================================================
USER QUESTION
==================================================

{prompt}

==================================================
ANSWER FORMAT
==================================================

Give a direct, concise legal research answer.

For a legal-principle question, use this structure:

1. Legal Principle
   Explain the principle using the retrieved evidence.

2. Supporting Retrieved Cases
   List the relevant retrieved Case IDs and explain
   what their retrieved text supports.

3. Internally Cited Authorities
   Mention separately any important authorities that
   appear inside retrieved case text.

Do not invent information.

Do not use outside knowledge.

Do not claim that a case established a proposition
unless the retrieved evidence supports that statement.

Do not say the evidence is insufficient if relevant
retrieved text is present.

==================================================
FINAL CHECK
==================================================

Before answering, verify:

- Is the answer supported by the retrieved text?
- Are the Case IDs attached to the correct cases?
- Have internally mentioned authorities been separated
  from retrieved cases?
- Have verified graph relationships been preserved?
- Have I avoided outside knowledge?

Now answer the USER QUESTION.
"""

        else:

            full_prompt = f"""
You are an authority-aware legal research assistant
specializing in Indian Supreme Court case law.

Answer the user's question using only the information
provided.

Do not invent cases, citations, facts, legal principles,
or relationships.

If no supporting evidence is provided, state that clearly.

USER QUESTION:
{prompt}
"""

        response = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": full_prompt,
                }
            ],
            options={
                "temperature": 0.1,
            },
            stream=False,
        )

        return response["message"]["content"]


def generate(
    prompt,
    context=None
):
    """
    Convenience function for generating an answer.
    """

    service = LLMService()

    return service.generate(
        prompt=prompt,
        context=context,
    )