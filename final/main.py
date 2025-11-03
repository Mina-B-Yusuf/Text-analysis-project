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
        print(f"Results successfully saved to {filename}"))


#========================================================================================================================
# Menu
#========================================================================================================================

def main():
    data = load_data()
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
        try:
            file_choice = int(input("Choose a file number: ")) - 1
        except ValueError:
            print("Please enter an integer.")
            return False
            continue

        
        print ('''
        ==============================================''')

        if choice == 1 : # load text file
            print("Available text files:")
            files = [f for f in os.listdir("texts") if f.endswith(".txt")]
            i = 1
            for file in files:
                print(f"{i}. {file}")
                i += 1

            # ---- Safely get file choice ----
            try:
                file_choice = int(input("Choose a file number: ")) - 1
            except ValueError:
                print("❌ Please enter a valid integer.")
                return False

            # ---- Check if file number is valid ----
            if 0 <= file_choice < len(files):
                filename = os.path.join("texts", files[file_choice])
                print(f"Processing {filename}...")
                run_processing_from_main(filename)
            else:
                print("Please select one of files.")
                return False


        elif choice == 2 and data: # display basic statistics
            print("--------- Basic Statistics---------")
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



        elif choice == 3: # word frequency analysis
            print ("--------- Word Analysis ---------")
            print(f"Processing {filename}...")
            word_analysis(data)
            print('''
                1. Visuals for Word Analysis
                2. Back to menu''')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                word_analysis_visuals(data)
            continue

        elif choice == 4:
            print ("--------- Sentence Analysis ---------")
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

        elif choice == 5:
            print ("--------- Character Analysis ---------")
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

        elif choice == 6:
            print ('6')   # export resultat
            saving_stats(data)

        else: 
            break      #break the loop
            print (7)   # exit
        print('press enter to continue...')

if __name__ == "__main__":
    main()