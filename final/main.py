import os
import time
import stats_functions as stats
import visuals
import exporting_data as ed
import file_processing as fp

# --- Run all analyses and store results ---
def get_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid integer.")
        return None

def run_all_analyses(data):
    all_stats = {
        "basic": stats.basic_statistics(data),
        "word": stats.word_analysis(data),
        "sentence": stats.sentence_analysis(data),
        "character": stats.character_analysis(data),
        "lix": stats.LIX(data)
    }
    return all_stats


def run_analysis(label, filename, data, stat_key, display_func, visual_func, all_stats, foldername):
    print(f"------{label}-------")

    if filename is None or data is None:
        print("please load a text file first (option 1). ")
        input ("press Enter to reutrn to the menu...")
        return
    
    print(F"processing {filename} ...")
    display_func(all_stats[stat_key])
    
    print("Visuals? (y/n)")

    choice = input("Enter your choice: ").strip().lower()

    # strict yes/no handling
    if choice == 'y':
        visual_func(data, foldername)
    elif choice == 'n':
        return
    else:
        print("Invalid choice. Returning to menu...")

def check_script_directory():
    # Actual folder where main.py lives
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Folder user is running from
    cwd = os.getcwd()

    if os.path.normpath(cwd) != os.path.normpath(script_dir):
        print(f"""\n 
                                OOOOoooopsies
        You are running the program from the WRONG directory.
         - Current working directory: {cwd}
         - main.py location:         {script_dir}\n
        Fix: Navigate to the folder where main.py is located before running it.
                Example:
                cd \"{script_dir}\"
                        Then run""")

        return False

    return True

#========================================================================================================================
# INPUT HANDELING
#========================================================================================================================

def getting_file_selection():
    
    print("Available text files:")
    files = [f for f in os.listdir("texts") if f.endswith(".txt")]
    i = 1
    for file in files:
        print(f"{i}. {file}")
        i += 1

    file_choice = input("Enter your choice: ")

    if file_choice.isdigit(): 
        file_choice = int(file_choice) - 1
        if 0 <= file_choice < len(files):
            if os.path.exists("processed_data.json"):
                os.remove("processed_data.json")
            return os.path.join("texts", files[file_choice])
        else:
            print("Invalid selection.")
            return None
    
    else:
        cleaned = file_choice.strip()
        if not cleaned.lower().endswith(".txt"):
            cleaned = cleaned + ".txt"

        if cleaned in files: 
            if os.path.exists("processed_data.json"):
                os.remove("processed_data.json")
            return os.path.join("texts", cleaned)
        
        else:
            print(""" 
                  ---------------------------------
                  File not found. Please try again.
                  ----------------------------------
                  
                  """)
            return None

#========================================================================================================================
# Menu
#========================================================================================================================

def main():
    if not check_script_directory():
        return
    data = None
    filename = None
    all_stats= None
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
            data = None
            filename = None
            all_stats= None
            while filename is None:
                filename = getting_file_selection()
            print(f"""
                  ------------------------------------------------------
                   Processing {filename}...
                  ------------------------------------------------------
                  """)
            before = time.time()
            data = fp.run_processing_from_main(filename)

            all_stats = run_all_analyses(data)

            foldername = ed.create_export_folder(filename)

            print("""
                  ==================================================
                             File loaded successfully.""")
            measured_time = time.time() - before
            print(f"""
                          The time it took to measure: {measured_time :.2f}
                  =================================================
                    """)


        elif menu_choice == 2: # display basic statistics
            run_analysis(
                label= "Basic Statistics", 
                filename=filename, 
                data=data, 
                stat_key="basic", 
                display_func=stats.display_basic_statistics, 
                visual_func=visuals.basic_statistics_visuals, 
                all_stats=all_stats,
                foldername=foldername
            )
            stats.display_lix(all_stats["lix"])


        elif menu_choice == 3: # word frequency analysis
            run_analysis(
                label= "Word Analysis", 
                filename=filename, 
                data=data, 
                stat_key="word", 
                display_func=stats.display_word_analysis, 
                visual_func=visuals.word_analysis_visuals,
                all_stats=all_stats,
                foldername=foldername
            )


        elif menu_choice == 4:
            run_analysis(
                label= "Sentence Analysis", 
                filename=filename, 
                data=data, 
                stat_key="sentence", 
                display_func=stats.display_sentence_analysis, 
                visual_func=visuals.sentence_analysis_visuals,
                all_stats=all_stats,
                foldername=foldername
            )

        elif menu_choice == 5:
            run_analysis(
                label= "Character Analysis", 
                filename=filename, 
                data=data, 
                stat_key="character", 
                display_func=stats.display_character_analysis, 
                visual_func=visuals.character_analysis_visuals,
                all_stats=all_stats,
                foldername=foldername
            )


        elif menu_choice == 6:
            if data is None:
                print("Please load a text file first (option 1).")
                input("Press Enter to return to the menu...")
                continue

            print("Saving results...")
            visuals.basic_statistics_visuals(data, foldername)
            visuals.word_analysis_visuals(data, foldername)
            visuals.sentence_analysis_visuals(data, foldername)
            visuals.character_analysis_visuals(data, foldername)
            ed.export_results(all_stats, foldername)


        else: 
            break      #break the loop
            print (7)   # exit
        input("Press Enter to return to the menu...")

if __name__ == "__main__":
    main()