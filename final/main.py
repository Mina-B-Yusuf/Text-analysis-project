from stats_functions import load_data, basic_statistics, word_analysis, sentence_analysis, character_analysis
from visuals import basic_statistics_visuals, word_analysis_visuals, sentence_analysis_visuals, character_analysis_visuals

from file_processing import run_processing_from_main
import os
import json

#========================================================================================================================
# SAVING PROCESSED DATA
#========================================================================================================================

def saving_stats(data, filename="results.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("---- Basic Statistics ----\n")
            basic_statistics(data)
            file.write("\n---- Word Analysis ----\n")
            word_analysis(data)
            file.write("\n---- Sentence Analysis ----\n")
            sentence_analysis(data)
            file.write("\n---- Character Analysis ----\n")
            character_analysis(data)
    except IOError as e:
        print("Error saving results:", e)
    else:
        print(f"Results successfully saved to {filename}")


#========================================================================================================================
# ROBUST INPUT HANDELING
#========================================================================================================================


def get_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid integer.")
        return None


#========================================================================================================================
# Menu
#========================================================================================================================

def main():
    data = None
    filename = None

    while True: #keep looping forever — until I manually tell it to stop
        print ('''
        ===============================================
                    ------- Menu -------
        ===============================================
        1. Load text file
        2. Basic statistics
        3. word frequency analysis
        4. Sentence analysis
        5. Character analysis
        6. Export results
        7. Exit''')
        
        menu_choice = get_int("Enter your choice: ")
        if menu_choice is None:
            continue

        
        print ('''
        ==============================================''')

        if menu_choice == 1:  # load data
            print("Available text files:")
            files = [f for f in os.listdir("texts") if f.endswith(".txt")]
            i = 1
            for file in files:
                print(f"{i}. {file}")
                i += 1

            file_choice = get_int("Enter your choice: ") -1
            if file_choice is None:
                continue

            if 0 <= file_choice < len(files):
                filename = os.path.join("texts", files[file_choice])
                print(f"Processing {filename}...")
                run_processing_from_main(filename)
                data = load_data()
                print("✅ File loaded successfully.")
            else:
                print("Invalid selection.")
                continue


        elif menu_choice == 2: # display basic statistics
            print("--------- Basic Statistics---------")
            if 'filename' not in locals() or data is None:
                print("⚠️ Please load a text file first (option 1).")
                continue
            print(f"Processing {filename}...")
            basic_statistics(data)
            print()
            print('''
                1. Visuals for Basics Statistics
                2. Back to menu''')
            
            choice = int(input('Enter your choice: '))
            if choice == 1:
                basic_statistics_visuals(data)
            continue 



        elif menu_choice == 3: # word frequency analysis
            print ("--------- Word Analysis ---------")
            if 'filename' not in locals() or data is None:
                print("⚠️ Please load a text file first (option 1).")
                continue
            print(f"Processing {filename}...")
            word_analysis(data)
            print('''
                1. Visuals for Word Analysis
                2. Back to menu''')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                word_analysis_visuals(data)
            continue

        elif menu_choice == 4:
            print ("--------- Sentence Analysis ---------")
            if 'filename' not in locals() or data is None:
                print("⚠️ Please load a text file first (option 1).")
                continue
            print(f"Processing {filename}...")
            sentence_analysis(data)
            print()
            print('''
                1. Visuals for Sentence analysis
                2. Back to menu''')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                sentence_analysis_visuals(data)
            continue 

        elif menu_choice == 5:
            print ("--------- Character Analysis ---------")
            if 'filename' not in locals() or data is None:
                print("⚠️ Please load a text file first (option 1).")
                continue
            print(f"Processing {filename}...")
            character_analysis(data)
            print()
            print('''
                1. Visuals for character analysis
                2. Back to menu''')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                character_analysis_visuals(data)
            continue

        elif menu_choice == 6:
            if 'filename' not in locals() or data is None:
                print("⚠️ Please load a text file first (option 1).")
                continue
            print(f"saving {filename}...")
            saving_stats(data, filename="results.txt")

        else: 
            break      #break the loop
            print (7)   # exit
        input("Press Enter to return to the menu...")

if __name__ == "__main__":
    main()