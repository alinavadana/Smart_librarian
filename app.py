import streamlit as st
import time

from src.moderation import contains_offensive_language
from src.recommender import recommend_book
from src.bots import (
    generate_main_bot_response,
    generate_grumpy_bot_response,
    generate_enthusiastic_bot_response
)
from src.vector_store import index_books
from src.history import (
    load_conversations,
    append_conversation,
    clear_conversations,
    create_conversation_entry,
    save_conversations
)


WARNING_LINES = [
    "Did you just...",
    "DID YOU JUST CURSE?",
    "Oh wow. Everybody, look!",
    "We got a little keyboard warrior boy in here.",
    "...or girl.",
    "It's really hard to see through this screen.",
    "SHAME!",
    "One more stunt like that, and I may personally haunt this interface every time you try to type.",
    "No, seriously, I dish out IRL curses.",
    "This is your official and last warning."
]


if "warning_active" not in st.session_state:
    st.session_state.warning_active = False

if "warning_step" not in st.session_state:
    st.session_state.warning_step = 0

if "warning_revealed_chars" not in st.session_state:
    st.session_state.warning_revealed_chars = 0

if "books_indexed" not in st.session_state:
    st.session_state.books_indexed = False

if "conversations" not in st.session_state:
    st.session_state.conversations = load_conversations()

if "selected_conversation_id" not in st.session_state:
    st.session_state.selected_conversation_id = None


def get_current_warning_line() -> str:
    return WARNING_LINES[st.session_state.warning_step]


def get_visible_warning_text() -> str:
    current_line = get_current_warning_line()
    return current_line[:st.session_state.warning_revealed_chars]


def reveal_next_character():
    current_line = get_current_warning_line()
    if st.session_state.warning_revealed_chars < len(current_line):
        st.session_state.warning_revealed_chars += 1


def is_current_line_fully_revealed() -> bool:
    current_line = get_current_warning_line()
    return st.session_state.warning_revealed_chars >= len(current_line)


def go_to_next_warning_line():
    if st.session_state.warning_step < len(WARNING_LINES) - 1:
        st.session_state.warning_step += 1
        st.session_state.warning_revealed_chars = 0


def trigger_warning():
    st.session_state.warning_active = True
    st.session_state.warning_step = 0
    st.session_state.warning_revealed_chars = 0


def get_steven_face() -> str:
    current_line = get_current_warning_line()

    thinking_lines = {
        "...or girl.",
        "It's really hard to see through this screen."
    }

    if current_line in thinking_lines:
        return "🤔"

    return "😠"


def is_last_warning_line() -> bool:
    return st.session_state.warning_step == len(WARNING_LINES) - 1


def close_warning():
    st.session_state.warning_active = False
    st.session_state.warning_step = 0
    st.session_state.warning_revealed_chars = 0


def get_selected_conversation():
    if st.session_state.selected_conversation_id is None:
        return None

    for conversation in st.session_state.conversations:
        if conversation["id"] == st.session_state.selected_conversation_id:
            return conversation

    return None


def update_selected_conversation(updated_conversation: dict):
    for i, conversation in enumerate(st.session_state.conversations):
        if conversation["id"] == updated_conversation["id"]:
            st.session_state.conversations[i] = updated_conversation
            break

    save_conversations(st.session_state.conversations)


def select_conversation(conversation_id: str):
    st.session_state.selected_conversation_id = conversation_id


def render_warning_overlay():
    visible_text = get_visible_warning_text()
    steven_face = get_steven_face()

    st.markdown(
        f"""
        <style>
        .warning-overlay {{
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.90);
            z-index: 9998;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .warning-wrapper {{
            width: min(1000px, 92vw);
            text-align: center;
            position: relative;
        }}

        .speech-bubble {{
            background: #fff8dc;
            color: #111;
            border: 6px solid #111;
            border-radius: 28px;
            padding: 32px;
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.4;
            box-shadow: 0 10px 0 #111;
            margin-bottom: 24px;
        }}

        .steven-face {{
            font-size: 7rem;
            filter: drop-shadow(0 6px 0 #111);
            margin-bottom: 10px;
        }}

        .warning-subtitle {{
            color: white;
            font-size: 1.1rem;
            margin-top: 12px;
            opacity: 0.9;
        }}

        div[data-testid="stButton"] {{
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10000;
            width: 280px;
        }}

        div[data-testid="stButton"] > button {{
            width: 100%;
            font-size: 1.1rem;
            font-weight: 700;
            border-radius: 14px;
            padding: 0.9rem 1rem;
        }}
        </style>

        <div class="warning-overlay">
            <div class="warning-wrapper">
                <div class="speech-bubble">{visible_text}</div>
                <div class="steven-face">{steven_face}</div>
                <div class="warning-subtitle">Steven has taken over the screen.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if is_current_line_fully_revealed():
        button_label = "Fine, I'll behave." if is_last_warning_line() else "Next"

        if st.button(
            button_label,
            key=f"steven_button_{st.session_state.warning_step}",
            use_container_width=True
        ):
            if is_last_warning_line():
                close_warning()
            else:
                go_to_next_warning_line()

            st.rerun()


if st.session_state.warning_active:
    render_warning_overlay()

    if not is_current_line_fully_revealed():
        time.sleep(0.015)
        reveal_next_character()
        st.rerun()

    st.stop()


st.markdown(
    """
    <style>
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding-bottom: 80px;
    }

    .chat-row {
        display: flex;
        margin: 14px 0;
        width: 100%;
    }

    .chat-row.user {
        justify-content: flex-end;
    }

    .chat-row.bot {
        justify-content: flex-start;
    }

    .chat-message-group {
        max-width: 75%;
    }

    .chat-message-group.user {
        text-align: right;
    }

    .chat-message-group.bot {
        text-align: left;
    }

    .chat-name {
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 6px;
        opacity: 0.8;
        padding: 0 4px;
    }

    .chat-bubble {
        padding: 14px 18px;
        border-radius: 18px;
        font-size: 1rem;
        line-height: 1.5;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        white-space: pre-wrap;
    }

    .chat-bubble.user {
        background: #2563eb;
        color: white;
        border-bottom-right-radius: 6px;
    }

    .chat-bubble.storyteller {
        background: #f3f4f6;
        color: #111827;
        border-bottom-left-radius: 6px;
    }

    .chat-bubble.steven {
        background: #fee2e2;
        color: #7f1d1d;
        border-bottom-left-radius: 6px;
    }

    .chat-bubble.crispy {
        background: #fef3c7;
        color: #92400e;
        border-bottom-left-radius: 6px;
    }

    .typing-row {
        display: flex;
        justify-content: flex-start;
        margin: 8px 0 16px 0;
    }

    .typing-bubble {
        background: #e5e7eb;
        padding: 12px 16px;
        border-radius: 16px;
        display: inline-flex;
        gap: 6px;
        align-items: center;
    }

    .typing-dot {
        width: 8px;
        height: 8px;
        background: #6b7280;
        border-radius: 50%;
        display: inline-block;
        animation: blink 1.4s infinite ease-in-out both;
    }

    .typing-dot:nth-child(1) {
        animation-delay: -0.32s;
    }

    .typing-dot:nth-child(2) {
        animation-delay: -0.16s;
    }

    .summary-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 28px;
    }

    .summary-card {
        width: min(760px, 90%);
        background: #e0f2fe;
        color: #0c4a6e;
        border-radius: 20px;
        padding: 20px 24px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        text-align: left;
    }

    .summary-title {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 12px;
        text-align: center;
    }

    @keyframes blink {
        0%, 80%, 100% {
            transform: scale(0.6);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


def render_user_message(text: str):
    st.markdown(
        f"""
        <div class="chat-row user">
            <div class="chat-message-group user">
                <div class="chat-name">You</div>
                <div class="chat-bubble user">
                    {text}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_bot_message(name: str, text: str, variant: str):
    st.markdown(
        f"""
        <div class="chat-row bot">
            <div class="chat-message-group bot">
                <div class="chat-name">{name}</div>
                <div class="chat-bubble {variant}">
                    {text}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_typing_indicator(name: str):
    st.markdown(
        f"""
        <div class="typing-row">
            <div class="typing-bubble">
                <span style="font-size: 0.85rem; font-weight: 600; margin-right: 8px;">{name}</span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_centered_summary(text: str):
    st.markdown(
        f"""
        <div class="summary-wrapper">
            <div class="summary-card">
                <div class="summary-title">Full Summary</div>
                {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with st.sidebar:
    st.title("Smart Librarian")

    selected_language = st.selectbox(
        "Choose language / Alege limba",
        ["Romanian", "English"]
    )

    st.markdown("---")
    st.subheader("Conversation History")

    if st.button("New chat"):
        st.session_state.selected_conversation_id = None
        st.rerun()

    if st.button("Clear history"):
        st.session_state.conversations = []
        st.session_state.selected_conversation_id = None
        clear_conversations()
        st.rerun()

    if not st.session_state.conversations:
        st.write("No conversations yet.")
    else:
        for index, conversation in enumerate(reversed(st.session_state.conversations), start=1):
            short_user = conversation["user"][:40]
            if len(conversation["user"]) > 40:
                short_user += "..."

            label = f"{index}. {short_user}"

            if st.button(label, key=f"history_{conversation['id']}"):
                select_conversation(conversation["id"])
                st.rerun()


st.title("Smart Librarian")
st.write("Tell me what kind of book you are looking for.")

if not st.session_state.books_indexed:
    try:
        index_books()
        st.session_state.books_indexed = True
    except Exception as e:
        st.error(f"Indexing error: {e}")

user_query = st.chat_input("Tell me what kind of book you want:")

if user_query:
    if contains_offensive_language(user_query):
        trigger_warning()
        st.rerun()

    recommendation = recommend_book(user_query)

    typing_placeholder = st.empty()
    typing_placeholder.markdown(
        """
        <div class="chat-container">
            <div class="typing-row">
                <div class="typing-bubble">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    main_response = generate_main_bot_response(
        user_query,
        recommendation,
        selected_language
    )
    grumpy_response = generate_grumpy_bot_response(
        user_query,
        recommendation,
        selected_language
    )
    enthusiastic_response = generate_enthusiastic_bot_response(
        user_query,
        recommendation,
        selected_language
    )

    typing_placeholder.empty()

    conversation_entry = create_conversation_entry(
        user_query=user_query,
        recommendation=recommendation,
        main_response=main_response,
        grumpy_response=grumpy_response,
        enthusiastic_response=enthusiastic_response
    )

    conversation_entry["show_storyteller"] = False
    conversation_entry["show_steven"] = False
    conversation_entry["show_crispy"] = False
    conversation_entry["is_animating"] = True

    st.session_state.conversations.append(conversation_entry)
    append_conversation(conversation_entry)
    st.session_state.selected_conversation_id = conversation_entry["id"]
    st.rerun()


selected_conversation = get_selected_conversation()

if selected_conversation:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    render_user_message(selected_conversation["user"])

    if not selected_conversation.get("show_storyteller", False):
        render_typing_indicator("Storyteller is typing")
        time.sleep(1.2)
        selected_conversation["show_storyteller"] = True
        update_selected_conversation(selected_conversation)
        st.rerun()

    render_bot_message(
        "Storyteller",
        f"<strong>Recommended Book:</strong> {selected_conversation['title']} by {selected_conversation['author']}<br><br>{selected_conversation['main']}",
        "storyteller"
    )

    if not selected_conversation.get("show_steven", False):
        render_typing_indicator("Steven is typing")
        time.sleep(1.2)
        selected_conversation["show_steven"] = True
        update_selected_conversation(selected_conversation)
        st.rerun()

    render_bot_message(
        "Steven",
        selected_conversation["grumpy"],
        "steven"
    )

    if not selected_conversation.get("show_crispy", False):
        render_typing_indicator("Crispy is typing")
        time.sleep(1.2)
        selected_conversation["show_crispy"] = True
        selected_conversation["is_animating"] = False
        update_selected_conversation(selected_conversation)
        st.rerun()

    render_bot_message(
        "Crispy",
        selected_conversation["enthusiastic"],
        "crispy"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    render_centered_summary(selected_conversation["summary"])
else:
    st.info("Start a new chat or open a conversation from the sidebar.")