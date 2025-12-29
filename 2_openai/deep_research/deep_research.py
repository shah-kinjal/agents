import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run_with_answers(query: str, answers: str):
    async for chunk in ResearchManager().run(query, answers):
        yield chunk

async def ask_clarifying_questions(query: str) -> str:
    manager = ResearchManager()
    questions = await manager.ask_questions(query)
    # format as a numbered markdown list
    lines = []
    for idx, item in enumerate(questions.questions, start=1):
        lines.append(f"{idx}. {item.query}\n   - Reason: {item.reason}")
    return "\n\n".join(lines) if lines else "No clarifying questions generated."


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    ask_button = gr.Button("Optional: Ask Clarifying Questions")
    questions_md = gr.Markdown(label="Clarifying questions")
    answers_textbox = gr.Textbox(label="Your clarifications (optional)", lines=6, placeholder="Provide brief answers to the questions above.")
    run_button = gr.Button("Run Research", variant="primary")
    report = gr.Markdown(label="Report")

    ask_button.click(fn=ask_clarifying_questions, inputs=query_textbox, outputs=questions_md)
    run_button.click(fn=run_with_answers, inputs=[query_textbox, answers_textbox], outputs=report)
    query_textbox.submit(fn=run_with_answers, inputs=[query_textbox, answers_textbox], outputs=questions_md)

ui.launch(inbrowser=True)

