import json
import pandas as pd
from pathlib import Path
from document_processor import DocumentProcessor
from question_generator import QuestionGenerator

def main():
    # Configuration
    INPUT_FILE = "input/21583473018.pdf"  # Change to .docx if needed
    OUTPUT_JSON = "output/questions.json"
    OUTPUT_CSV = "output/questions.csv"
    
    print("🚀 Starting Question Bank Generator...")
    
    # Step 1: Extract text from document
    print("\n📄 Processing document...")
    processor = DocumentProcessor()
    
    if INPUT_FILE.endswith('.pdf'):
        content = processor.extract_text_from_pdf(INPUT_FILE)
    else:
        content = processor.extract_text_from_docx(INPUT_FILE)
    
    print(f"✅ Extracted {len(content)} characters from document")
    
    # Step 2: Generate questions
    print("\n🤖 Generating questions using Qwen3:8b...")
    generator = QuestionGenerator(model_name="qwen3:8b")
    
    print("  - Generating 5 MCQs...")
    mcqs = generator.generate_mcqs(content, num_questions=5)
    
    print("  - Generating 2 short-answer questions...")
    short_answers = generator.generate_short_answer(content, num_questions=2)
    
    # Step 3: Combine and structure output
    all_questions = {
        "mcqs": mcqs,
        "short_answer": short_answers,
        "metadata": {
            "total_mcqs": len(mcqs),
            "total_short_answer": len(short_answers),
            "source_document": INPUT_FILE
        }
    }
    
    # Step 4: Save as JSON
    Path("output").mkdir(exist_ok=True)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ JSON output saved to: {OUTPUT_JSON}")
    
    # Step 5: Convert to CSV for easy viewing
    mcq_df = pd.DataFrame(mcqs)
    short_df = pd.DataFrame(short_answers)
    
    mcq_df['type'] = 'MCQ'
    short_df['type'] = 'Short Answer'
    
    combined_df = pd.concat([mcq_df, short_df], ignore_index=True)
    combined_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    
    print(f"✅ CSV output saved to: {OUTPUT_CSV}")
    
    # Step 6: Display summary
    print("\n" + "="*50)
    print("📊 GENERATION SUMMARY")
    print("="*50)
    print(f"Total MCQs: {len(mcqs)}")
    print(f"Total Short Answer: {len(short_answers)}")
    print(f"\nDifficulty Distribution:")
    print(combined_df['difficulty'].value_counts())
    print("="*50)

if __name__ == "__main__":
    main()