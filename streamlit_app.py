
import streamlit as st

from modules.content_standardizer import standardize_text
from modules.quality_checker import check_quality
from modules.ai_reviewer import build_review_prompt


# 1. Page configuration
st.set_page_config(
    page_title="Content Standardization Assistant",
    page_icon="📝",
    layout="wide"
)

st.title("GenAI-Assisted Content Standardization")

st.write(
    "Clean, standardize and review your business content "
    "using Python automation."
)

st.divider()


# 2. Sample input
sample_text = """employee name : john smith

department - INFORMATION TECHNOLOGY

joining date : 15/11/2026

email id : JOHN@GMAIL.COM

status : ACTIVE

employee is responsible for managing
website content and digital assets.
"""


# 3. Raw content input
st.subheader("1. Enter Raw Content")

raw_text = st.text_area(
    "Paste your unformatted content below:",
    value=sample_text,
    height=250
)


# 4. Standardization
if st.button("Standardize Content", type="primary"):

    if not raw_text.strip():
        st.warning("Please enter some content first.")

    else:
        result = standardize_text(raw_text)
        issues = check_quality(result)

        st.session_state["original_text"] = raw_text
        st.session_state["result"] = result
        st.session_state["issues"] = issues

        # Clear previous review and approval data
        for key in [
            "copilot_prompt",
            "approved_content",
            "approved_notes",
            "revised_content",
            "review_notes",
            "approval"
        ]:
            st.session_state.pop(key, None)

        st.success("Content standardization completed!")


# 5. Display standardized content
if "result" in st.session_state:

    result = st.session_state["result"]
    original = st.session_state["original_text"]
    issues = st.session_state["issues"]

    st.divider()
    st.subheader("2. Before and After Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.caption("Original Content")

        st.text_area(
            "Original",
            value=original,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )

    with col2:
        st.caption("Standardized Content")

        st.text_area(
            "Standardized",
            value=result,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )

    # 6. Quality assurance
    st.divider()
    st.subheader("3. Quality Assurance Report")

    metric1, metric2 = st.columns(2)

    with metric1:
        st.metric("Total Words", len(result.split()))

    with metric2:
        st.metric("Quality Findings", len(issues))

    if issues:
        for issue in issues:
            st.warning(
                f"{issue.code}: {issue.message} "
                f"(Line: {issue.line})"
            )
    else:
        st.success("No configured quality issues detected.")

    # 7. Download standardized content
    st.divider()
    st.subheader("4. Download Standardized Content")

    st.download_button(
        label="Download Standardized Content",
        data=result,
        file_name="standardized_content.txt",
        mime="text/plain"
    )

    # 8. Generate Copilot review prompt
    st.divider()
    st.subheader("5. AI-Assisted Content Review")

    st.write(
        "Generate a review prompt and use Microsoft Copilot "
        "to review grammar, readability and consistency."
    )

    if st.button("Generate Copilot Review Prompt"):

        st.session_state["copilot_prompt"] = (
            build_review_prompt(result)
        )

        st.success("Copilot review prompt generated!")

    if "copilot_prompt" in st.session_state:

        st.caption("Copy this prompt into Microsoft Copilot:")

        st.code(
            st.session_state["copilot_prompt"],
            language=None
        )

        st.download_button(
            label="Download Copilot Review Prompt",
            data=st.session_state["copilot_prompt"],
            file_name="copilot_review_prompt.txt",
            mime="text/plain"
        )

    # 9. Human review and approval
    st.divider()
    st.subheader("6. Review and Approve Final Content")

    st.write(
        "Paste the revised content received from Microsoft Copilot. "
        "Review it before approving the final version."
    )

    revised_content = st.text_area(
        "Paste Copilot's revised version here:",
        height=250,
        key="revised_content"
    )

    review_notes = st.text_area(
        "Copilot's suggestions and verification notes:",
        height=120,
        key="review_notes"
    )

    approval = st.checkbox(
        "I have reviewed the content and approve this version.",
        key="approval"
    )

    if st.button("Approve and Save Final Content"):

        if not revised_content.strip():
            st.warning("Please paste the revised content first.")

        elif not approval:
            st.warning("Please confirm your review before approving.")

        else:
            st.session_state["approved_content"] = (
                revised_content.strip()
            )

            st.session_state["approved_notes"] = (
                review_notes.strip()
            )

            st.success("Final content approved and saved!")

    # 10. Display approved content
    if "approved_content" in st.session_state:

        st.divider()
        st.subheader("7. Approved Final Content")

        st.code(
            st.session_state["approved_content"],
            language=None
        )

        if st.session_state["approved_notes"]:
            st.subheader("Review Notes")
            st.write(st.session_state["approved_notes"])

        st.download_button(
            label="Download Approved Content",
            data=st.session_state["approved_content"],
            file_name="approved_final_content.txt",
            mime="text/plain"
        )

else:
    st.info("Enter your content and click Standardize Content to begin.")

st.divider()

st.caption(
    "Note: Automated quality checks do not guarantee "
    "factual or grammatical accuracy. Human review is required."
)
