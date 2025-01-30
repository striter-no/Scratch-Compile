import json as jn

def str_all(inp_list: list) -> list[str]:
    return [str(i) for i in inp_list]

class Costume:
    def __init__(self, data: dict, isStage: bool) -> None:
        self._data = data
        self.name: str = data["name"]
        self.dataFormat: str = data["dataFormat"]
        self.assetId: str = data["assetId"]
        self.md5ext: str = data["md5ext"]
        self.rotationCenterX: float = data["rotationCenterX"]
        self.rotationCenterY: float = data["rotationCenterY"]
        if not isStage:
            self.bitmapResolution: int = data["bitmapResolution"]

    def __str__(self) -> str:
        o = "Costume:"
        o += f"\n\tname = {self.name}"
        o += f"\n\tdataFormat = {self.dataFormat}"
        o += f"\n\tassetId = {self.assetId}"
        o += f"\n\tmd5ext = {self.md5ext}"
        o += f"\n\trotationCenterX = {self.rotationCenterX}"
        o += f"\n\trotationCenterY = {self.rotationCenterY}"
        if not self._isStage:
            o += f"\n\tbitmapResolution = {self.bitmapResolution}"
        
        return o

'''
https://github.com/scratchfoundation/scratch-vm/blob/develop/src/serialization/sb3.js

const MATH_NUM_PRIMITIVE = 4; // there's no reason these constants can't collide
// math_positive_number
const POSITIVE_NUM_PRIMITIVE = 5; // with the above, but removing duplication for clarity
// math_whole_number
const WHOLE_NUM_PRIMITIVE = 6;
// math_integer
const INTEGER_NUM_PRIMITIVE = 7;
// math_angle
const ANGLE_NUM_PRIMITIVE = 8;
// colour_picker
const COLOR_PICKER_PRIMITIVE = 9;
// text
const TEXT_PRIMITIVE = 10;
// event_broadcast_menu
const BROADCAST_PRIMITIVE = 11;
// data_variable
const VAR_PRIMITIVE = 12;
// data_listcontents
const LIST_PRIMITIVE = 13;

// Map block opcodes to the above primitives and the name of the field we can use
// to find the value of the field
const primitiveOpcodeInfoMap = {
    math_number: [MATH_NUM_PRIMITIVE, 'NUM'],
    math_positive_number: [POSITIVE_NUM_PRIMITIVE, 'NUM'],
    math_whole_number: [WHOLE_NUM_PRIMITIVE, 'NUM'],
    math_integer: [INTEGER_NUM_PRIMITIVE, 'NUM'],
    math_angle: [ANGLE_NUM_PRIMITIVE, 'NUM'],
    colour_picker: [COLOR_PICKER_PRIMITIVE, 'COLOUR'],
    text: [TEXT_PRIMITIVE, 'TEXT'],
    event_broadcast_menu: [BROADCAST_PRIMITIVE, 'BROADCAST_OPTION'],
    data_variable: [VAR_PRIMITIVE, 'VARIABLE'],
    data_listcontents: [LIST_PRIMITIVE, 'LIST']
};
'''

class VariableType:
    def __init__(self, name: (str | None) = None, constant: (int | None) = None) -> None:
        constants = {
            "math_num_primitive": 4,
            "math_positive_number": 5,
            "math_whole_number": 6,
            "math_integer": 7,
            "math_angle": 8,
            "colour_picker": 9,
            "text": 10,
            "event_broadcast_menu": 11,
            "data_variable": 12,
            "data_listcontents": 13,
        }

        self._data = name
        
        self.name = name
        self.number_constant = constant

        if not (name is None):
            self.number_constant = constants[name]
        elif not (constant is None):
            self.name = list(constants.keys())[list(constants.values()).index(constant)]
        else:
            raise ValueError(f"Unknown variable type: ({name}/{constant})")

class Variable:
    def __init__(self, data: list) -> None:
        self._data = data
        self.type: VariableType = VariableType(constant=data[0][0])
        self.name: str = data[0]
        self.value: float = data[1]
    
    def __str__(self) -> str:
        o = "Variable:"
        o += f"\n\tName: {self.name}"
        o += f"\n\tValue: {self.value}"

        return o

class List:
    def __init__(self, data: list) -> None:
        self._data = data
        self.name: str = data[0]
        self.data: list[float] = data[1]
    
    def __str__(self) -> str:
        o = "List:"
        o += f"\n\tname = {self.name}"
        o += f"\n\tdata = {self.data}"
        
        return o

class Block:
    def __init__(self, data: dict) -> None:
        self._data = data
        
        self.opcode: str = data["opcode"]
        self.next: str = data["next"]
        self.parent: str = data["parent"]
        self.shadow: bool = data["shadow"]
        self.topLevel: bool = data["topLevel"]

        self.isTop = False

        if "x" in data:
            self.x: float = data["x"]
            self.y: float = data["y"]
            self.isTop = True

        self.fields: list[str] = data["fields"]
        self.inputs: dict[str, Input] = {} # Filled in later

        for name, raw_input in data["inputs"].items():
            self.inputs[name] = Input(raw_input)

    def __str__(self) -> str:

        parsed_inputs = {i: str(self.inputs[i]) for i in self.inputs}

        o = "Block:"
        o += f"\n\topcode = {self.opcode}"
        o += f"\n\tnext = {self.next}"
        o += f"\n\tparent = {self.parent}"
        o += f"\n\tshadow = {self.shadow}"
        o += f"\n\ttopLevel = {self.topLevel}"
        o += f"\n\tisTop = {self.isTop}"
        o += f"\n\tinputs = {parsed_inputs}"

        return o

class Input:
    def __init__(self, data: list) -> None:
        self._data = data

        self.__undef_num_0: int = data[0]
        self.__undef_num_1: int = data[1][0]
        self.value: str = data[1][1]

    def __str__(self) -> None:
        o = "Input:"
        o += f"\n\t__undef_num_0 = {self.__undef_num_0}"
        o += f"\n\t__undef_num_1 = {self.__undef_num_1}"
        o += f"\n\tvalue = {self.value}"

        return o

class ProjectTarget:
    def __init__(self, data: dict) -> None:
        self._data = data
        self.isStage: bool = data["isStage"]
        self.name: str = data["name"]
        self.currentCostume: int = data["currentCostume"]
        self.volume: int = data["volume"]
        self.layerOrder: int = data["layerOrder"]
        
        if self.isStage:
            self.tempo: int = data["tempo"]
            self.videoTransparency: int = data["videoTransparency"]
            self.videoState: bool = data["videoState"] == "on"
            self.textToSpeechLanguage: (str | None) = data["textToSpeechLanguage"]
        else:
            self.visible: bool = data["visible"]
            self.x: float = data["x"]
            self.y: float = data["y"]
            self.size: float = data["size"]
            self.direction: float = data["direction"]
            self.draggable: bool = data["draggable"]
            self.rotationStyle: str = data["rotationStyle"]

        self.variables: dict[str, Variable] = {} # Y | Filled in later
        self.lists: dict[str, List] = {} # Y | Filled in later
        self.costumes: dict[str, Costume] = [] # Y | Filled in later
        self.blocks: dict[str, Block] = {} # Y | Filled in later
        self.sounds = [] # X | Filled in later
        self.broadcasts = {} # X | Filled in later
        
        self.comments = {} # In TODO


        for raw_var in data["variables"]:
            self.variables[raw_var] = Variable(data["variables"][raw_var])
        
        for raw_list in data["lists"]:
            self.lists[raw_list] = Variable(data["lists"][raw_list])

        for raw_block in data["blocks"]:
            self.blocks[raw_block] = Block(data["blocks"][raw_block])

        # print(data["costumes"])
        for raw_costume in data["costumes"]:
            self.costumes.append(Costume(raw_costume, self.isStage))

    def __str__(self) -> str:
        o = "Target:"
        o += f"\n\tisStage = {self.isStage}"
        o += f"\n\tname = {self.name}"
        o += f"\n\tcurrentCostume = {self.currentCostume}"
        o += f"\n\tvolume = {self.volume}"
        o += f"\n\tlayerOrder = {self.layerOrder}"
        
        if self.isStage:
            o += f"\n\ttempo = {self.tempo}"
            o += f"\n\tvideoTransparency = {self.videoTransparency}"
            o += f"\n\tvideoState = {self.videoState}"
            o += f"\n\ttextToSpeechLanguage = {self.textToSpeechLanguage}"
        else:
            o += f"\n\tvisible = {self.visible}"
            o += f"\n\tx = {self.x}"
            o += f"\n\ty = {self.y}"
            o += f"\n\tsize = {self.size}"
            o += f"\n\tdirection = {self.direction}"
            o += f"\n\tdraggable = {self.draggable}"
            o += f"\n\trotationStyle = {self.rotationStyle}"

        o += f"\n\tvariables = {str_all(self.variables)}"
        o += f"\n\tlists = {str_all(self.lists)}"
        o += f"\n\tcostumes = {str_all(self.costumes)}"
        o += f"\n\tblocks = {str_all(self.blocks)}"
        o += f"\n\tsounds = {self.sounds}"
        o += f"\n\tbroadcasts = {self.broadcasts}"

        return o

class ScratchProject:
    def __init__(self, file_path: str) -> None:
        self._json_data = jn.load(open(file_path))
        self._file_path = file_path
        self.targets: list[ProjectTarget] = []
        self.monitors = []
        self.extensions = []
        
        self.meta = {
            "semver": None,
            "vm": None,
            "agent": None,
            "platform": {
                "name": None,
                "url": None
            }
        }
    
    def load(self) -> None:
        self.meta = self._json_data["meta"]
        self.extensions = self._json_data["extensions"]
        self.monitors = self._json_data["monitors"]

        for target in self._json_data["targets"]:
            self.targets.append(ProjectTarget(target))

    def compile(self, path: str) -> None:
        pass