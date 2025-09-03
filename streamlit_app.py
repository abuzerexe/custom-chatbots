"""
Streamlit Web Interface for Custom ChatBot
Week 2 Assignment Part 3 - Streamlit Interface
"""

import streamlit as st
from utils import llm_helpers
import json
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="Custom AI ChatBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_persona" not in st.session_state:
        st.session_state.current_persona = llm_helpers.get_current_persona()

def export_chat_history():
    """Export chat history as JSON"""
    if st.session_state.messages:
        export_data = {
            "export_date": datetime.now().isoformat(),
            "persona": st.session_state.current_persona,
            "persona_info": llm_helpers.get_current_persona_info(),
            "messages": st.session_state.messages,
            "stats": llm_helpers.get_conversation_stats()
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    return None

def main():
    # Initialize
    initialize_session_state()
    
    # Header
    st.title("Custom AI ChatBot")
    st.markdown("**Week 2: Conversational LLMs & System Prompt Experimentation**")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Persona selection
        personas = llm_helpers.get_available_personas()
        persona_names = {p: llm_helpers.SYSTEM_PROMPTS[p]["name"] for p in personas}
        
        # Display options with full names
        persona_options = [f"{p} - {persona_names[p]}" for p in personas]
        current_index = personas.index(st.session_state.current_persona)
        
        selected_option = st.selectbox(
            "Choose AI Persona:",
            persona_options,
            index=current_index,
            key="persona_select"
        )
        
        # Extract persona key from selection
        selected_persona = selected_option.split(" - ")[0]
        
        # Update persona if changed
        if selected_persona != st.session_state.current_persona:
            st.session_state.current_persona = selected_persona
            llm_helpers.set_system_prompt(selected_persona)
            # Clear messages when changing persona
            st.session_state.messages = []
            st.rerun()
        
        # Display current system prompt
        current_info = llm_helpers.get_current_persona_info()
        with st.expander("View Current System Prompt", expanded=False):
            st.markdown(f"**{current_info['name']}**")
            st.text_area(
                "System Prompt:",
                value=current_info['prompt'],
                height=150,
                disabled=True,
                key="system_prompt_display"
            )
        
        st.divider()
        
        # Chat controls
        st.header("Chat Controls")
        
        # Clear conversation
        if st.button("Clear Conversation", type="secondary", use_container_width=True):
            st.session_state.messages = []
            llm_helpers.clear_history()
            st.rerun()
        
        # Statistics
        if st.session_state.messages:
            stats = llm_helpers.get_conversation_stats()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Your Messages", stats["user_messages"])
            with col2:
                st.metric("AI Responses", stats["assistant_messages"])
        
        st.divider()
        
        # Export functionality
        st.header("Export")
        if st.session_state.messages:
            export_data = export_chat_history()
            if export_data:
                st.download_button(
                    "Download Chat History",
                    export_data,
                    f"chat_history_{st.session_state.current_persona}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json",
                    use_container_width=True
                )
        else:
            st.info("Start chatting to enable export")
        
        st.divider()
        
        # Instructions
        with st.expander("Usage Tips"):
            st.markdown("""
            **Getting Started:**
            1. Select different personas to see how they respond
            2. Ask the same question to different personas
            3. Notice differences in tone, detail, and approach
            
            **Persona Guide:**
            - **Professional**: Formal business responses
            - **Creative**: Imaginative and artistic responses  
            - **Technical**: Detailed technical explanations
            
            **Tips:**
            - Be specific in your questions
            - Try comparative questions across personas
            - Export conversations for analysis
            """)

    # Main chat interface
    st.header(f"Chat with {llm_helpers.get_current_persona_info()['name']}")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if message["role"] == "assistant":
                    st.caption(f"Generated at {message.get('timestamp', 'Unknown time')} using {message.get('persona', 'Unknown persona')}")

    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to session state
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.messages.append(user_message)
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Sync session state with llm_helpers conversation history
                    llm_helpers.clear_history()
                    for msg in st.session_state.messages[:-1]:  # Exclude the message we just added
                        if msg["role"] == "user":
                            llm_helpers.message_history.append({"role": "user", "content": msg["content"]})
                        elif msg["role"] == "assistant":
                            llm_helpers.message_history.append({"role": "assistant", "content": msg["content"]})
                    
                    response = llm_helpers.chat(user_input)
                    st.write(response)
                    
                    current_time = datetime.now().strftime("%H:%M:%S")
                    current_persona_info = llm_helpers.get_current_persona_info()
                    st.caption(f"Generated at {current_time} using {current_persona_info['name']}")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    response = f"Error: {str(e)}"
        
        # Add assistant response to session state
        assistant_message = {
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "persona": st.session_state.current_persona
        }
        st.session_state.messages.append(assistant_message)
        
        # Rerun to update the interface
        st.rerun()

    # Footer with assignment info
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<div style='text-align: center; color: #666;'>"
            "Week 2 Assignment: Custom Chatbot Interface<br>"
            "Built with Streamlit - Powered by OpenAI API"
            "</div>",
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()