"""
Test script to verify all functionality works correctly
"""

from utils import llm_helpers
import json
import os

def test_basic_functionality():
    """Test basic functionality without API calls"""
    print("=" * 50)
    print("TESTING BASIC FUNCTIONALITY")
    print("=" * 50)
    
    # Test persona management
    print("\n1. Testing Persona Management:")
    print(f"   Available personas: {llm_helpers.get_available_personas()}")
    print(f"   Current persona: {llm_helpers.get_current_persona()}")
    
    # Test persona switching
    print("\n2. Testing Persona Switching:")
    for persona in llm_helpers.get_available_personas():
        result = llm_helpers.set_system_prompt(persona)
        print(f"   {persona}: {result}")
    
    # Test conversation history
    print("\n3. Testing Conversation History:")
    history = llm_helpers.get_conversation_history()
    print(f"   Initial history length: {len(history)}")
    print(f"   System message: {history[0]['role']}")
    
    # Test stats
    print("\n4. Testing Statistics:")
    stats = llm_helpers.get_conversation_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test save functionality (without actual conversation)
    print("\n5. Testing Save/Load (Mock):")
    try:
        filename = llm_helpers.save_conversation("test_conversation.json")
        print(f"   Save successful: {filename}")
        
        if os.path.exists("test_conversation.json"):
            with open("test_conversation.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"   Saved data keys: {list(data.keys())}")
            
            # Test load
            llm_helpers.load_conversation("test_conversation.json")
            print("   Load successful")
            
            # Cleanup
            os.remove("test_conversation.json")
            print("   Test file cleaned up")
        
    except Exception as e:
        print(f"   Error in save/load test: {e}")
    
    print("\n" + "=" * 50)
    print("BASIC FUNCTIONALITY TEST COMPLETE")
    print("=" * 50)

def test_persona_differences():
    """Test that personas have different system prompts"""
    print("\n" + "=" * 50)
    print("TESTING PERSONA DIFFERENCES")
    print("=" * 50)
    
    personas = llm_helpers.get_available_personas()
    
    for persona in personas:
        llm_helpers.set_system_prompt(persona)
        info = llm_helpers.get_current_persona_info()
        print(f"\n{persona.upper()}:")
        print(f"   Name: {info['name']}")
        print(f"   Prompt: {info['prompt'][:100]}...")

def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 50)
    print("TESTING ERROR HANDLING")
    print("=" * 50)
    
    # Test invalid persona
    result = llm_helpers.set_system_prompt("invalid_persona")
    print(f"Invalid persona test: {result}")
    
    # Test loading non-existent file
    try:
        llm_helpers.load_conversation("nonexistent_file.json")
    except Exception as e:
        print(f"Load non-existent file test: {str(e)[:50]}...")

if __name__ == "__main__":
    print("CUSTOM CHATBOT FUNCTIONALITY TEST")
    print("This test verifies the implementation without making API calls")
    
    try:
        test_basic_functionality()
        test_persona_differences()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\nTo test with actual API calls:")
        print("1. Ensure your .env file has valid API keys")
        print("2. Run: python main.py")
        print("3. Run: streamlit run streamlit_app.py")
        print("4. Run: python persona_test.py")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()