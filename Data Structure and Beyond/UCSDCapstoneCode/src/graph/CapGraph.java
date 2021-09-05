/**
 * 
 */
package graph;

import util.GraphLoader;
import util.TwitterFriendInfo;
import util.TwitterGraphLoader;

import javax.xml.soap.Node;
import java.net.Inet4Address;
import java.util.*;

/**
 * @author shoukang.
 * 
 * For the warm up assignment, you must implement your Graph in a class
 * named CapGraph.  Here is the stub file.
 *
 */

/**
 * Data structure for edges
 */
class Edges {
	/**
	 * store all to vertexes
	 */
	public HashSet<Integer> edges;
	/**
	 * used to count betweenness.
	 */
	public HashMap<Integer,Double> count;
	public Edges(){
		edges = new HashSet <Integer>();
		count = new HashMap<>();
	}
	public void initCount(){
		for (int idx: edges){
			count.put(idx, 0.0);
		}
	}
	public void addCount(int idx, Double val){
		double prev = count.get(idx);
		count.put(idx, prev + val);
	}
	public double getCount(int idx){
		return count.get(idx);
	}
	public void add(int num){ edges.add(num); }
	public void  remove(int num) {edges.remove(num);}
	public HashSet<Integer> getEdges(){ return edges;}
	public void printCount(int idFrom){
		String text = "From " + idFrom + " to:";
		for (int idTo: edges){
			text += "\t" + idTo + "-" + getCount(idTo);
		}
		System.out.println(text);
	}
}

public class CapGraph implements Graph {
	private HashMap<Integer, Edges> graph;

	public CapGraph(){
		graph = new HashMap<Integer, Edges>();
	}

	public void removeEdge(int from, int to) {
		// TODO Auto-generated method stub
		graph.get(from).remove(to);
	}

	/** remove the edge with the largest betweenness in this graph, not used*/
	public void removeMostVisitedEdge(){
		double maxCount = -1;
		initAllCount();
		countAllEdges();
		for (int from: getAllVertex()){
			Edges edges = graph.get(from);
			for (int to: edges.getEdges()){
				if (edges.getCount(to) > maxCount){
					maxCount = edges.getCount(to);
				}
			}
		}
		for (int from: getAllVertex()){
			HashSet<Integer> edges = new HashSet<>(getNeighbours(from));
			for (int to: edges){
				if (getCount(from, to) >= maxCount){
					removeEdge(from, to);
					System.out.println("removed Edge:" + from + "\t" + to + ", count" + maxCount);
				}
			}
		}
	}

	/** calculate betweenness of each sub graph in scc, and remove the edge with the largest betweenness*/
	public void removeMostVisitedEdge(List<CapGraph> scc){
		double maxCount = -1;

		for (CapGraph g: scc){
			g.initAllCount();
			g.countAllEdges();
			for (int from: g.getAllVertex()){
				HashSet<Integer> edges = g.getNeighbours(from);
				for (int to: edges){
					if (g.getCount(from, to) > maxCount){
						maxCount = g.getCount(from, to);
					}
				}
			}
		}
		for (CapGraph g: scc){
			for (int from: g.getAllVertex()){
				HashSet<Integer> edges = new HashSet<>(g.getNeighbours(from));
				for (int to: edges){
					if (g.getCount(from, to) >= maxCount){
						removeEdge(from, to);
						System.out.println("removed Edge:" + from + "\t" + to + ", count" + maxCount);
					}
				}
			}
		}
	}

	public void initAllCount() {
		// TODO Auto-generated method stub
		for (int idx:getAllVertex()){
			graph.get(idx).initCount();;
		}
	}

	public void countAllEdges(){
		initAllCount();
		for (int idx:getAllVertex()){
			bfsCount(idx);
		}
	}

	public void bfsCount(int center){
		LinkedList<Integer> queue =  new LinkedList<>();
		HashMap<Integer, HashSet<Integer>> prevNode = new HashMap<>(); // store node and prev node
		HashMap<Integer, Double> score = new HashMap<>();
		HashMap<Integer, Double> outFlow = new HashMap<>();
		Stack<Integer> visited = new Stack<>();
		queue.add(center);
		visited.add(center);
		for (int idx:getAllVertex()){
			score.put(idx, 0.0);
			outFlow.put(idx, 0.0);
			prevNode.put(idx, new HashSet<>());
		}
		score.put(center, 1.0);
		while (queue.size() > 0){
			LinkedList<Integer> tmp =  new LinkedList<>();
			for (int from: queue){
				for (int to :getNeighbours(from)){
					if (!visited.contains(to)) {
						tmp.add(to);
						prevNode.get(to).add(from);
						score.put(to, score.get(to) + score.get(from));
					}
				}
			}
			queue =  new LinkedList<>();
			for ( int idx: tmp){
				if (!visited.contains(idx)){
					visited.push(idx);
					queue.add(idx);
				}
			}
		}
		//for (int val: score.keySet()){
			//System.out.println("key: " + val + " score: " + score.get(val));
			//System.out.println("prev:" + prevNode.get(val));
		//}
		//System.out.println(visited);
		while (visited.size() > 0){
			int to = visited.pop();
			//System.out.println(to);
			for (int from: prevNode.get(to)){
				double val = score.get(from) *(1 + outFlow.get(to)) / score.get(to);
				//System.out.println(from + " "+ val);
				outFlow.put(from, outFlow.get(from) + val);
				addCount(from, to, val);
			}
		}
		//printAllCount();
	}

	public void addCount(int from, int to, double val){
		graph.get(from).addCount(to, val);
	}

	public double getCount(int from, int to){
		return graph.get(from).getCount(to);
	}

	@Override
	public void addVertex(int num) {
		// TODO Auto-generated method stub
		graph.put(num, new Edges());
	}

	@Override
	public void addEdge(int from, int to) {
		// TODO Auto-generated method stub
		graph.get(from).add(to);
	}

	private HashSet<Integer> getNeighbours(int center) {
		return graph.get(center).getEdges();
	}

	public boolean hasVertex(int num){ return graph.containsKey(num);}

	public HashSet<Integer> getAllVertex(){
		return new HashSet(graph.keySet());
	}

	public int size(){return getAllVertex().size();}

	@Override
	public Graph getEgonet(int center) {
		// TODO Auto-generated method stub
		CapGraph egoNet = new CapGraph();
		egoNet.addVertex(center);
		for (int num: getNeighbours(center)){
			egoNet.addVertex(num);
		}
		for (int from: egoNet.getAllVertex()){
			for (int to: getNeighbours(from)){
				if (egoNet.hasVertex(to)){
					egoNet.addEdge(from, to);
				}
			}
		}
		return egoNet;
	}

	@Override
	public List<Graph> getSCCs() {
		// TODO Auto-generated method stub
		return new ArrayList<>(getCapSCC());
	}

	/** used to create SCC with CapGraph data structure. Otherwise it's hard to convert Garph to CapGraph some times*/
	public  List<CapGraph> getCapSCC(){
		List<CapGraph> ans = new ArrayList<>();
		HashSet<Integer> visited= new HashSet<>();
		ArrayList<Integer> finished = new ArrayList<>();
		CapGraph reverse = getReversedGraph();
		for (int num: getAllVertex()){
			if (!visited.contains(num)) {
				dfsVisit(this, num, visited, finished);
			}
		}
		visited= new HashSet<>();
		while (finished.size() > 0){
			int num = finished.remove(finished.size() - 1);
			if (!visited.contains(num)) {
				ArrayList<Integer> component = new ArrayList<>();
				dfsVisit(reverse, num, visited, component);
				ans.add(buildSubGraph(component));
			}
		}

		return ans;
	}

	/** build a subgraph given certain vertexes, used for SCC */
	public CapGraph buildSubGraph(List<Integer> comp){
		CapGraph g = new CapGraph();
		for (int num: comp){
			g.addVertex(num);
		}
		for (int from: comp){
			for (int to: getNeighbours(from)){
				if (g.hasVertex(to)){
					g.addEdge(from, to);
				}
			}
		}
		return g;
	}

	/** used for SCC */
	public void dfsVisit(CapGraph g, int n, HashSet<Integer> visited, ArrayList<Integer> finished){
		visited.add(n);
		for (int neigh: g.getNeighbours(n)){
			if (!visited.contains(neigh)){
				dfsVisit(g, neigh, visited, finished);
			}
		}
		finished.add(n);
	}

	/** used for SCC */
	public  CapGraph getReversedGraph(){
		CapGraph rGraph = new CapGraph();
		for (int num: getAllVertex()){
			rGraph.addVertex(num);
		}
		for (int to: getAllVertex()){
			for (int from: getNeighbours(to)){
				rGraph.addEdge(from, to);
			}
		}
		return rGraph;
	}

	@Override
	public HashMap<Integer, HashSet<Integer>> exportGraph() {
		// TODO Auto-generated method stub
		HashMap<Integer, HashSet<Integer>> result = new HashMap<>();
		for (int num: graph.keySet()) {
			result.put(num, graph.get(num).getEdges());
		}
		return result;
	}

	public void print(){
		for ( int num : getAllVertex()){
			System.out.println(num +":"+ getNeighbours(num));
		}
		System.out.println();
	}

	/** given my twitter info, and the group number, print out the user name of vertexes */
	public void printName(TwitterFriendInfo info, int count){
		String names = "Group" + count + ":\t";
		for (int  idx: getAllVertex()){
			names += idx + "-" +info.getUserName(idx) + ", ";
		};
		System.out.println(names);
	}

	/** print out the betweeness of all edges */
	public void printAllCount() {
		// TODO Auto-generated method stub
		for (int idx:getAllVertex()){
			graph.get(idx).printCount(idx);;
		}
	}

	/** run this to get my twitter communities */

	public void getCommunity(int number, TwitterFriendInfo info) {
		// load the graph
		int count = 0;

		//print out all the vertexes and edges, just used to take a look
		for (int  idx: getAllVertex()){
			String names = count + "-" + info.getUserName(idx) + ":";
			HashSet<Integer> edges= (HashSet<Integer>) getNeighbours(idx);
			for (int idy:edges){
				names += "\t" + info.getUserName(idy);
			};
			count += 1;
			System.out.println(names);
		};

		// main logic starts here
		count = 0;
		List<CapGraph> scc = getCapSCC();
		// while it doesn't reach the size we want, here I set the size to 33.
		while (scc.size()<number){
			//calculate betweenness of each sub graph in scc, and remove the edge with the largest betweenness
			removeMostVisitedEdge(scc);
			scc = getCapSCC();
		}
		//print out the result
		for(CapGraph cg:scc){
			if (cg.size() > 1){
				count += 1;
				cg.printName(info, count);
				cg.countAllEdges();
				cg.printAllCount();
			}
		}
	}

	public static void main(String[] args) {
		TwitterFriendInfo info = new TwitterFriendInfo("data/twitterFriendList.txt");
		CapGraph g = new CapGraph();
		GraphLoader.loadGraph(g, "data/scc/test_mine2.txt");
		g.initAllCount();
		g.bfsCount(2);
		int count = 0;
		List<CapGraph> scc = g.getCapSCC();

		//print out the count result
		for(CapGraph cg:scc){
			if (cg.size() > 1){
				count += 1;
				cg.printName(info, count);
				cg.countAllEdges();
				cg.printAllCount();
			}
		}

		CapGraph myTwitter = new CapGraph();
		TwitterGraphLoader.loadDirectedGraph(myTwitter, "data/twitterGraphData.txt", info);
		myTwitter.getCommunity(30, info);
	}
};