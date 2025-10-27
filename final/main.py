from stats_functions import load_data, basic_statistics, word_analysis, sentence_analysis, character_analysis
from visuals import basic_statistics_visuals, word_analysis_visuals, sentence_analysis_visuals, character_analysis_visuals

from file_processing import run_processing_from_main
import os

def main():
    data = load_data()
    while True: #keep looping forever — until I manually tell it to stop
        print ('''--- Menu ---
        1. Load text file
        2. Basic statistics
        3. word frequency analysis
        4. Sentence analysis
        5. character analysis
        6. export resultatcd fina
        7. exit''')
        choice = int(input('Enter your choice: '))

        if choice == 1 : # load text file
            print("Available text files:")
            files = [f for f in os.listdir("texts") if f.endswith(".txt")]
            i = 1
            for file in files:
                print(f"{i}. {file}")
                i += 1

            file_choice = int(input("Choose a file number: ")) - 1

            if 0 <= file_choice < len(files):
                filename = os.path.join("texts", files[file_choice])
                print(f"Processing {filename}...")
                run_processing_from_main(filename)  
                data = load_data()  
            else:
                print("Invalid choice.")


        elif choice == 2 and data: # display basic statistics
            print("--------- Basic Statistics---------")
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
            print (6)   # export resultat


        else: 
            break      #break the loop
            print (7)   # exit
        print('press enter to continue...')

if __name__ == "__main__":
    main()