import streamlit as st

from research_copilot.core.config import get_settings


def main() -> None:
    settings = get_settings()

    st.set_page_config(page_title="AI Research Copilot")
    st.title("AI Research Copilot")
    st.caption(f"Environment: {settings.app_env}")
    st.write("Phase 0 project skeleton is ready.")


if __name__ == "__main__":
    main()
