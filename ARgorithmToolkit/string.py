"""The string module provides support for immutable strings. The main class in
this module is the String class. The StringState acts as a support class to
String class. For this reason the String class can directly be imported from
the ARgorithmToolkit library without having to import from the string module:

    >>> s = ARgorithmToolkit.string.String(name="s",algo=algo)
    >>> s = ARgorithmToolkit.String(name="s",algo=algo)
"""

from ARgorithmToolkit.utils import ARgorithmHashable, State, StateSet, ARgorithmError, ARgorithmStructure
from ARgorithmToolkit.encoders import serialize

class StringState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.string.String`` object.

    Attributes:

        name (str) : Name of the variable for whom we are generating states
        _id (str) : id of the variable for whom we are generating states
    """

    def __init__(self, name, _id):
        self.name = name
        self._id = _id

    def string_declare(self, body, comments=""):
        """Generates the `string_declare` state when an instance of string is
        created.

        Args:
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `string_declare` state for respective string
        """

        state_type = "string_declare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def string_iter(self, body, index, comments=""):
        """Generates the `string_iter` state when an character of string has
        been accessed.

        Args:
            body (str): The string
            index (int): The index which has been accessed
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `string_iter` state for respective string
        """
        state_type = "string_iter"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body,
            "index" : index
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def string_append(self, body, element, comments=""):
        """Generates the `string_append` state when another string has been
        appended to this string.

        Args:
            body (str): The original string appended with new string
            element (str): The new string that has been appended
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `string_append` state for respective string
        """
        state_type = "string_append"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body,
            "element" : element,
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

class StringIterator:
    """This class is a generator that is returned each time an string has to be
    iterated.

    Yields:
        character of string

    Raises:
        AssertionError: If not declared with an instance of ARgorithmToolkit.string.String
    """

    def __init__(self,string):
        assert isinstance(string,String)
        self.string = string
        self._index = 0
        self.size = len(string)

    def __next__(self):
        if self._index == self.size:
            raise StopIteration
        v = self.string[self._index]
        self._index += 1
        return v

@serialize
class String(ARgorithmStructure, ARgorithmHashable):
    """The String class is a wrapper around the already existing string class
    in python adding the feature to store states.

    Attributes:
        name (str): name given to the rendered block in augmented reality. Essential. Should not be altered after initialisation
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of String Class
        body (str , optional) : The contents of String. Defaults to "".

    Raises:
        ARgorithmError: raised if name is not given or Stateset if not provided
        TypeError: raised if body not a string

    Example:
        >>> algo = ARgorithmToolkit.StateSet()
        >>> st = ARgorithmToolkit.String('st', algo, "Hello world! 1234")
        >>> st
        String('Hello world! 1234')
    """
    def __init__(self,name,algo,body='',comments=""):
        try:
            assert isinstance(name,str)
            self._id = str(id(self))
            self.state_generator = StringState(name, self._id)
        except AssertionError as e:
            raise ARgorithmError('Give valid name to data structure') from e
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise TypeError("string structure needs a reference of StateSet to store states") from e
        try:
            assert isinstance(body,str)
            self.body = body
        except AssertionError as e:
            raise ARgorithmError("String body should be of type string") from e
        state = self.state_generator.string_declare(self.body,comments)
        self.algo.add_state(state)

    def __len__(self):
        """The operator overload for len() function. Returns size of string.

        Returns:
            int: size of string

        Example:
            >>> st
            String('Hello world! 1234hahaha')
            >>> len(st)
            23
        """
        return len(self.body)

    def __getitem__(self,key):
        """The operator overload for string indexing as well as string
        splicing.

        Args:
            key (index): If int then character at index is returned. Else if slice , then substring is returned
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            str: The character at index or substring wrt to slicing

        Example:
            >>> st
            String('Hello world! 1234hahaha')
            >>> st[2]
            'l'
            >>> st[2:6]
            String('llo ')
        """
        if isinstance(key,slice):
            name = f"{self.state_generator.name}_sub"
            return String(name , self.algo , self.body[key] , comments=f"creating new substring for {key}")
        state = self.state_generator.string_iter(self.body,key,comments=f"accessing character at {key}")
        self.algo.add_state(state)
        return self.body[key]


    def __setitem__(self, key, value):
        """As this wrapper is for immutable string, set item is not supported
        so an error is raised.

        Raises:
            TypeError: Raised always
        """
        raise ARgorithmError("'String' object does not support item assignment")

    def __iter__(self):
        """Returns iterator for string.

        Returns:
            [StringIterator]: The generator object for the String

        Example:
            >>> st
            String('Hello world! 1234hahaha')
            >>> [s for s in st]
            ['H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!', ' ', '1', '2', '3', '4', 'h', 'a', 'h', 'a', 'h', 'a']
        """
        return StringIterator(self)

    def __repr__(self):
        return f"String({repr(self.body)})"

    def __str__(self):
        return str(self.body)

    def append(self, value, comments=''):
        """appends second string (that is value) to self.

        Args:
            value (str or String): The string that is to be appeneded
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Example:
            >>> st
            String('Hello world! 1234')
            >>> st.append("hahaha")
            >>> st
            String('Hello world! 1234hahaha')
        """
        if isinstance(value,String):
            value = value.body
        self.body += value
        state = self.state_generator.string_append(self.body , value, comments)
        self.algo.add_state(state)

    def __add__(self, value):
        """Operator overload for addition operation that work similar to append
        but returns a new String object.

        Returns:
            [String]: The new string that is the addition of the 2 strings

        Example:
            >>> st
            String('Hello world! 1234hahaha')
            >>> x = st + "?!"
            >>> x
            String('Hello world! 1234hahaha?!')
        """
        if isinstance(value,String):
            value = value.body
        name = f"{self.state_generator.name}_super"
        new = String(name=name, algo=self.algo, body=self.body, comments=f'creating new string with {value} appended to the original string')
        new.append(value)
        return new
