import os
import json
import time

import stats_functions as stats
import visuals
import exporting_data as ed

import file_processing as fp

# --- Run all analyses and store results ---

def run_all_analyses(data):
    """Run all analysis functions once and store their results in one dictionary."""
    all_stats = {
        "basic": stats.basic_statistics(data),
        "word": stats.word_analysis(data),
        "sentence": stats.sentence_analysis(data),
        "character": stats.character_analysis(data)
    }
    return all_stats


def run_analysis(label, filename, data, stat_key, display_func, visual_func, all_stats):
    print(f"------{label}-------")

    if data is None or filename is None:
        print("please load a text file first (option 1). ")
        input ("press Enter to reutrn to the menu...")
        return
    
    print(F"processing {filename} ...")
    display_func(all_stats[stat_key])
    
    print('''
            1. Visuals
            2. Back to menu
    ''')

    choice = get_int("Enter your choice: ")
    if choice == 1: 
        visual_func(data)

#========================================================================================================================
# SAVING PROCESSED DATA
#========================================================================================================================

def saving_stats(all_stats, filename="results.txt"):
    with open("results.json", "w", encoding="utf-8") as json_file:
        json.dump(all_stats, json_file, indent=4, ensure_ascii=False)

    print(f"Processing complete. Results saved to results.json from {filename}")

#========================================================================================================================
# INPUT HANDELING
#========================================================================================================================


def get_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid integer.")
        return None



def getting_file_selection():
    print("Available text files:")
    files = [f for f in os.listdir("texts") if f.endswith(".txt")]
    i = 1
    for file in files:
        print(f"{i}. {file}")
        i += 1

    file_choice = input("Enter your choice: ")

    if file_choice.isdigit(): 
        file_choice -= 1
        if 0 <= file_choice < len(files):
            return os.path.join("texts", files[file_choice])
        else:
            print("Invalid selection.")
            return None
    
    else:
        cleaned = file_choice.strip
        if not cleaned.lower().endswith(".txt"):
            cleaned = cleaned + ".txt"

        if file_choice in files: 
            return os.path.join("texts", file_choice)
        
        else:
            print("File not found. Please try again.")
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
            while filename is None:
                filename = getting_file_selection()
                print(f"Processing {filename}...")
                before = time.time()
                fp.run_processing_from_main(filename)
                data = stats.load_data()
                all_stats = run_all_analyses(data)
                print("File loaded successfully.")
                measured_time = time.time() - before
                print(f'The time it took to measure: {measured_time :.2f}')

        elif menu_choice == 2: # display basic statistics
            run_analysis(
                label= "Basic Statistics", 
                filename=filename, 
                data=data, 
                stat_key="basic", 
                display_func=stats.display_basic_statistics, 
                visual_func=visuals.basic_statistics_visuals
            )



        elif menu_choice == 3: # word frequency analysis
            run_analysis(
                label= "Word Analysis", 
                filename=filename, 
                data=data, 
                stat_key="word", 
                display_func=stats.display_word_analysis, 
                visual_func=visuals.word_analysis_visuals
            )


        elif menu_choice == 4:
            run_analysis(
                label= "Sentence Analysis", 
                filename=filename, 
                data=data, 
                stat_key="sentence", 
                display_func=stats.display_sentence_analysis, 
                visual_func=visuals.sentence_analysis_visuals
            )

        elif menu_choice == 5:
            run_analysis(
                label= "Character Analysis", 
                filename=filename, 
                data=data, 
                stat_key="character", 
                display_func=stats.display_character_analysis, 
                visual_func=visuals.character_analysis_visuals
            )


        elif menu_choice == 6:
            if 'filename' not in locals() or data is None:
                print("Please load a text file first (option 1).")
                input("Press Enter to return to the menu...")
                continue
            print(f"saving {filename}...")
            saving_stats(data, filename="results.txt")

        else: 
            break      #break the loop
            print (7)   # exit
        input("Press Enter to return to the menu...")

if __name__ == "__main__":
    main()