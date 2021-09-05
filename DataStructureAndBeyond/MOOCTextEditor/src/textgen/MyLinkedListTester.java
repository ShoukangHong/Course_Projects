/**
 * 
 */
package textgen;

import static org.junit.Assert.*;

import java.util.LinkedList;

import org.junit.Before;
import org.junit.Test;

/**
 * @author UC San Diego MOOC team
 *
 */
public class MyLinkedListTester {

	private static final int LONG_LIST_LENGTH =10; 

	MyLinkedList<String> shortList;
	MyLinkedList<Integer> emptyList;
	MyLinkedList<Integer> longerList;
	MyLinkedList<Integer> list1;
	
	/**
	 * @throws java.lang.Exception
	 */
	@Before
	public void setUp() throws Exception {
		// Feel free to use these lists, or add your own
	    shortList = new MyLinkedList<String>();
		shortList.add("A");
		shortList.add("B");
		emptyList = new MyLinkedList<Integer>();
		longerList = new MyLinkedList<Integer>();
		for (int i = 0; i < LONG_LIST_LENGTH; i++)
		{
			longerList.add(i);
		}
		list1 = new MyLinkedList<Integer>();
		list1.add(65);
		list1.add(21);
		list1.add(42);
		
	}

	
	/** Test if the get method is working correctly.
	 */
	/*You should not need to add much to this method.
	 * We provide it as an example of a thorough test. */
	@Test
	public void testGet()
	{
		//test empty list, get should throw an exception
		try {
			emptyList.get(0);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		
		// test short list, first contents, then out of bounds
		assertEquals("Check first", "A", shortList.get(0));
		assertEquals("Check second", "B", shortList.get(1));
		
		try {
			shortList.get(-1);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		try {
			shortList.get(2);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		// test longer list contents
		for(int i = 0; i<LONG_LIST_LENGTH; i++ ) {
			assertEquals("Check "+i+ " element", (Integer)i, longerList.get(i));
		}
		
		// test off the end of the longer array
		try {
			longerList.get(-1);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		try {
			longerList.get(LONG_LIST_LENGTH);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		}
		
	}
	
	
	/** Test removing an element from the list.
	 * We've included the example from the concept challenge.
	 * You will want to add more tests.  */
	@Test
	public void testRemove()
	{
		int a = list1.remove(0);
		assertEquals("Remove: check a is correct ", 65, a);
		assertEquals("Remove: check element 0 is correct ", (Integer)21, list1.get(0));
		assertEquals("Remove: check size is correct ", 2, list1.size());
		
		// TODO: Add more tests here
		try {
			emptyList.remove(0);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {}

		a = longerList.remove(LONG_LIST_LENGTH - 1);
		assertEquals("Remove: check a is correct ", LONG_LIST_LENGTH - 1, a);
		assertEquals("Remove: check element 0 is correct ", (Integer)0, longerList.get(0));
		assertEquals("Remove: check size is correct ", LONG_LIST_LENGTH - 1, longerList.size());
		try{
			longerList.remove(LONG_LIST_LENGTH - 1);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {}
		assertEquals("Add: check size is correct ", LONG_LIST_LENGTH - 1, longerList.size());

		longerList.add(LONG_LIST_LENGTH - 1);
		a = longerList.get(LONG_LIST_LENGTH - 1);
		assertEquals("Add: check longlist tail is correct", LONG_LIST_LENGTH - 1, a);
		assertEquals("Add: check size is correct ", LONG_LIST_LENGTH, longerList.size());

		emptyList.add(10);
		emptyList.add(10);
		emptyList.remove(0);
		emptyList.remove(0);
		assertNull("Remove: check emptyList tail is correct", emptyList.tail);
		assertNull("Remove: check emptyList head is correct", emptyList.head);
		assertEquals("Remove: check emptyList size is correct", 0, emptyList.size());
	}
	
	/** Test adding an element into the end of the list, specifically
	 *  public boolean add(E element)
	 * */
	@Test
	public void testAddEnd()
	{
        // TODO: implement this test
		try {
			shortList.add(0, null);
			fail("Check add null");
		}
		catch (NullPointerException e) {}

		emptyList.add(10);
		LLNode tail = emptyList.tail;
		LLNode head = emptyList.head;
		assertEquals("Add: check emptyList tail is correct", 10, tail.data);
		assertEquals("Add: check emptyList head is correct", 10, head.data);
		assertNull("Add: check emptyList head prev is correct", head.prev);
		assertNull("Add: check emptyList tail prev is correct", tail.prev);
		assertNull("Add: check emptyList head next is correct", head.next);
		assertNull("Add: check emptyList tail next is correct", tail.next);
		assertEquals("Add: check emptyList size is correct", 1, emptyList.size());

		emptyList.add(20);
		tail = emptyList.tail;
		head = emptyList.head;
		assertEquals("Add: check emptyList tail is correct", 20, tail.data);
		assertEquals("Add: check emptyList head is correct", 10, head.data);
		assertNull("Add: check emptyList head prev is correct", head.prev);
		assertEquals("Add: check emptyList tail prev is correct", 10, tail.prev.data);
		assertEquals("Add: check emptyList head next is correct", 20, head.next.data);
		assertNull("Add: check emptyList tail next is correct", tail.next);
		assertEquals("Add: check emptyList size is correct", 2, emptyList.size());

		emptyList.add(30);
		tail = emptyList.tail;
		head = emptyList.head;
		assertEquals("Add: check edited emptyList tail is correct", 30, tail.data);
		assertEquals("Add: check edited emptyList head is correct", 10, head.data);
		assertNull("Add: check edited emptyList head prev is correct", head.prev);
		assertEquals("Add: check edited emptyList tail prev is correct", 20, tail.prev.data);
		assertEquals("Add: check edited emptyList head next is correct", 20, head.next.data);
		assertEquals("Add: check edited emptyList middle next is correct", 30, head.next.next.data);
		assertEquals("Add: check edited emptyList middle prev is correct", 10, tail.prev.prev.data);
		assertNull("Add: check edited emptyList tail next is correct", tail.next);
		assertEquals("Add: check edited emptyList size is correct", 3, emptyList.size());

		emptyList.remove(2);
		emptyList.remove(1);
		emptyList.remove(0);
	}

	
	/** Test the size of the list */
	@Test
	public void testSize()
	{
		// TODO: implement this test
		assertEquals("Size: check emptyList size is correct", 0, emptyList.size());
		assertEquals("Size: check longList size is correct", LONG_LIST_LENGTH, longerList.size());
	}

	
	
	/** Test adding an element into the list at a specified index,
	 * specifically:
	 * public void add(int index, E element)
	 * */
	@Test
	public void testAddAtIndex()
	{
        // TODO: implement this test
		try {
			shortList.add(0, null);
			fail("Check add null");
		}
		catch (NullPointerException e) {}

		try {
			emptyList.add(1, 10);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {}

		try {
			emptyList.add(-1, 10);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {}

		emptyList.add(0, 10);
		LLNode tail = emptyList.tail;
		LLNode head = emptyList.head;
		assertEquals("Add: check emptyList tail is correct", 10, tail.data);
		assertEquals("Add: check emptyList head is correct", 10, head.data);
		assertNull("Add: check emptyList head prev is correct", head.prev);
		assertNull("Add: check emptyList tail prev is correct", tail.prev);
		assertNull("Add: check emptyList head next is correct", head.next);
		assertNull("Add: check emptyList tail next is correct", tail.next);
		assertEquals("Add: check emptyList size is correct", 1, emptyList.size());

		emptyList.add(1,20);
		tail = emptyList.tail;
		head = emptyList.head;
		assertEquals("Add: check emptyList tail is correct", 20, tail.data);
		assertEquals("Add: check emptyList head is correct", 10, head.data);
		assertNull("Add: check emptyList head prev is correct", head.prev);
		assertEquals("Add: check emptyList tail prev is correct", 10, tail.prev.data);
		assertEquals("Add: check emptyList head next is correct", 20, head.next.data);
		assertNull("Add: check emptyList tail next is correct", tail.next);
		assertEquals("Add: check emptyList size is correct", 2, emptyList.size());

		emptyList.remove(1);
		emptyList.add(1,30);
		emptyList.add(1,20);
		tail = emptyList.tail;
		head = emptyList.head;
		assertEquals("Add: check edited emptyList tail is correct", 30, tail.data);
		assertEquals("Add: check edited emptyList head is correct", 10, head.data);
		assertNull("Add: check edited emptyList head prev is correct", head.prev);
		assertEquals("Add: check edited emptyList tail prev is correct", 20, tail.prev.data);
		assertEquals("Add: check edited emptyList head next is correct", 20, head.next.data);
		assertEquals("Add: check edited emptyList middle next is correct", 30, head.next.next.data);
		assertEquals("Add: check edited emptyList middle prev is correct", 10, tail.prev.prev.data);
		assertNull("Add: check edited emptyList tail next is correct", tail.next);
		assertEquals("Add: check edited emptyList size is correct", 3, emptyList.size());

		emptyList.remove(0);
		emptyList.add(0, 10);
		tail = emptyList.tail;
		head = emptyList.head;
		assertEquals("Add: check edited emptyList tail is correct", 30, tail.data);
		assertEquals("Add: check edited emptyList head is correct", 10, head.data);
		assertNull("Add: check edited emptyList head prev is correct", head.prev);
		assertEquals("Add: check edited emptyList tail prev is correct", 20, tail.prev.data);
		assertEquals("Add: check edited emptyList head next is correct", 20, head.next.data);
		assertEquals("Add: check edited emptyList middle next is correct", 30, head.next.next.data);
		assertEquals("Add: check edited emptyList middle prev is correct", 10, tail.prev.prev.data);
		assertNull("Add: check edited emptyList tail next is correct", tail.next);
		assertEquals("Add: check edited emptyList size is correct", 3, emptyList.size());
	}
	
	/** Test setting an element in the list */
	@Test
	public void testSet()
	{
	    // TODO: implement this test
		try {
			shortList.set(0, null);
			fail("Check add null");
		}
		catch (NullPointerException e) {}

		try {
			emptyList.set(0, 10);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {}
		try {
			longerList.set(11, LONG_LIST_LENGTH);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {}

		longerList.set(9, 20);
		longerList.set(0, -20);
		longerList.set(5, 0);
		LLNode tail = longerList.tail;
		LLNode head = longerList.head;
		int last = longerList.get(9);
		int first = longerList.get(0);
		int mid = longerList.get(5);
		assertEquals("Set: check longer list tail val", 20, tail.data);
		assertEquals("Set: check longer list last val", 20, last);
		assertEquals("Set: check longer list head val", -20, head.data);
		assertEquals("Set: check longer list first val", -20, first);
		assertEquals("Set: check longer list mid val", 0, mid);
	}
	
	
	// TODO: Optionally add more test methods.
	
}
