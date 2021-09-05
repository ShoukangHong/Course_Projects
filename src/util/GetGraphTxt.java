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

/**
 * Lists followers' ids
 *
 * @author Yusuke Yamamoto - yusuke at mac.com
 */
public final class GetGraphTxt {
    /**
     * Usage: java twitter4j.examples.friendsandfollowers.GetFollowersIDs [screen name]
     *
     * @param args message
     */

    public static void main(String[] args) {
        TwitterFriendInfo info = new TwitterFriendInfo("friendList-small.txt");
        TwitterFriendInfo all = new TwitterFriendInfo("friendList.txt");
        System.out.println(info.getIdList());
        String text = new String();
        try {
            Twitter twitter = new TwitterFactory().getInstance();
            IDs ids;
            for (long friendId: info.getIdList()){
                long cursor = -1;
                do {
                    ids = twitter.getFriendsIDs(friendId, cursor);
                    for (Long id : ids.getIDs()) {
                        if (all.hasId(id)){
                            text += friendId + " " + id + "\n";
                        }
                    }
                    Thread.sleep(3000);
                    System.out.println("current Cursor: " + cursor + "\tcurrentId" + friendId);
                } while ((cursor = ids.getNextCursor())!= 0);
            }
        } catch (TwitterException | InterruptedException te) {
            te.printStackTrace();
            System.out.println("Failed to get followers' ids: " + te.getMessage());
        }
        outPutToFile(text, "twitterGraphFinal.txt");
    }

    public static void outPutToFile(String text, String file){
        try {
            PrintWriter writer = new PrintWriter(file);
            System.out.println("test File starts here");
            System.out.println(text);
            writer.println(text);
            writer.close();
        } catch (FileNotFoundException e){
            System.out.println("failed to save file");
        }
    }
}
