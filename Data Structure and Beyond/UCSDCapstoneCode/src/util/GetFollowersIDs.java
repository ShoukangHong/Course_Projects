package util;
import twitter4j.IDs;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.User;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.List;
import twitter4j.PagableResponseList;

public final class GetFollowersIDs {

    public static void main(String[] args) {
        String text = new String();
        try {
            Twitter twitter = new TwitterFactory().getInstance();
            long cursor = -1;
            PagableResponseList<User> users;
            do {
                users = twitter.getFriendsList(1157916092490272768L, cursor);
                for (User user : users) {
                    text += user.getId() + "\t" + user.getName() + '\n';
                }
            } while ((cursor = users.getNextCursor())!= 0);
        } catch (TwitterException te) {
            te.printStackTrace();
            System.out.println("Failed to get followers' ids: " + te.getMessage());
        }
        try {
            PrintWriter writer = new PrintWriter("filename.txt");
            System.out.println("test File starts here");
            System.out.println(text);
            writer.println(text);
            writer.close();
        } catch (FileNotFoundException e){
            System.out.println("failed to save file");
        }
    }
}

//    public static void main(String[] args) {
//        String text = new String();
//        try {
//            Twitter twitter = new TwitterFactory().getInstance();
//            long cursor = -1;
//            IDs ids;
//            System.out.println("Listing followers's ids.");
//            do {
//                ids = twitter.getFriendsIDs(cursor);
//                for (long id : ids.getIDs()) {
//                    User user = twitter.showUser(id);
//                    text += id + " " + user.getName() + '\n';
//                }
//            } while ((cursor = ids.getNextCursor()) != 0);
//        } catch (TwitterException te) {
//            te.printStackTrace();
//            System.out.println("Failed to get followers' ids: " + te.getMessage());
//        }
//        try {
//            PrintWriter writer = new PrintWriter("filename.txt");
//            System.out.println("test File starts here");
//            System.out.println(text);
//            writer.println(text);
//            writer.close();
//        } catch (FileNotFoundException e){
//            System.out.println("failed to save file");
//        }
//    }
