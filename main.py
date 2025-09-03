from utils import llm_helpers
import sys

def show_help():
    """Display available commands"""
    print("\n" + "="*50)
    print("CHATBOT COMMANDS")
    print("="*50)
    print("Just type your message to chat")
    print("/persona [name] - Change AI persona (professional/creative/technical)")
    print("/list          - List available personas")
    print("/clear         - Clear conversation history")
    print("/save          - Save conversation to file")
    print("/load [file]   - Load conversation from file") 
    print("/stats         - Show conversation statistics")
    print("/help          - Show this help message")
    print("/exit          - Exit the chatbot")
    print("="*50)

def main():
    print("Welcome to Custom ChatBot!")
    print("="*40)
    print("Type '/help' for available commands")
    print(f"Current persona: {llm_helpers.get_current_persona()}")
    print("Ready to chat!\n")
    
    try:
        user_input = input("You: ").strip()
        
        while user_input.lower() != "exit":
            if not user_input:
                user_input = input("You: ").strip()
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                command = user_input[1:].lower().split()
                
                if command[0] == 'exit':
                    break
                elif command[0] == 'help':
                    show_help()
                elif command[0] == 'clear':
                    llm_helpers.clear_history()
                    print("Conversation history cleared!")
                elif command[0] == 'list':
                    personas = llm_helpers.get_available_personas()
                    current = llm_helpers.get_current_persona()
                    print("\nAvailable Personas:")
                    for persona in personas:
                        marker = ">" if persona == current else " "
                        print(f"  {marker} {persona}")
                    print()
                elif command[0] == 'persona' and len(command) > 1:
                    result = llm_helpers.set_system_prompt(command[1])
                    print(result)
                elif command[0] == 'save':
                    try:
                        filename = llm_helpers.save_conversation()
                        print(f"Conversation saved to: {filename}")
                    except Exception as e:
                        print(f"Error saving: {e}")
                elif command[0] == 'load' and len(command) > 1:
                    try:
                        llm_helpers.load_conversation(command[1])
                        print(f"Conversation loaded from: {command[1]}")
                        print(f"Current persona: {llm_helpers.get_current_persona()}")
                    except Exception as e:
                        print(f"Error loading: {e}")
                elif command[0] == 'stats':
                    stats = llm_helpers.get_conversation_stats()
                    print(f"\nConversation Statistics:")
                    print(f"   Current Persona: {stats['current_persona']}")
                    print(f"   Your Messages: {stats['user_messages']}")
                    print(f"   AI Responses: {stats['assistant_messages']}")
                    print(f"   Total Messages: {stats['total_messages']}")
                else:
                    print(f"Unknown command: /{command[0]}. Type '/help' for available commands.")
            else:
                # Regular chat message
                try:
                    response = llm_helpers.chat(user_input)
                    print(f"Assistant: {response}")
                except Exception as e:
                    print(f"Error getting response: {str(e)}")
            
            user_input = input("\nYou: ").strip()
            
    except KeyboardInterrupt:
        print("\n\nChat interrupted. Goodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
    
    print("Goodbye!")

if __name__ == "__main__":
    main()

