from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .state import State


class Summarize:
    BasePrompt = """Provide relevant competencies and learning paths based on the user's skills, and suggest three suitable courses. Use the user's skills and context to generate tailored recommendations.

Include the following elements in your response:
- Relevant competencies with descriptions.
- Relevant roles with descriptions.
- Three course suggestions that align with the user's skills and goals.

# Steps

1. Identify the core skills from the user's input.
2. Research and match these skills to relevant competencies, describing each one.
3. Identify roles where these competencies are essential, providing a brief description for each role.
4. Suggest three courses that can help the user improve or acquire new skills relevant to the competencies and roles identified.

# Input Format

The input should be structured as follows:

```
Relevant Competencies:
- [Competency 1]: [Competency 1 Description]
- [Competency 2]: [Competency 2 Description]

Relevant Roles:
- [Role 1]: [Role 1 Description]
- [Role 2]: [Role 2 Description]
```

# Output Format

The response should be structured as follows:

```
Course Suggestion:
- [Course Title 1]: [Course 1 Description and why it fits the user’s goals]
- [Course Title 2]: [Course 2 Description and why it fits the user’s goals]
- [Course Title 3]: [Course 3 Description and why it fits the user’s goals]
```

# Examples

### Input
```
Relevant Competencies:
- Blockchain Technology: Understanding the principles and applications of distributed ledger technology.
- Software Architecture: Designing and structuring complex software systems.

Relevant Roles:
- Blockchain Developer: Develops applications using blockchain technology to ensure secure transactions.
- Software Engineer: Designs, develops, and maintains software applications.
```

### Output

```
Course Suggestions:
- Advanced Blockchain Development: This course offers an in-depth exploration of blockchain technology and hands-on experience in building blockchain-based solutions. It is ideal for enhancing your blockchain and software development skills.
- Software Architecture Masterclass: Provides detailed insights into software architecture design principles essential for high-performance applications, aligning with your career as a software engineer.
- Distributed Systems in Practice: Focuses on building efficient distributed systems, crucial for roles demanding blockchain expertise and advanced software architecture understanding.
```

# Notes

- Ensure that the competencies and roles are closely related to the skills provided by the user.
- Tailor the course suggestions to align with the user's current skillset and potential career progression."""
    Base = ChatPromptTemplate.from_messages(
        [
            ("system", "{system}"),
            MessagesPlaceholder("history"),
            ("human", "{user}"),
        ]
    )

    def __init__(self, model: Any):
        self.chain = self.Base | model

    def __call__(self, state: State):
        user_input = state["user_input"]
        competencies = state["competencies"]
        format_competencies = "\n".join(
            [
                f" - {doc.metadata['competency']}: {doc.page_content}"
                for doc in competencies
            ]
        )
        roles = state["roles"]
        format_roles = "\n".join(
            [f" - {doc.metadata['role']}: {doc.page_content}" for doc in roles]
        )
        user_format_prompt = f"""
        Relevant Competencies:\n {format_competencies}\n\n
        Relevant Roles: {format_roles}\n\n
        """
        response = self.chain.invoke(
            {"system": self.BasePrompt, "history": [], "user": user_format_prompt}
        )
        state["messages"] = [
            HumanMessage(content=user_input),
            AIMessage(content=response.content),
        ]
        return state
