/**
 * @author UCSD MOOC development team and YOU
 * 
 * A class which reprsents a graph of geographic locations
 * Nodes in the graph are intersections between 
 *
 */
package roadgraph;


import java.util.*;
import java.util.function.Consumer;

import geography.GeographicPoint;
import util.GraphLoader;

/**
 * @author UCSD MOOC development team and YOU
 * 
 * A class which represents a graph of geographic locations
 * Nodes in the graph are intersections between 
 *
 */
class EdgeInfo {
	public String roadName;
	public String roadType;
	public double length;
	public EdgeInfo(String roadName, String roadType, double length){
		this.roadName = roadName;
		this.roadType = roadType;
		this.length = length;
	}
}

class PriorityNode implements Comparable{
	public GeographicPoint node;
	public double priority;
	public PriorityNode(GeographicPoint node, double priority){
		this.node = node;
		this.priority = priority;
	}

	public void setPriority(double val) { priority = val;}

	public GeographicPoint getNode(){return node;}

	public double getPriority() {
		return priority;
	}

	@Override
	public int compareTo(Object node2) {
		PriorityNode node = (PriorityNode) node2;
		return (int) (this.priority * 1000 - node.getPriority() * 1000);
	}
}

public class MapGraph {
	//TODO: Add your member variables here in WEEK 3
	private HashMap<GeographicPoint, HashMap<GeographicPoint, EdgeInfo>> nodes;
	/**
	 * Create a new empty MapGraph 
	 */
	public MapGraph()
	{
		// TODO: Implement in this constructor in WEEK 3
		nodes = new HashMap<GeographicPoint, HashMap<GeographicPoint, EdgeInfo>>();
	}
	
	/**
	 * Get the number of vertices (road intersections) in the graph
	 * @return The number of vertices in the graph.
	 */
	public int getNumVertices()
	{
		//TODO: Implement this method in WEEK 3
		return nodes.size();
	}
	
	/**
	 * Return the intersections, which are the vertices in this graph.
	 * @return The vertices in this graph as GeographicPoints
	 */
	public Set<GeographicPoint> getVertices()
	{
		//TODO: Implement this method in WEEK 3
		return nodes.keySet();
	}
	
	/**
	 * Get the number of road segments in the graph
	 * @return The number of edges in the graph.
	 */
	public int getNumEdges()
	{
		//TODO: Implement this method in WEEK 3
		int num = 0;
		for (GeographicPoint node: nodes.keySet()){
			num += nodes.get(node).size();
		}
		return num;
	}

	private Set<GeographicPoint> getOutNeighbours(GeographicPoint node){
		return nodes.get(node).keySet();
	}

    private double getDist(GeographicPoint start, GeographicPoint end){
		return nodes.get(start).get(end).length;
	}
	
	/** Add a node corresponding to an intersection at a Geographic Point
	 * If the location is already in the graph or null, this method does 
	 * not change the graph.
	 * @param location  The location of the intersection
	 * @return true if a node was added, false if it was not (the node
	 * was already in the graph, or the parameter is null).
	 */
	public boolean addVertex(GeographicPoint location)
	{
		// TODO: Implement this method in WEEK 3
		if (!nodes.containsKey(location)){
			nodes.put(location, new HashMap<GeographicPoint, EdgeInfo>());
			return true;
		}
		return false;
	}
	
	/**
	 * Adds a directed edge to the graph from pt1 to pt2.  
	 * Precondition: Both GeographicPoints have already been added to the graph
	 * @param from The starting point of the edge
	 * @param to The ending point of the edge
	 * @param roadName The name of the road
	 * @param roadType The type of the road
	 * @param length The length of the road, in km
	 * @throws IllegalArgumentException If the points have not already been
	 *   added as nodes to the graph, if any of the arguments is null,
	 *   or if the length is less than 0.
	 */
	public void addEdge(GeographicPoint from, GeographicPoint to, String roadName,
			String roadType, double length) throws IllegalArgumentException {
		//TODO: Implement this method in WEEK 3
		if (!nodes.containsKey(from) | !nodes.containsKey(to)){
			throw new IllegalArgumentException();
		}
		EdgeInfo info = new EdgeInfo(roadName, roadType,length);
		nodes.get(from).put(to, info);
	}
	

	/** Find the path from start to goal using breadth first search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest (unweighted)
	 *   path from start to goal (including both start and goal).
	 */
	public List<GeographicPoint> bfs(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
        Consumer<GeographicPoint> temp = (x) -> {};
        return bfs(start, goal, temp);
	}
	
	/** Find the path from start to goal using breadth first search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest (unweighted)
	 *   path from start to goal (including both start and goal).
	 */
	public List<GeographicPoint> bfs(GeographicPoint start, 
			 					     GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		// TODO: Implement this method in WEEK 3
		Queue<GeographicPoint> queue = new LinkedList<>();
		HashMap<GeographicPoint, GeographicPoint> prevMap = new HashMap<>(); // key: current, val: previous
		queue.add(start);
		nodeSearched.accept(start);

		//BFS until find the goal
		while (queue.size() > 0){
			GeographicPoint current = queue.remove();
			for (GeographicPoint node: getOutNeighbours(current)){
				if (prevMap.containsKey(node)) {continue;}
				queue.add(node);
				prevMap.put(node, current);
				nodeSearched.accept(node);
				if (node.equals(goal)) {break;}
			}
		}

        //Backtrace for the route
		GeographicPoint current = goal;
		List<GeographicPoint> ans = new LinkedList<>();
		while (!start.equals(current)){
			ans.add(0,current);
			current = prevMap.get(current);
			if (current == null) {return null;}
		}
		ans.add(0,current);
		return ans;
	}
	

	/** Find the path from start to goal using Dijkstra's algorithm
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */

	public List<GeographicPoint> dijkstra(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
		// You do not need to change this method.
        Consumer<GeographicPoint> temp = (x) -> {};
        return dijkstra(start, goal, temp);
	}
	
	/** Find the path from start to goal using Dijkstra's algorithm
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> dijkstra(GeographicPoint start, 
										  GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		// TODO: Implement this method in WEEK 4\
		PriorityQueue<PriorityNode> queue = new PriorityQueue<>();
		HashMap<GeographicPoint, PriorityNode> prevMap = new HashMap<>(); // key: current, val: previous
		queue.add(new PriorityNode(start, 0));
		nodeSearched.accept(start);
		int count = 0;
		//BFS until find the goal
		while (queue.size() > 0){
			count++;
			PriorityNode tmp = queue.remove();
			GeographicPoint current = tmp.getNode();
			if (current.equals(goal)) {break;}
			double priority = tmp.getPriority();
			for (GeographicPoint node: getOutNeighbours(current)){
				double dist = priority + getDist(current, node);
				if (prevMap.containsKey(node) && prevMap.get(node).getPriority() <= dist) {
					continue;
				}
				PriorityNode pNode = new PriorityNode(node, dist);
				queue.add(pNode);
				prevMap.put(node, new PriorityNode(current, dist));
				nodeSearched.accept(node);
			}
		}
		//System.out.println(prevMap);
		//Backtrace for the route
		GeographicPoint current = goal;
		List<GeographicPoint> ans = new LinkedList<>();
		while (!start.equals(current)){
			ans.add(0,current);
			current = prevMap.get(current).getNode();
			if (current == null) {return null;}
		}
		ans.add(0,current);
		System.out.println(count);
		return ans;
	}

	/** Find the path from start to goal using A-Star search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> aStarSearch(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
        Consumer<GeographicPoint> temp = (x) -> {};
        return aStarSearch(start, goal, temp);
	}
	
	/** Find the path from start to goal using A-Star search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> aStarSearch(GeographicPoint start, 
											 GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		// TODO: Implement this method in WEEK 4
		PriorityQueue<PriorityNode> queue = new PriorityQueue<>();
		HashMap<GeographicPoint, PriorityNode> prevMap = new HashMap<>(); // key: current, val: previous
		queue.add(new PriorityNode(start, goal.distance(start)));
		nodeSearched.accept(start);
		int count = 0;
		//BFS until find the goal
		while (queue.size() > 0){
			count++;
			PriorityNode tmp = queue.remove();
			GeographicPoint current = tmp.getNode();
			if (current.equals(goal)) {break;}
			double priority = tmp.getPriority();
			for (GeographicPoint node: getOutNeighbours(current)){
				double dist = priority + getDist(current, node) + goal.distance(node) - goal.distance(current);
				if (prevMap.containsKey(node) && prevMap.get(node).getPriority() <= dist) {
					continue;
				}
				PriorityNode pNode = new PriorityNode(node, dist);
				queue.add(pNode);
				prevMap.put(node, new PriorityNode(current, dist));
				nodeSearched.accept(node);
			}
		}
		//System.out.println(prevMap);
		//Backtrace for the route
		GeographicPoint current = goal;
		List<GeographicPoint> ans = new LinkedList<>();
		while (!start.equals(current)){
			ans.add(0,current);
			current = prevMap.get(current).getNode();
			if (current == null) {return null;}
		}
		ans.add(0,current);
		System.out.println(count);
		return ans;
	}

	
	
	public static void main(String[] args)
	{
		System.out.print("Making a new map...");
		MapGraph firstMap = new MapGraph();
		System.out.print("DONE. \nLoading the map...");
		GraphLoader.loadRoadMap("data/testdata/simpletest.map", firstMap);
		System.out.println("DONE.");

		// You can use this method for testing.
		
		
		/* Here are some test cases you should try before you attempt
		 * the Week 3 End of Week Quiz, EVEN IF you score 100% on the
		 * programming assignment.
		 */
//		MapGraph simpleTestMap = new MapGraph();
//		GraphLoader.loadRoadMap("data/testdata/simpletest.map", simpleTestMap);
//
//		GeographicPoint testStart = new GeographicPoint(1.0, 1.0);
//		GeographicPoint testEnd = new GeographicPoint(8.0, -1.0);
//
//		System.out.println("Test 1 using simpletest: Dijkstra should be 9 and AStar should be 5");
//		List<GeographicPoint> testroute = simpleTestMap.dijkstra(testStart,testEnd);
//		List<GeographicPoint> testroute2 = simpleTestMap.aStarSearch(testStart,testEnd);
//		System.out.println(testroute);
//		System.out.println(testroute2);
//
//		MapGraph testMap = new MapGraph();
//		GraphLoader.loadRoadMap("data/maps/utc.map", testMap);
//
//		// A very simple test using real data
//		testStart = new GeographicPoint(32.869423, -117.220917);
//		testEnd = new GeographicPoint(32.869255, -117.216927);
//		System.out.println("Test 2 using utc: Dijkstra should be 13 and AStar should be 5");
//		testroute = testMap.dijkstra(testStart,testEnd);
//		testroute2 = testMap.aStarSearch(testStart,testEnd);
//
//
//		// A slightly more complex test using real data
//		testStart = new GeographicPoint(32.8674388, -117.2190213);
//		testEnd = new GeographicPoint(32.8697828, -117.2244506);
//		System.out.println("Test 3 using utc: Dijkstra should be 37 and AStar should be 10");
//		testroute = testMap.dijkstra(testStart,testEnd);
//		testroute2 = testMap.aStarSearch(testStart,testEnd);


		MapGraph theMap = new MapGraph();
		System.out.print("DONE. \nLoading the map...");
		GraphLoader.loadRoadMap("data/maps/utc.map", theMap);
		System.out.println("DONE.");

		GeographicPoint start = new GeographicPoint(32.8648772, -117.2254046);
		GeographicPoint end = new GeographicPoint(32.8660691, -117.217393);


		List<GeographicPoint> route = theMap.dijkstra(start,end);
		List<GeographicPoint> route2 = theMap.aStarSearch(start,end);

		
	}
	
}
