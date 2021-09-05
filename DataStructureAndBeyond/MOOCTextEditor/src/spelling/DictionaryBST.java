package spelling;

import sun.reflect.generics.tree.Tree;

import java.util.Locale;
import java.util.TreeSet;

/**
 * @author UC San Diego Intermediate MOOC team
 *
 */
public class DictionaryBST implements Dictionary 
{
    private TreeSet<String> words;
	
    // TODO: Implement the dictionary interface using a TreeSet.  
 	// You'll need a constructor here
    public DictionaryBST(){
        words = new TreeSet();
    }

    /** Add this word to the dictionary.  Convert it to lowercase first
     * for the assignment requirements.
     * @param word The word to add
     * @return true if the word was added to the dictionary 
     * (it wasn't already there). */
    public boolean addWord(String word) {
    	// TODO: Implement this method
        return words.add(word.toLowerCase());
    }


    /** Return the number of words in the dictionary */
    public int size()
    {
    	// TODO: Implement this method
        return words.size();
    }

    /** Is this a word according to this dictionary? */
    public boolean isWord(String s) {
    	//TODO: Implement this method
        return words.contains(s.toLowerCase()); //dict.contains(s.toLowerCase());
    }

}
