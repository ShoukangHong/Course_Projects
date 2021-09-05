/**
 * @author UCSD MOOC development team
 *
 * Utility class to add vertices and edges to a graph
 *
 */
package util;
import java.io.File;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class TwitterGraphLoader {
    /**
     * Loads graph with data from a file.
     * The file should consist of lines with 2 integers each, corresponding
     * to a "from" vertex and a "to" vertex.
     */
    public static void loadDirectedGraph(graph.Graph g, String filename, TwitterFriendInfo info) {
        Set<Integer> seen = new HashSet<Integer>();
        Scanner sc;
        try {
            sc = new Scanner(new File(filename));
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }
        for (Long id: info.getIdList()){
            int idx = info.getUserIdx(id);
            g.addVertex(idx);
        }
        // Iterate over the lines in the file, adding new
        // vertices as they are found and connecting them with edges.
        int count = 0;
        while (sc.hasNextLong()) {
            count += 1;
            int v1 = info.getUserIdx(sc.nextLong()) ;
            int v2 = info.getUserIdx(sc.nextLong());
            if (!seen.contains(v1)) {
                g.addVertex(v1);
                seen.add(v1);
            }
            if (!seen.contains(v2)) {
                g.addVertex(v2);
                seen.add(v2);
            }
            g.addEdge(v1, v2);
        }
        System.out.println("loaded total " + count +"edges");

        sc.close();
    }

//    public static void loadUndirectedGraph(graph.Graph g, String filename, TwitterFriendInfo info) {
//        Set<Integer> seen = new HashSet<Integer>();
//        Scanner sc;
//        try {
//            sc = new Scanner(new File(filename));
//        } catch (Exception e) {
//            e.printStackTrace();
//            return;
//        }
//        for (Long id: info.getIdList()){
//            int idx = info.getUserIdx(id);
//            g.addVertex(idx);
//        }
//        // Iterate over the lines in the file, adding new
//        // vertices as they are found and connecting them with edges.
//        while (sc.hasNextLong()) {
//            int v1 = info.getUserIdx(sc.nextLong()) ;
//            int v2 = info.getUserIdx(sc.nextLong());
//            if (!seen.contains(v1)) {
//                g.addVertex(v1);
//                seen.add(v1);
//            }
//            if (!seen.contains(v2)) {
//                g.addVertex(v2);
//                seen.add(v2);
//            }
//            g.addEdge(v1, v2);
//            g.addEdge(v2, v1);
//        }
//
//        sc.close();
//    }
}

