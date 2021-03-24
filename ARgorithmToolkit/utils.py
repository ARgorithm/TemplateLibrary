"""The utils module is the most important module of the entire library with the
most important classes stored in the utils module. Due to the importance of
these classes, all these classes can be directly imported from
ARgorithmToolkit.

Both work:
    >>> algo = ARgorithmToolkit.utils.StateSet()
    >>> algo = ARgorithmToolkit.StateSet()
"""
class ARgorithmError(Exception):
    """The error class for ARgorithmToolkit.

    Used to debug errors that are caused due to the logic and internal
    workings of ARgorithmToolkit
    """
    def __init__(self,*args):
        super().__init__(*args)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'{self.message}'
        return "There's an error within ARgorithm"

class ARgorithmClientError(Exception):
    """The error class for programmers to use in their ARgorithm.

    Programmers can throw this error from their program when they want
    to raise an error For example when user gives incorrect input to
    program
    """
    def __init__(self,*args):
        super().__init__(*args)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'{self.message}'
        return "User has entered faulty data"

class State:
    """The Instance of State class can be considered as an event in the
    sequential order of events that get played out in Augmented Reality Each
    Data structure has a helper class that makes states for it.

    For example , ARgorithmToolkit.array.Array has
    ARgorithmToolkit.array.ArrayState

    Attributes:
        state_type (str) : The State Type which has fixed value based on designs
        state_def (dict) : Definition of event that trigger this state
        comments (str) : Description of state event that can be given by user or auto-generated
        autoplay (bool) : Flag that suggested whether this state can automatically trigger the next in rendering process
    """
    state_type:str = ""
    state_def:dict = {}
    comments:str = ""
    autoplay:bool = False

    def __init__(self,**kwargs):
        for x in ['state_type','state_def','comments']:
            try:
                self.__dict__[x] = kwargs[x]
            except KeyError as e:
                raise ARgorithmError(f"{x} should be present in State arguments") from e
        if 'autoplay' in kwargs:
            self.autoplay = kwargs['autoplay']

    def __str__(self):
        content = {
            "state_type" : self.state_type,
            "state_def" : self.state_def,
            "comments" : self.comments,
            "autoplay" : self.autoplay
        }
        data = str(content)
        return data

class StateSet:
    """The most important class in the entire toolkit. An object of this class
    has to exist in every algorithm. That object of StateSet is what should
    returned by ARgorithm as that is what is rendered in Augmented Reality As
    these are what contain the metadata for rendering the algorithm. Instance
    of this class is conventionally called ``algo``

    Attributes:
        states (list): This is list of State objects that is sequentially rendered in Augmented Reality.
        autoplay (bool): If this is set, then all states

    Examples:
        >>> algo = ARgorithmToolkit.StateSet()
    """
    def __init__(self,autoplay=None):
        self.states = []
        try:
            assert isinstance(autoplay,bool) or autoplay is None
            self.autoplay = None
        except AssertionError as ae:
            raise TypeError("autoplay should be of type bool or None") from ae

    def add_state(self,state):
        """This method adds State to the list of states.

        Args:
            state (ARgorithmToolkit.utils.State): The state that has to be added

        Raises:
            ARgorithmError: Raised if state is not of type State

        Example:
            >>> algo.add_state(state)
        """
        assert isinstance(state,State) , ARgorithmError("state should be of Type state")
        self.states.append(state)

    def __str__(self):
        """String representation of StateSet.

        Returns:
            str: The list of all states in a multiline string
        """
        state_desc = "\n".join([x.__str__() for x in self.states]) if len(self.states) > 0 else ""
        return f"{state_desc}"

    def add_comment(self,comments:str):
        """Adds a blank state with just text information that could be used for
        describing content. Check the comments section for more info.

        Args:
            comments (str): Comments for descriptive purpose
        """
        comment_state = State(
            state_type="comment",
            state_def=None,
            comments=comments
        )
        self.add_state(comment_state)

class ARgorithmHashable:
    """Interface from which main classes for datastructures can inherit to make
    them hashable in Set and Map implementations.

    This interface will enable different classes to be keys in Map(hash-
    map) and Set(hash-set) implementations.
    """

class ARgorithmStructure:
    """Interface from which main classes for datastructures.

    This interface enables different classes to be a values in Map(hash-
    map) implementations.
    """

class Variable(ARgorithmStructure, ARgorithmHashable):
    """Some programs might need us to listen and store states of primitive
    datatypes like int, str , bool etc. For tha purpose, we have the Variable
    class.

    Attributes:
        name (str): name given to the rendered block in augmented reality. Essential. Should not be altered after initialisation
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of Variable Class
        value : The data stored in the variable

    Example:
        >>> flag = ARgorithmToolkit.Variable(name="flag",algo=algo,value=True)
        >>> count = ARgorithmToolkit.Variable(name="count",algo=algo,value=0)

    Note:
        Making changes in values of variable might seen hectic for now but future versions will fix the matter
    """
    def __init__(self,name:str,algo:StateSet,value=None,comments=""):
        self.algo = algo
        self.name = name
        self.__flag = False
        self.value = value
        self._id = str(id(self))
        state_type = "variable_declare"
        state_def = {
            "id" : self._id,
            "variable_name" : name ,
            "value" : value
        }
        self.algo.add_state(State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        ))

    def __setattr__(self,key,value):
        """Operator overload to listen to changes in value of Variables.

        Args:
            key ([type]): [description]
            value ([type]): [description]
        """
        last_value = None
        if key=='value' and self.__flag:
            last_value = self.value
        self.__dict__[key] = value
        if(key == 'value' and self.__flag):
            state_type = "variable_highlight"
            state_def = {
                "id" : self._id,
                "variable_name" : self.name,
                "value" : self.value,
            }
            if last_value is not None:
                state_def["last_value"] = last_value
            self.algo.add_state(State(
                state_type=state_type,
                state_def=state_def,
                comments=""
            ))
        elif key=='value':
            self.__flag = True

    def __repr__(self):
        return f"Variable({repr(self.value)})"
