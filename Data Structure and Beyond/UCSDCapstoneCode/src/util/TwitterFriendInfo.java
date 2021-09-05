package util;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.HashMap;
import java.util.List;

public class TwitterFriendInfo {
    private HashMap<Long, Integer> idMap;
    private List<Long> idList;
    private List<String> nameList;
    public static void main(String[] args)
    {
        String filePath = "friendList.txt";
        TwitterFriendInfo info = new TwitterFriendInfo(filePath);
        System.out.println(info.hasId(984633810951139328L) + "\t answer is true");
        System.out.println(info.hasId(9846338109511393L) + "\t answer is false");
        System.out.println((info.getUserId(0) == 153746050L) + "\t answer is true");
        System.out.println((info.getUserId(3) == 984633810951139328L) + "\t answer is true");
        System.out.println(info.getUserName(1273704482L) + "\t answer is 神楽坂真冬");
        System.out.println(info.getUserName(864400939125415936L));
        System.out.println(info.getUserName(2585157547L));
        System.out.println(info.getUserName(1482780949L));
        System.out.println(info.getUserName(11) + "\t answer is Chin_");
        System.out.println(info.getIdList() + "\t answer is a List of Id");
    }

    public TwitterFriendInfo() {
        idMap = new HashMap<>();
        idList = new ArrayList<>();
        nameList = new ArrayList<>();
    }

    public TwitterFriendInfo(String filePath) {
        idMap = new HashMap<>();
        idList = new ArrayList<>();
        nameList = new ArrayList<>();
        getInfoFromFile(filePath);
    }

    public void getInfoFromFile(String filePath)
    {
        String  text = read(filePath);
        String[] parts = text.split("\n|\t");
        for (int count = 0; count < parts.length - 1; count+= 2){
            idMap.put(Long.parseLong(parts[count]), count/2);
            idList.add(Long.parseLong(parts[count]));
            nameList.add(parts[count + 1]);
//            System.out.println(parts[count]);
//            System.out.println(parts[count + 1]);
        }
//        System.out.println(idMap);
//        System.out.println(idList);
//        System.out.println(nameList);
    }
    //Read file content into string with - Files.readAllBytes(Path path)

    public static String read(String filePath)
    {
        String content = "";
        try
        {
            content = new String ( Files.readAllBytes( Paths.get(filePath) ) );
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

        return content;
    }

    public boolean hasId(long id){
        return idMap.containsKey(id);
    }

    public long getUserId(int idx){
        return idList.get(idx);
    }
    public int getUserIdx(long id){
        return idMap.get(id);
    }
    public String getUserName(long id){
        return nameList.get(getUserIdx(id));
    }

    public String getUserName(int idx){
        return nameList.get(idx);
    }

    public List<Long> getIdList(){
        return idList;
    }
}
