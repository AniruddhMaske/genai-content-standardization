# GenAI-Assisted Content Standardization Workflow

A Python-based application that helps standardize business content, perform automated quality checks, and support AI-assisted content review using Microsoft Copilot.

The project combines Python automation with a Streamlit interface to make content standardization and review easier.

## Features

- **Text Standardization:** Cleans and formats unstructured business content.
- **Quality Assurance:** Identifies configured content quality issues.
- **Before and After Comparison:** Displays original and standardized content side by side.
- **AI-Assisted Review:** Generates prompts that can be used with Microsoft Copilot.
- **Human Approval:** Allows users to review and approve revised content.
- **File Export:** Downloads standardized content, review prompts, and approved content.
- **Automated Testing:** Includes unit tests for core functionality.

## Technologies Used

- Python
- Streamlit
- Microsoft Copilot
- Git and GitHub

## Project Structure

```text
genai-content-standardization/
│
├── app.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── modules/
│   ├── text_cleaner.py
│   ├── content_standardizer.py
│   ├── quality_checker.py
│   └── ai_reviewer.py
│
├── samples/
├── tests/
├── documentation/
│
└── copilot_prompt.txt
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/AniruddhMaske/genai-content-standardization.git
```

**2. Navigate to the project directory**

```bash
cd genai-content-standardization
```

**3. Create a virtual environment (recommended)**

```bash
python -m venv venv
```

**4. Activate the virtual environment**

Windows:

```bash
venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

## Run the Application

Launch the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

## Run the Python CLI

The project also supports command-line content standardization:

```bash
python app.py samples/sample_input.txt
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## How It Works

1. The user enters unformatted business content.
2. Python processes and standardizes the text.
3. Automated quality checks identify configured issues.
4. The application generates a Microsoft Copilot review prompt.
5. The user manually submits the prompt to Microsoft Copilot.
6. The revised content is returned to the application.
7. The user reviews and approves the final content.
8. The approved content can be downloaded.

## Important Note

This project does not directly connect to the Microsoft Copilot API or automatically send content to an external AI service.

Copilot review is performed manually using generated prompts. Human verification is required before approving revised content, especially when factual accuracy is important.

## Learning Outcomes

Through this project, I gained practical experience with:

- Python programming and modular code organization.
- Text processing and standardization.
- Automated quality checks and unit testing.
- Streamlit application development.
- AI-assisted content review workflows.
- Git and GitHub version control.

## Author

**Aniruddh Maske**

GitHub: [AniruddhMaske](https://github.com/AniruddhMaske)
