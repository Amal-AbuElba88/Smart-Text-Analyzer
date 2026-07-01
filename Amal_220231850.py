import string
import re 



class TrieNode:                       # O(1)
    def __init__(self):
        # Each node holds a dictionary of child nodes and a flag for end of word
        self.children = {}            # Dictionary of character children                  # O(1)
        self.is_end = False           # True if node marks end of a valid word            # O(1)


class Trie:
    def __init__(self):
        self.root = TrieNode()                        # O(1)

    def insert(self, word):                           # O(n), n = length of word
        # Insert a word into the trie
        node = self.root 
        for ch in word:                               # O(n)
            if ch not in node.children:               # O(1)
                node.children[ch] = TrieNode()        # O(1)
            node = node.children[ch]                  # Traverse to next node     # O(1)
        node.is_end = True                            # O(1)


    def search_prefix(self, prefix):                 # O(n)
        # Search for all words in the trie that start with the given prefix
        node = self.root                              
        for ch in prefix:                            # O(n)
            if ch in node.children:
                node = node.children[ch]

            else:
                return[]               # Prefix not found
                    
        return self._collect_words(node, prefix)
            
    def _collect_words(self, node, prefix):         # O(n)
        results = []
        # Helper recursive function to collect all words under a node
        if node.is_end:
            results.append(prefix)

        for ch, child in node.children.items():     # O(n)
            results.extend(self._collect_words(child, prefix + ch))

        return results
         





class SmartTextAnalyzer:
    def __init__(self):
        self.word_list = []                # List of all words extracted from the text       # O(1)
        self.sentence_list = []            # List of sentences extracted from the text       # O(1)
        self.text_data = ""                # Raw text data loaded or entered                 # O(1)
        self.history_stack = []
        self.trie = None



    def load_text(self):                   # O(n) where n = number of chars read from file or input

        while True:
            # Ask user to choose between file input or direct text input
            choice = input("Do you want to load text from a file (f) or enter it directly (d)? [f/d]: ").strip().lower()         # O(1)

            if choice == "f":
                while True:
                    file_path = input("Please enter the full path to your text file: ")            # O(1)

                    try:
                        # Read the entire content of the file
                        with open(file_path, "r", encoding="utf-8") as f:
                            self.text_data = f.read()       # O(n) to read file contents, n = file size in chars
                        return
                        
                    except FileNotFoundError:
                        print("File not found. Please try again or type 'cancel' to go back.")     # O(1)
                        if input().strip().lower() == "cancel":
                            break                            # Return to outer menu
    
    
                    
            elif choice == "d":
                print("Please enter your text. Type '$$END_TEXT$$' on a new line when you are finished: ")                      # O(1)
                lines = []
                # Read lines until user types the end signal
                while True:                                   # O(n) where n = number of lines user inputs
                    line = input()                            # O(1)
                    if line.strip() == "$$END_TEXT$$":        # O(1)
                        break
                    lines.append(line)                        # O(1) per append

                # Join all lines into a single string
                self.text_data = "\n".join(lines)             # O(n)  
                print("\nText loaded successfully.")
                return

            
            else:
                print("Invalid choice. Please try again.")    # O(1)





    def preprocess_text(self):                                # O(n)
        """Preprocess text: lowercase, remove punctuation and spaces, split into words and sentences"""
        
        if not self.text_data.strip():
            print("Error: No text to process!")
            return

        # Processes the raw text_data to extract normalized word and sentence lists
        self.text_data = self.text_data.lower()                          # O(n)

        # Remove unexpected punctuation, fix with .,!? to split sentences
        self.text_data = re.sub(r"[^\w\s.,!?]", "", self.text_data)

        # Divide the text into sentences while preserving the boundaries
        self.sentence_list = [s.strip() for s in re.split(r'[.!?,]', self.text_data) if s.strip()]  # O(n)

        # Extract words after removing punctuation
        self.word_list = re.findall(r'\w+', self.text_data)  # O(n)




    def display_menu(self):
        # Main interactive menu to let user choose different analysis options
        self.load_text()                 # O(n) for loading text
        self.preprocess_text()           # O(n) for preprocessing text  


        # Build a trie from unique words for fast prefix searching
        self.trie = Trie()
        unique_words = set(self.word_list)       # Remove duplicates using sets           # O(n)

        for word in unique_words:                                                         # O(n)
            self.trie.insert(word)               # Insert each unique word                # O(n)


        while True:

            print("\n\t***___________Smart Text Analyzer____________***")
            print("1. Smart Autocompletion / Predictive Typing.")
            print("2. Contextual Next Word Prediction.")
            print("3. Simple Sentiment Analysis (Sentence Level).")
            print("4. Keyword Extraction / Most Significant Terms.")
            print("5. Interactive Word Cloud Data Generation.")
            print("6. Word Statistics.")                   
            print("7. Character Statistics.")             
            print("8. Search for Word/Phrase.")          
            print("9. Replace a Word.") 
            print("10. Undo Last Change.")
            print("11. Load New Text.")
            print("12. Exit.")
            
            choice = input("Choose an option (1-12): ")



            if choice == "1":
                self.auto_complete(self.trie)

            elif choice == "2":
                self.next_word_prediction()

            elif choice == "3":
                self.simple_sentiment_analysis()

            elif choice == "4":
                self.extract_keywords()

            elif choice == "5":
                self.generate_word_cloud_data()

            elif choice == "6":
                self.word_statistics()

            elif choice == "7":
                self.character_statistics()

            elif choice == "8":
                self.search_word()

            elif choice == "9":
                self.replace_word()

            elif choice == "10":
                self.undo_last_change()

            elif choice == "11":
                self.load_text()
                self.preprocess_text()

                # re-built trie --- To ensure Trie is updated when new text is uploaded.
                self.trie = Trie()
                unique_words = set(self.word_list)

                for word in unique_words:
                    self.trie.insert(word)

            elif choice == "12":
                break

            else:
                print("Invalid choice. Please try again.")






    def _save_state(self):                                   # O(n)
        # save the current status of undo حفظ الحالة الحالية للتراجع
        self.history_stack.append({
            'word_list': self.word_list.copy(),              # O(n)
            'sentence_list': self.sentence_list.copy(),      # O(n)
            'text_data': self.text_data                      # O(1)
        })



    def replace_word(self):                                            # O(n) where n = number of words/sentences
        """Replace all occurrences of a word with another and update global lists"""

        if not self.word_list or not self.sentence_list:
            print("Error: No text loaded!")
            return
        

        self._save_state()
    
        old_word = input("Enter the word to replace: ").lower()          # O(1)
        new_word = input("Enter the new word: ").lower()                 # O(1)

        if not old_word or not new_word:
            print("Error: Invalid input!")
            return
        
        # Request confirmation  طلب التأكيد
        print(f"Are you sure you want to replace all occurrences of '{old_word}' with '{new_word}'? (y/n): ")
        if input().strip().lower() != 'y':                     # O(1)
            print("The replacement has been cancelled.")
            return
        

        # Calculate the number of substitutions
        count = 0
        new_word_list = []

        for word in self.word_list:                             # O(n)
            if word.lower() == old_word:                        # O(1)
                new_word_list.append(new_word)
                count += 1

            else:
                new_word_list.append(word)

        self.word_list = new_word_list                          # O(1)
        new_sentences = []


        for sentence in self.sentence_list:                     # O(n)
            words = sentence.lower().split()                    # O(n)
            new_words = [new_word if word.lower() == old_word else word for word in words]  # O(n)
            new_sentences.append(' '.join(new_words))           # O(n)


        self.sentence_list = new_sentences                      # O(1)
        self.text_data = '. '.join(self.sentence_list) + '.'    # O(n)

        if count == 0:
            print("No replacements made.")

        else:
            print(f"Replaced {count} occurrences of '{old_word}' with '{new_word}'.")


        # Rebuild Trie after replacement 
        self.trie = Trie()
        unique_words = set(self.word_list)

        for word in unique_words:                            # O(n)
            self.trie.insert(word)



    def undo_last_change(self):                             # O(1) for pop and assignment
        """Undo the last replacement by restoring the previous state."""

        if not self.history_stack:
            print("Nothing to undo")
            return
        

        last_state = self.history_stack.pop()                # O(1)
        self.word_list = last_state['word_list']             # O(1)
        self.sentence_list = last_state['sentence_list']     # O(1)
        self.text_data = last_state['text_data']             # O(1)

        # re-built trie --- To ensure Trie is updated 
        self.trie = Trie()
        unique_words = set(self.word_list)

        for word in unique_words:                            # O(n)
            self.trie.insert(word)

        print("Last change has been undone!")
        
 
    

    def auto_complete(self, trie):            # O(n^2) , worst-case with deep recursion
        
        print("\nSmart Autocompletion / Predictive Typing.")

        while True:
            prefix = input("Enter a prefix (or type 'exit' to go back): ").lower()

            if prefix == "exit":
                break

            suggestions = trie.search_prefix(prefix)       # O(n)

            if suggestions:
                print("Suggestions:", ", ".join(suggestions))

            else:
                print("No Suggestions Found.")





    def build_bigram_model(self, words):                        # O(n)
        # Build bigram frequency dictionary 
        bigrams = {}
        for i in range(len(words) - 1):                         # O(n)
            current_word = words[i]
            next_word = words[i + 1]

            if current_word not in bigrams:
                bigrams[current_word] = {}

            bigrams[current_word][next_word] = bigrams[current_word].get(next_word, 0) + 1

        return bigrams




    def next_word_prediction(self):                           # O(n log n)
        bigrams = self.build_bigram_model(self.word_list)           # O(n)
        print("\nContextual Next Word Prediction: ")

        while True:
            phrase = input("Enter a word or phrase (or type 'exit' to go back): ").strip().lower()

            if phrase == "exit":                          # O(1)
                break
            
            words = phrase.split()                        # O(n) split input

            if len(words) == 0:                           # O(1)
                print("Please enter at least one word.")
                continue

            last_word = words[-1]                         # O(1)
    
            if last_word in bigrams:                      # O(1)
                next_words = bigrams[last_word]           # O(1)

                # Sort next words by frequency descending
                sorted_words = sorted(next_words.items(), key= lambda x: x[1], reverse= True)          # O(nlogn)
                print("Most probable next words: ")
                for word, count in sorted_words[:5]:                 # Show the top 5 predictions      # O(1) (fixed 5 iterations)
                    print(f"-{word}\t occurrences: {count}")

            else:
                print("No Prediction Found for that word.")




            
            



    def simple_sentiment_analysis(self):                                                 # O(n)
        positive_words = {"good", "happy", "joy", "excellent", "fortunate", "great", "love", "like",
                        "wonderful", "amazing", "fun", "cool", "powerful", "enjoyable", "smart"}             # O(1)
        
        negative_words = {"bad", "sad", "pain", "terrible", "unfortunate", "hate", "angry", "dislike",
                        "awful", "horrible", "boring", "useless", "dumb", "slow"}                            # O(1)

        print("\nSentiment Analysis of Each Sentence:\n")

        positive_sentences = 0            # O(1)
        negative_sentences = 0            # O(1)
        neutral_sentences = 0             # O(1)

        print(f"{'Sentence':<50} | {'Sentiment':<10}")
        print("---------------------------------------------------------------------")

        for sentence in self.sentence_list:               # O(n)
            words = sentence.lower().split()              # O(n)

            positive_count = 0
            negative_count = 0
            i = 0


            # Iterate over words to count positive and negative sentiment with "not" negation handling
            while i < len(words):                        # O(n)
                word = words[i]                          # O(1)
                
                """if the word = not , and there is also a next word, then store the next word in the next_word variable,
                then the variable is checked, if in the positive word adds it to the negative_counter, because exist not, 
                as well as with the negative """
                
                if word == "not" and i + 1 < len(words): # O(1)
                    next_word = words[i + 1]
                    # Negate the sentiment of the next word if it is positive or negative
                    if next_word in positive_words:      # O(1)
                        negative_count += 1
                        i += 2                           # skip next word
                        continue

                    elif next_word in negative_words:    # O(1)
                        positive_count += 1
                        i += 2
                        continue

                # Regular sentiment counting
                if word in positive_words:               # O(1)
                    positive_count += 1

                elif word in negative_words:             # O(1)
                    negative_count += 1

                i += 1

    
            # Label the sentence sentiment based on counts
            if positive_count > negative_count:
                label = "Positive"
                positive_sentences += 1

            elif negative_count > positive_count:
                label = "Negative"
                negative_sentences += 1

            else:
                label = "Neutral"
                neutral_sentences += 1


            print(f"{sentence:<50} | {label:<10}")



        print("\nOverall Sentiment Summary:")
        print("----------------------------------")
        print(f"{'Positive Sentences:':<25} {positive_sentences}")
        print(f"{'Negative Sentences:':<25} {negative_sentences}")
        print(f"{'Neutral Sentences:':<25} {neutral_sentences}")

        if positive_sentences > negative_sentences:
            general = "Positive"

        elif negative_sentences > positive_sentences:
            general = "Negative"
            
        else:
            general = "Neutral"

        print(f"{'General Sentiment:':<25} {general}.")





    def extract_keywords(self):                        # O(n log n) total
        # define stop words using a set
        stop_words = {
            "the", "is", "and", "a", "an", "in", "on", "at", "of", "to", "it", "this", "that",
            "was", "for", "with", "as", "by", "from", "but", "be", "or", "not", "are", "am", "were"
        }

        # Filter out stop words
        filtered_words = [word for word in self.word_list if word not in stop_words]        # O(n)


        # Count frequency using a dictionary
        freq_dict = {}                                                                 # O(1)
        for word in filtered_words:                                                    # O(n)
            freq_dict[word] = freq_dict.get(word, 0) + 1                               # O(1) per insertion


        # Sort the dictionary by frequency descending
        sorted_keywords = sorted(freq_dict.items(), key= lambda x: x[1], reverse= True)        # O(n log n) 


        # Ask the user how many top keywords to display
        try:
            top_n = int(input("How many top keywords would you like to display? (default is 10): ")or 10)      # O(1)

        except ValueError:
            top_n = 10                   # O(1)
    

        # Display the keywords in a formatted table
        print("\n Keyword Extraction - Top Significant Terms\n")
        print(f"{'Keyword':<20} Frequency")
        print("----------------------------------------------")
        for word, freq in sorted_keywords[:top_n]:               # O(1) (top_n is constant)
            print(f"{word:<20} | {freq}")








    def generate_word_cloud_data(self):                            # O(n log n) total
        # Generate word cloud data: frequencies of words excluding stopwords
        stop_words = {
            "the", "is", "and", "a", "an", "in", "on", "at", "of", "to", "it", "this", "that",
            "was", "for", "with", "as", "by", "from", "but", "be", "or", "not", "are", "am", "were"
        }

        cleaned_words = [word.strip(string.punctuation) for word in self.word_list]                    # O(n)
        filtered_words = [word for word in cleaned_words if word and word not in stop_words]      # O(n)

        freq_dict = {}                                              # O(1)
        for word in filtered_words:                                 # O(n)
            freq_dict[word] = freq_dict.get(word, 0) + 1            # O(1)

        if not freq_dict:
            print("No Valid Words Found.")
            return
        
        max_freq = max(freq_dict.values())                          # O(n)
        word_cloud_data = [(word, round(freq / max_freq, 3)) for word, freq in freq_dict.items()]    # O(n)

        print("\nWord Cloud Data(Normalized Frequencies, max = 1.0): ")
        print(f"{'word':<15} | {'Normalized Freq'}")
        print("----------------------------------------------")

        for word, norm_freq in sorted(word_cloud_data, key= lambda x: -x[1]):                        # O(n log n)
            print(f"{word:<15} | {norm_freq}") 





    def word_statistics(self):
        """Calculate total words, unique words, and top N frequent words"""

        if not self.word_list:
            print("Error: No text loaded!")
            return
        
        print("\nWord Statistics: ")
        total_words = len(self.word_list)                            # O(1)
        unique_words = set(self.word_list)                           # O(n)
        print(f"Total Number of Words: {total_words}")
        print(f"Number of unique words: {len(unique_words)}")

        # Count word frequencies
        freq = {}
        for word in self.word_list:                                  # O(n)
            freq[word] = freq.get(word, 0) + 1

        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)  # O(n log n)

        # Show top N frequent words
        try:
            top_n = int(input("How many top frequent words to display? (default 10): ") or 10)
        except ValueError:
            top_n = 10

        # Display result
        print(f"\n{'Word':<15} | Frequency")
        print("----------------------------------------------")
        for word, count in sorted_words[:top_n]:                # O(n)
            print(f"{word:<15} | {count}")






    def character_statistics(self):
        """Count the total number of characters (excluding spaces) and the frequency of each character"""

        if not self.text_data:
            print("Error: No text loaded!")
            return
        
        # Calculate the total number of characters excluding spaces
        total_chars = sum(1 for char in self.text_data if char not in ' \n')  # O(n)

        # Character frequency count (letters and numbers only)
        freq = {}
        for char in self.text_data.lower():                                   # O(n)
            if char.isalnum():                                                # O(1)
                freq[char] = freq.get(char, 0) + 1                            # O(1)



        print("\nCharacter Statistics: ")
        print(f"Total characters (excluding spaces):<30 | {total_chars}")

        print("\nCharacter repetitions: ")
        print(f"\n{'Character':<10} | Frequency")
        print("----------------------------------------------")
        for char, count in sorted(freq.items()):                             # O(n log n)
            print(f"{char:<10} | {count}")







    def search_word(self):
        """Search for a word or phrase and return its occurrences with positions"""

        if not self.sentence_list:
            print("Error: No text loaded!")
            return
        
        query = input("Enter word or phrase to search: ").lower()

        if not query:
            print("Error: Empty search query!")
            return
        
        query_words = query.split()                                     # O(n)
        occurrences = []
        # Total O(n^2) ---- Nested loop
        for sent_index, sentence in enumerate(self.sentence_list, 1):    # O(n)
            words = sentence.lower().split()                       
            for i in range(len(words) - len(query_words) + 1):           # O(n)

                # search for multi-word phrases
                if words[i:i+len(query_words)] == query_words:    
                    occurrences.append((sent_index, i+1))                # O(1)


        if occurrences:
            print(f"\nFound {len(occurrences)} occurrences of '{query}':")
            print(f"{'Sentence Number':<12} | {'Word Position':<15}")
            print("----------------------------------------------")

            for sent_index, word_pos in occurrences:                     # O(n)
                print(f"{sent_index:<12} | {word_pos:<15}")

        else:
            print(f"No duplicates found for '{query}'.")


   



smart_text_analyzer = SmartTextAnalyzer()
smart_text_analyzer.display_menu()





"""
def auto_correct():
    from collections import Counter
    word_freq = Counter(word_list)
    vocabulary = set(word_freq.keys())
    bigrams = build_bigram_model(word_list)

    context = input("Enter the previous word (optional, press Enter to skip): ").strip().lower()
    word = input("Enter the word to check: ").strip().lower()

    if word in vocabulary:
        print(f"'{word}' is spelled correctly.")
        return
    
    candidates = generate_candidates(word, vocabulary)

    if not candidates:
        print("No Suggestions Found.")
        return 
    
    if context and context in bigrams:
        ranked = sorted(candidates, key= lambda w: bigrams[context].get(w, 0), reverse= True)

    else:
        freq = {w: word_list.count(w) for w in candidates}
        ranked = sorted(candidates, key= lambda w: freq[w], reverse= True)

    print("Did You Mean: ")
    for i, w in enumerate(ranked[:5], 1):
        print(f"{i}. {w}")




    def edits1(self, word):                                               # O(n²) (n = len(word))
        # Generate all strings one edit away from 'word' (deletion, transposition, replacement, insertion)
        letters = string.ascii_lowercase
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]                # O(n)

        deletes = [L + R[1:] for L, R in splits if R]                                # O(n)
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]      # O(n)
        replaces = [L + C + R[1:] for L, R in splits if R for C in letters]          # O(n^2)
        inserts = [L + C + R for L, R in splits for C in letters]                    # O(n^2)

        return set(deletes + transposes + replaces + inserts)                        # O(n^2)

    def generate_candidates(self, word, vocabulary):                                       # O(n^2)
        # Generate candidate corrections within 1 or 2 edits that exist in the vocabulary
        candidates1 = self.edits1(word)                                                   # O(n^2)
        candidates2 = set(e2 for e1 in candidates1 for e2 in self.edits1(e1))             # O(n^4)
        known_candidates1 = set(w for w in candidates1 if w in vocabulary)           # O(n^2)
        known_candidates2 = set(w for w in candidates2 if w in vocabulary)           # O(n^4)

        return known_candidates1 or known_candidates2                                # O(1)



"""
