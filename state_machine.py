import re

class State:
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()
    def __eq__(self,other):
        return self.name == other.name
    def __ne__(self,other):
        return self.name != other.name
    def __hash__(self):
        return hash(self.name)
    
class Event:
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()
    def __eq__(self,other):
        return self.name == other.name
    def __ne__(self,other):
        return self.name != other.name
    def __hash__(self):
        return hash(self.name)

class StateTransition:
    def __init__(self, stf = {}, from_file = False, filename = None):
        self.stf = stf
        if (from_file):
            is_first = True
            with open(filename) as fh:
                for line in fh:
                    line = line.replace(' ','')
                    if is_first:
                        s = re.findall("(\S+)",line)[0]
                        self.state = State(s)
                        is_first = False
                    else:
                        t = re.findall("\((\S+)\,(\S+)\)->(\S+)",line)[0]
                        self.stf[(State(t[0]),Event(t[1]))] = State(t[2])
        else:
            self.stf = stf

    def state_update(self,event,from_code=False):
        if (from_code):
            try:
                event = code_to_event[event]
            except:
                print("Unknown event")
                return False
        try:
            print("Current state: {0!s}".format(self.state))
            print("Event: {0!s}".format(event))
            self.state = self.stf[(self.state,event)]
            print("New state: {0!s}".format(self.state))
            return True
        except:
            print("Unknown transition")
            return False
    

code_to_event = {
        714: Event('GAIN_UP'),
        715: Event('GAIN_DOWN'),
        304: Event('B1'),
        305: Event('B2'),
        306: Event('B3'),
        307: Event('B4'),
        308: Event('B5'),
        708: Event('SYM_UP'),
        709: Event('SYM_DOWN'),
        309: Event('B6'),
        310: Event('B7'),
        311: Event('B8'),
        312: Event('B9'),
        313: Event('B10'),
        710: Event('CON_UP'),
        711: Event('CON_DOWN'),
        314: Event('B11'),
        315: Event('B12'),
        316: Event('B13'),
        317: Event('B14'),
        318: Event('B15'),
        712: Event('BRT_UP'),
        713: Event('BRT_DOWN'),
        319: Event('B16'),
        704: Event('B17'),
        705: Event('B18'),
        706: Event('B19'),
        707: Event('B20')
    }

