# Base template that all algorithms will use

# error class to simplify user debugging
class ARgorithmError(Exception):

  def __init__(self,*args):
    if args:
        self.message = args[0]
    else:
        self.message = None
        
  def __str__(self):
    if self.message:
        return f'{self.message}'
    else:
        return f"There's an error within ARgorithm template usage"


# the template class to store states for our algorithms
class Template:

    def __init__(self):
        self.states = []

    def add_state(self,state):
        assert type(state) == State , ARgorithmError("state should be of Type state")
        self.states.append(state)

    def __str__(self):
        state_desc = "\n".join([x for x in self.states]) if len(self.states) > 0 else ""
        return f"{state_desc}"


# the state template class to ensure each state is of same structure

class State:
    def __init__(self,**kwargs):
        self.content = {}
        for x in ['state_type','state_def','comments']:
            try:
                self.content[x] = kwargs[x]
            except:
                raise ARgorithmError(f"{x} should be present in State arguments")

    def __str__(self):
        data = str(self.content)
        return data

# this is to store any important variables to your algo that you can highlight
# prefer this for int , char , bool
class Variable:
    def __init__(self,name,algo,value=None,comments=""):
        self.value = value
        self.algo = algo
        self.name = name
        state_type = "variable_declare"
        state_def = {
            "variable_name" : name ,
            "value" : value  
        }
        self.algo.add_state(State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        ))
        
    def highlight(self,comments=""):
        state_type = "variable_highlight"
        state_def = {
            "variable_name" : self.name,
            "value" : self.value
        }
        self.algo.add_state(State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        ))