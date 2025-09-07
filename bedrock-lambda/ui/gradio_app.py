import gradio as gr
import requests
from get_terraform_outputs import get_api_gateway_url

DEFAULT_ERROR_MESSAGE = "Error: Failed to get the answer. Please try again later."


def get_aws_answer(question: str, api_gateway_url: str) -> str:
    """Get answer from AWS Bedrock via API Gateway"""
    try:
        response = requests.get(f"{api_gateway_url}?question={question}")
        response.raise_for_status()
        return response.json()["body"]
    except requests.exceptions.RequestException:
        return DEFAULT_ERROR_MESSAGE
    except Exception:
        return DEFAULT_ERROR_MESSAGE


def process_question(question: str) -> str:
    """Process the question and return the answer"""
    if not question.strip():
        return "Please enter a question first."

    api_gateway_url = get_api_gateway_url()
    if not api_gateway_url:
        return DEFAULT_ERROR_MESSAGE

    return get_aws_answer(question, api_gateway_url)


def create_interface():
    """Create and configure the Gradio interface"""

    # Custom CSS for better styling
    css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .example-questions {
        background-color: var(--block-background-fill);
        border: 1px solid var(--border-color-primary);
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .example-questions h4 {
        color: var(--body-text-color);
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    .example-questions ul {
        color: var(--body-text-color);
        margin: 0;
        padding-left: 1.2rem;
    }
    .example-questions li {
        margin-bottom: 0.25rem;
    }
    """

    with gr.Blocks(css=css, title="AWS Service Answerer") as demo:
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🔧 AWS Service Answerer</h1>
            <p>Ask questions about AWS services and get answers powered by Amazon Bedrock.</p>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                question_input = gr.Textbox(
                    label="Enter your AWS service question:",
                    placeholder="e.g., What is the difference between S3 and EBS?",
                    lines=4,
                    info="Ask any question related to AWS services",
                )

                submit_btn = gr.Button("Get Answer", variant="primary", size="lg")

                # Example questions
                gr.HTML("""
                <div class="example-questions">
                    <h4>Example Questions:</h4>
                    <ul>
                        <li>What is AWS Lambda?</li>
                        <li>How do I set up an S3 bucket?</li>
                        <li>What's the difference between EC2 and ECS?</li>
                        <li>How to configure CloudFront?</li>
                        <li>What is AWS IAM?</li>
                    </ul>
                </div>
                """)

            with gr.Column(scale=1):
                # Output section
                answer_output = gr.Textbox(
                    label="Answer", lines=15, interactive=False, show_copy_button=True
                )

        # About section
        with gr.Accordion("About", open=False):
            gr.Markdown("""
            This application uses **Amazon Bedrock** to provide expert answers about AWS services.
            
            **Features:**
            - Powered by Amazon Nova Lite v1
            """)

        # Event handlers
        submit_btn.click(
            fn=process_question, inputs=question_input, outputs=answer_output
        )

        # Allow Enter key to submit
        question_input.submit(
            fn=process_question, inputs=question_input, outputs=answer_output
        )

    return demo


def main():
    """Main function to launch the Gradio interface"""
    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)


if __name__ == "__main__":
    main()
