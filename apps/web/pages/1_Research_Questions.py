import httpx
import streamlit as st

from research_copilot.core.config import get_settings


def api_url(path: str) -> str:
    settings = get_settings()
    return f"{settings.api_base_url.rstrip('/')}{path}"


def fetch_research_questions() -> list[dict]:
    response = httpx.get(api_url("/research-questions"), timeout=10.0)
    response.raise_for_status()
    return response.json()


def create_research_question(payload: dict[str, str | None]) -> dict:
    response = httpx.post(api_url("/research-questions"), json=payload, timeout=10.0)
    response.raise_for_status()
    return response.json()


def normalize_optional(value: str) -> str | None:
    value = value.strip()
    return value or None


def main() -> None:
    settings = get_settings()

    st.set_page_config(page_title="Research Questions")
    st.title("Research Questions")
    st.caption(f"Phase 0 MVP | API: {settings.api_base_url}")

    with st.form("create_research_question", clear_on_submit=True):
        title = st.text_input("Question title")
        description = st.text_area("Description", height=120)
        company = st.text_input("Company")
        theme = st.text_input("Theme")
        submitted = st.form_submit_button("Create question")

    if submitted:
        if not title.strip():
            st.error("Question title is required.")
        else:
            try:
                create_research_question(
                    {
                        "title": title.strip(),
                        "description": normalize_optional(description),
                        "company": normalize_optional(company),
                        "theme": normalize_optional(theme),
                    }
                )
            except httpx.HTTPError as exc:
                st.error(f"Could not create research question: {exc}")
            else:
                st.success("Research question created.")

    if st.button("Refresh"):
        st.rerun()

    st.subheader("Question list")
    try:
        questions = fetch_research_questions()
    except httpx.HTTPError as exc:
        st.error(f"Could not load research questions: {exc}")
        return

    if not questions:
        st.info("No research questions yet.")
        return

    for question in questions:
        with st.container(border=True):
            st.markdown(f"**{question['title']}**")
            st.caption(
                f"Status: {question.get('status', 'unknown')} | "
                f"Created: {question.get('created_at', 'unknown')}"
            )
            if question.get("description"):
                st.write(question["description"])
            context = [
                value
                for value in [question.get("company"), question.get("theme")]
                if value
            ]
            if context:
                st.write(" | ".join(context))


if __name__ == "__main__":
    main()
