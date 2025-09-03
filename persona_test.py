"""
Persona Testing Script for Week 2 Assignment Part 2
Tests all 3 personas with identical questions to demonstrate differences
"""

from utils import llm_helpers
import json
from datetime import datetime

def test_personas():
    """Test all personas with the same questions and save results"""
    
    # Test questions covering different domains
    test_questions = [
        "How do I start a business?",
        "Write a short story about a robot discovering emotions",
        "Explain how machine learning works",
        "What's the best way to manage a team?",
        "How do I solve creative blocks?"
    ]
    
    personas = llm_helpers.get_available_personas()
    results = {
        "test_date": datetime.now().isoformat(),
        "questions": test_questions,
        "results": {}
    }
    
    print("PERSONA TESTING STARTED")
    print("=" * 60)
    print(f"Testing {len(personas)} personas with {len(test_questions)} questions")
    print("=" * 60)
    
    for persona in personas:
        print(f"\nTesting {persona.upper()} persona...")
        results["results"][persona] = {}
        
        # Switch to persona
        llm_helpers.set_system_prompt(persona)
        persona_info = llm_helpers.get_current_persona_info()
        
        for i, question in enumerate(test_questions, 1):
            print(f"  Question {i}/{len(test_questions)}: {question[:50]}...")
            
            try:
                # Clear history for each question to avoid context bleeding
                llm_helpers.clear_history()
                response = llm_helpers.chat(question)
                
                results["results"][persona][question] = {
                    "response": response,
                    "persona_info": persona_info
                }
                
                print(f"    Response received ({len(response)} chars)")
                
            except Exception as e:
                print(f"    Error: {e}")
                results["results"][persona][question] = {
                    "error": str(e),
                    "persona_info": persona_info
                }
    
    # Save results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"persona_test_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {filename}")
    return results

def display_comparison(results=None):
    """Display a formatted comparison of persona responses"""
    
    if not results:
        # Try to load the most recent test results
        import os
        import glob
        
        test_files = glob.glob("persona_test_results_*.json")
        if not test_files:
            print("No test results found. Run test_personas() first.")
            return
        
        # Load most recent file
        latest_file = max(test_files, key=os.path.getctime)
        print(f"Loading results from: {latest_file}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    
    print("\n" + "=" * 80)
    print("PERSONA COMPARISON RESULTS")
    print("=" * 80)
    print(f"Test Date: {results['test_date']}")
    
    for question in results["questions"]:
        print(f"\nQUESTION: {question}")
        print("-" * 60)
        
        for persona, data in results["results"].items():
            if question in data:
                persona_name = data[question]["persona_info"]["name"]
                response = data[question].get("response", "ERROR")
                
                print(f"\n[{persona_name.upper()}]:")
                if "error" in data[question]:
                    print(f"Error: {data[question]['error']}")
                else:
                    # Truncate long responses for comparison view
                    display_response = response[:300] + "..." if len(response) > 300 else response
                    print(f"{display_response}")
                print("-" * 40)

def generate_comparison_report():
    """Generate a markdown report comparing personas"""
    
    # Try to load the most recent test results
    import os
    import glob
    
    test_files = glob.glob("persona_test_results_*.json")
    if not test_files:
        print("No test results found. Run test_personas() first.")
        return
    
    # Load most recent file
    latest_file = max(test_files, key=os.path.getctime)
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Generate markdown report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"persona_comparison_report_{timestamp}.md"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("# Persona Comparison Report\n\n")
        f.write(f"**Test Date:** {results['test_date']}\n\n")
        
        f.write("## Personas Tested\n\n")
        personas = list(results["results"].keys())
        for persona in personas:
            # Get persona info from first question
            first_question = results["questions"][0]
            persona_info = results["results"][persona][first_question]["persona_info"]
            f.write(f"### {persona_info['name']}\n")
            f.write(f"**System Prompt:** {persona_info['prompt']}\n\n")
        
        f.write("## Question-by-Question Analysis\n\n")
        
        for i, question in enumerate(results["questions"], 1):
            f.write(f"### Question {i}: {question}\n\n")
            
            for persona in personas:
                if question in results["results"][persona]:
                    persona_name = results["results"][persona][question]["persona_info"]["name"]
                    response = results["results"][persona][question].get("response", "ERROR")
                    
                    f.write(f"**{persona_name}:**\n")
                    if "error" in results["results"][persona][question]:
                        f.write(f"*Error: {results['results'][persona][question]['error']}*\n\n")
                    else:
                        f.write(f"{response}\n\n")
            
            f.write("---\n\n")
        
        f.write("## Key Observations\n\n")
        f.write("*TODO: Add your observations about how each persona responds differently*\n\n")
        f.write("- **Professional Assistant:** [Add observations]\n")
        f.write("- **Creative Companion:** [Add observations]\n") 
        f.write("- **Technical Expert:** [Add observations]\n\n")
    
    print(f"Comparison report generated: {report_filename}")
    return report_filename

if __name__ == "__main__":
    print("Persona Testing Suite")
    print("Choose an option:")
    print("1. Run persona tests")
    print("2. Display comparison")
    print("3. Generate markdown report")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        results = test_personas()
        print("\nTesting complete!")
        
        show_results = input("\nShow results now? (y/n): ").strip().lower()
        if show_results == 'y':
            display_comparison(results)
            
    elif choice == "2":
        display_comparison()
        
    elif choice == "3":
        generate_comparison_report()
        
    else:
        print("Invalid choice")