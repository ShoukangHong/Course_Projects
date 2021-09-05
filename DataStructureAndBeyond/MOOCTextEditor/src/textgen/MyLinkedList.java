package textgen;

import javax.management.remote.rmi._RMIConnection_Stub;
import java.util.AbstractList;


/** A class that implements a doubly linked list
 * 
 * @author UC San Diego Intermediate Programming MOOC team
 *
 * @param <E> The type of the elements stored in the list
 */
public class MyLinkedList<E> extends AbstractList<E> {
	LLNode<E> head;
	LLNode<E> tail;
	int size;

	/** Create a new empty LinkedList */
	public MyLinkedList() {
		// TODO: Implement this method
		head = null;
		tail = null;
		size = 0;
	}

	/**
	 * Appends an element to the end of the list
	 * @param element The element to add
	 */
	public boolean add(E element ) 
	{
		// TODO: Implement this method
		checkNull(element);
		LLNode<E> last = new LLNode<E>(element);
		size += 1;
		if (head == null){
			head = last;
			tail = last;
		} else if (size == 2){
			tail = last;
			head.next = tail;
			tail.prev = head;
		} else {
				tail.next = last;
				last.prev = tail;
				tail = last;
		}
		return false;
	}

	/** Get the element at position index 
	 * @throws IndexOutOfBoundsException if the index is out of bounds. */
	public E get(int index) 
	{
		// TODO: Implement this method.
		return (E) getNode(index).data;
	}

	/**
	 * Add an element to the list at the specified index
	 * @param index The index where the element should be added
	 * @param element The element to add
	 */
	public void add(int index, E element ) 
	{
		// TODO: Implement this method
		checkNull(element);
		if (index == size){
			add(element);
			return;
		}
		LLNode node = getNode(index);
		LLNode insert = new LLNode(element);
		size += 1;
		if (index == 0){
			insert.next = head;
			head.prev = insert;
			head = insert;
		} else{
			node.prev.next = insert;
			insert.prev = node.prev;
			node.prev = insert;
			insert.next = node;
		}
	}


	/** Return the size of the list */
	public int size() 
	{
		// TODO: Implement this method
		return size;
	}

	/** Remove a node at the specified index and return its data element.
	 * @param index The index of the element to remove
	 * @return The data element removed
	 * @throws IndexOutOfBoundsException If index is outside the bounds of the list
	 * 
	 */
	public E remove(int index) 
	{
		// TODO: Implement this method
		LLNode node = getNode(index);
		if (index == 0){
			if (size == 1){
				head = null;
				tail = null;
			}else{
				head = head.next;
				head.prev = null;
			}
		} else {
			node.prev.next = node.next;
			if (node.next != null){
				node.next.prev = node.prev;
			} else {
				tail = node.prev;
			}
		}
		size -= 1;
		return (E) node.data;
	}

	/**
	 * Set an index position in the list to a new element
	 * @param index The index of the element to change
	 * @param element The new element
	 * @return The element that was replaced
	 * @throws IndexOutOfBoundsException if the index is out of bounds.
	 */
	public E set(int index, E element) 
	{
		// TODO: Implement this method
		checkNull(element);
		LLNode node = getNode(index);
		E ans = (E) node.data;
		node.data = element;
		return ans;
	}

	private void checkValid(int index)
	{
		if (head == null | index < 0 | index >= size){
			throw new IndexOutOfBoundsException();
		}
	}

	private LLNode getNode(int index){
		checkValid(index);
		LLNode ans = head;
		for (int i = 0; i < index; i++){
			ans = ans.next;
		}
		return ans;
	}

	private void checkNull(E element){
		if (element == null){
			throw new NullPointerException();
		}
	}
}

class LLNode<E> 
{
	LLNode<E> prev;
	LLNode<E> next;
	E data;

	// TODO: Add any other methods you think are useful here
	// E.g. you might want to add another constructor

	public LLNode(E e) 
	{
		this.data = e;
		this.prev = null;
		this.next = null;
	}

}
