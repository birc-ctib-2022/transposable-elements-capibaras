"""A circular genome for simulating transposable elements."""
from __future__ import annotations
from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)
from typing import (
    Generic, TypeVar, Iterable,
    Callable, Protocol
)

from typing import Type

class Genome(ABC):
    """Representation of a circular enome."""

    ## transposable_elements: dict that will contain the active te_s
    ##                          {id, [pos,length]}
    transposable_elements = {}
   
        
    def __init__(self, n: int):
        """Create a genome of size n."""
        self.genome = ['-'] * n

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...


    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        
        ...  # not implemented yet
    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        #return ''.join(self.genome)


class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """
    transposable_elements = {}
    ## id initializer
    tes_counter = 1
    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.genome = ['-'] * n
        
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
       
        for id, info in self.transposable_elements.items():
            ## if new te is Active: find the id in the range pos : pos+length
            if self.genome[pos] == 'A' and (info[0] <= pos <= info[0]+info[1]):
                    self.disable_te(id)
                    break
            ## update positions in dictionary
            if (info[0] > pos):
                    self.transposable_elements[id] = [info[0]+length,info[1]]
                      
            
        ## insert the tes in the genome
        self.genome[pos:pos] =length*['A'] 
    
        ## update the dictionary that contains the active te_s
        id = ListGenome.tes_counter
        self.transposable_elements[id] = [pos,length]  
        ListGenome.tes_counter += 1  
        
        #print(self.transposable_elements)
        return id
        
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ## If te is not active, return None 
        if te not in self.transposable_elements.keys():
            return None
        else:
            pos = self.transposable_elements[te][0]
            length = self.transposable_elements[te][1]
            
            #print(pos,offset,len(self.genome),insertion_position)
            insertion_position = (pos+offset) % len(self.genome)
            return self.insert_te(insertion_position,length)

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ## drop from the dictionary since it is no longer active
        dropp_te = self.transposable_elements.pop(te)
        
        pos = dropp_te[0]
        l = dropp_te[1]    
        ## deactive in the genome   
        self.genome[pos:pos+l] = ['x']*l
        

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.transposable_elements.keys())

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.genome)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        return ''.join(self.genome)



T = TypeVar('T')

class Link(Generic[T]):
    """Doubly linked link."""

    val: T
    prev: Link[T]
    next: Link[T]

    def __init__(self, val: T, p: Link[T], n: Link[T]):
        """Create a new link and link up prev and next."""
        self.val = val
        self.prev = p
        self.next = n
    def __str__(self) -> str:
        return str(self.val)

def insert_after(link: Link[T], val: T) -> None:
    """Add a new link containing avl after link."""
    new_link = Link(val, link, link.next)
    new_link.prev.next = new_link
    new_link.next.prev = new_link


class DLList(Generic[T]):
    head: Link[T]  # Dummy head link

    def __init__(self, seq: Iterable[T] = ()):
        """Create a new circular list from a sequence."""
        self.head = Link(None, None, None)  # type: ignore
        self.head.prev = self.head
        self.head.next = self.head
        for val in seq:
            insert_after(self.head.prev, val)
    
    def __str__(self) -> str:
        elms: list[str] = []
        link = self.head.next
        while link and link is not self.head:
            elms.append(str(link.val))
            link = link.next
        return f"[{', '.join(elms)}]"
    __repr__ = __str__  # because why not?

    def __iter__(self) -> Iterable[T]:     #iterator 
        link = self.head.next
        while link != self.head:
            yield link.val
            link = link.next 
           
    def insert_n_elements(self,link_of_pos,length):
        how_long = length
        while how_long:
            insert_after(link_of_pos,'A')
            link_of_pos = link_of_pos.next
            how_long -= 1
        
    def get_position(self, position):
        if position < 1:  # Just in case the position is too small
            return
        current = self.head.next
        while current and position > 1:
            position -= 1
            current = current.next
        return current
    
    def __len__(self):
        link = self.head.next
        length = 0
        while link != self.head:
            length += 1
            link = link.next
        return length    


class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """
    ## id initializer
    tes_counter = 1
    genome:  DLList

    def __init__(self, n: int):
        """Create a new genome with length n."""
        ...  
        seg = ['-']*n
        self.genome = DLList(seg)

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ## get position to insert new te
        link_of_pos = self.genome.get_position(pos)
        
        for id, info in self.transposable_elements.items():
            ## if new te is Active, disable
            if link_of_pos.val == 'A':
                if info[0] <= pos <= info[0]+info[1]:
                    self.disable_te(id)
                    break
            ## update positions in dictionary
            if (info[0] > pos):
                    self.transposable_elements[id] = [info[0]+length,info[1]]
        
        ## insert in the linked list
        self.genome.insert_n_elements(link_of_pos,length)
                    
        id = LinkedListGenome.tes_counter
        self.transposable_elements[id] = [pos,length]  
        LinkedListGenome.tes_counter += 1  
        return id
    

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ## If te is not active, return None 
        if te not in self.transposable_elements.keys():
            return None
        else:
            pos = self.transposable_elements[te][0]
            length = self.transposable_elements[te][1]
            insertion_position = (pos+offset) % len(self.genome)
            return self.insert_te(insertion_position,length)
   

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        how_long = self.transposable_elements[te][1]
        active_counter = 0
        link = self.genome.head.next
        for id, info in self.transposable_elements.items():
            if id == te:
                while info[0] != active_counter:
                    link =  link.next
                    active_counter += 1
        
        while how_long:
            link.val = 'x'
            link = link.next
            how_long -= 1
        self.transposable_elements.pop(te)
        


    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        # FIXME
        return list(self.transposable_elements.keys())

    def __len__(self) -> int:
        """Current length of the genome."""
        # FIXME
        return len(self.genome)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        return ''.join(self.genome)
