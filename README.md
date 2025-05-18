# Conicle Test

## [Question 1](q1/README.MD)

### Task:

Using the provided [dataset](https://docs.google.com/spreadsheets/d/1_2BqDT6ipbu_nOguPlXMp0xO0vyBpvXyTTW-0T-_yPY/edit?usp=sharing), create a chatbot that can receive user input in the form of a
competency name or description, and return mapped competencies based on the data. The
chatbot should also be able to suggest or generate course examples related to the identified
competencies.

The chatbot must include a user interface (e.g., via Streamlit or Gradio) that demonstrates a
smooth conversation flow. The end goal is to simulate how a learning assistant could help users
discover relevant competencies and learning paths.

## [Question 2](q2/README.MD)

**Design a Recommendation System and Address the Cold-Start Problem**

### Task:

Explain the difference between implicit and explicit recommendation systems. Then, design
a workflow and architecture for a recommendation system that can handle both types of data
and effectively address the cold-start problem (for new users or new items). Your answer
should include the reasoning behind your chosen models, and explain which algorithms are
most suitable for implicit versus explicit feedback.

In addition, provide a brief overview or example of how you would build and serve the model in
a real-world setting (e.g., through an API or integration with a learning platform). You may
include diagrams or code snippets if necessary to clarify your approach.

## [Question 3](q3/README.MD)

**System Design: Course Transcription & Chatbot Assistant Integration**

### Task:

You are asked to design a system (using Airflow or equivalent) that automates the end-to-end
pipeline for processing educational content into a chatbot-ready knowledge base. The pipeline
should cover the following stages:

- Ingesting course content (audio/video files)
- Transcribing the content
- Parsing and cleaning the transcript
- Extracting key resources (e.g., topics, FAQs, learning objectives)
- Structuring the output for use in a course assistant chatbot (e.g., vector database,
  indexed format)

We are not looking for implementation or code—just the system design.

Please include:

- A diagram (e.g., DAG-style or system components) showing task structure and
  dependencies.
- Brief annotations or labels explaining the key steps and tools you might use (e.g.,
  Whisper, LangChain, FAISS, LlamaIndex).
- (Bonus) Any ideas for how you’d scale this for multiple courses, handle failures/retries,
  or support modular plugin-like components.
