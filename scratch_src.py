import json as jn

def list_str_all(inp_list: list) -> list[str]:
    return [str(i) for i in inp_list]

def dict_str_all(inp_dict: dict) -> dict:
    return {str(k): str(v) for k, v in inp_dict.items()}

class BlockId:
    def __init__(self, data: str) -> None:
        self._data = data

        self.id: str = data
    
    def __hash__(self) -> int:
        return hash(self._data)

    def __eq__(self, value) -> bool:
        return type(value).__name__ == "BlockId" and (self.id == value.id)

    def __str__(self) -> str:
        return f"{self.id}"

class Opcode:
    def __init__(self, data: (str | None) = None, module: (str | None) = None, full_str: (str | None) = None) -> None:
        self._data = {"value": data, "module": module, "full_str": full_str}

        if not (full_str is None):
            self.value: (str | None) = full_str
            self.module: (str | None) = full_str[:full_str.index('_')]
        else:
            self.value: (str | None) = data
            self.module: (str | None) = module

    def tokenize(self) -> tuple[(str | None), (int | None)]:
        return self.module, None if (self.value and self.module) is None else int(massStorage.opcodes[self.module].index(self.value))

    def __str__(self) -> str:
        return f"{self.module}_{self.value}"

class Costume:
    def __init__(self, data: dict, isStage: bool) -> None:
        self._data = data
        self.name: str = data["name"]
        self.dataFormat: str = data["dataFormat"]
        self.assetId: str = data["assetId"]
        self.md5ext: str = data["md5ext"]
        self.rotationCenterX: float = data["rotationCenterX"]
        self.rotationCenterY: float = data["rotationCenterY"]
        self.isStage = isStage
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
        if not self.isStage:
            o += f"\n\tbitmapResolution = {self.bitmapResolution}"
        
        return o

"""
Info from https://github.com/scratchfoundation/scratch-vm/blob/develop/test/unit/engine_adapter.js
"""
class Substack:
    def __init__(self, data: list):
        self._data = data
        self.branchShadowId: int = data[0]
        self.branchBlockId: BlockId = BlockId(data[1])
        self.value = None # For compability

"""
Info from https://github.com/scratchfoundation/scratch-vm/blob/develop/src/engine/scratch-blocks-constants.js
"""
class BlockType:
    def __init__(self, constant: int) -> None:
        self._data = constant
        self.constant: int = constant

        self.out_hex = constant == 1
        self.out_round = constant == 2
        self.out_square = constant == 3

"""
Info from https://github.com/scratchfoundation/scratch-vm/blob/develop/src/serialization/sb3.js
"""
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

class Field:
    def __init__(self, data: list, id: str) -> None:
        self._data = {"data": data, "id": id}
        
        self.name = id # name of argument
        self.value = data # link to actual data

class Input:
    def __init__(self, data: list) -> None:
        self._data = data
        
        self.output_shape: BlockType = BlockType(constant=data[0])
        self.outgoing_branch: (BlockId | None) = None
        self.value: (str | None) = None
        if len(data) == 2:
            self.input_type: VariableType = VariableType(constant=data[1][0])
            self.value = data[1][1]
        else:
            self.outgoing_branch = BlockId(data[1])

    def __str__(self) -> str:
        o = "Input:"
        o += f"\n\toutput_shape = {self.outgoing_branch}"
        o += f"\n\toutgoing_branch = {self.outgoing_branch}"
        if self.outgoing_branch is None:
            o += f"\n\tinput_type = {self.input_type}"

        o += f"\n\tvalue = {self.value}"

        return o

class Block:
    def __init__(self, data: dict, id: str) -> None:
        self._data = data

        self.opcode: Opcode = Opcode(full_str=data["opcode"])
        self.next: (BlockId | None) = BlockId(data["next"]) if data["next"] else None
        self.parent: (BlockId | None) = BlockId(data["parent"]) if data["parent"] else None
        self.shadow: bool = data["shadow"]
        self.topLevel: bool = data["topLevel"]

        self.isTop = False
        self.id = BlockId(id)

        if "x" in data:
            self.x: float = data["x"]
            self.y: float = data["y"]
            self.isTop = True

        self.fields: dict[str, Field] = {}
        self.inputs: dict[str, (Input | Substack)] = {} # Filled in later

        for name, raw_input in data["inputs"].items():
            if name.lower() == "substack":
                self.inputs[name] = Substack(raw_input)
            else:
                self.inputs[name] = Input(raw_input)
        
        for name, raw_field in data["fields"].items():
            self.fields[name] = Field(raw_field, name)

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

class Branch:
    def __init__(self, root: BlockId, blocks: dict[BlockId, Block]) -> None:
        self._data = {"root":root, "blocks": blocks}
        self.all_blocks = blocks
        
        self.branch: dict[BlockId, set[BlockId]] = {root: set()}

        for i in range(len(set(list(blocks.keys())))):
            for bid, block in blocks.items():
                parent = block.parent
                if parent is None:
                    continue
                
                if parent in self.branch:
                    self.branch[parent].add(bid)
                    if not (bid in self.branch):
                        self.branch[bid] = set()
            
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
        self.costumes: list[Costume] = [] # Y | Filled in later
        self.blocks: dict[BlockId, Block] = {} # Y | Filled in later
        self.sounds = [] # X | Filled in later
        self.broadcasts = {} # X | Filled in later
        
        self.comments = {} # In TODO

        for var_id in data["variables"]:
            self.variables[var_id] = Variable(data["variables"][var_id])
        
        for list_id in data["lists"]:
            self.lists[list_id] = List(data["lists"][list_id])

        for block_id in data["blocks"]:
            self.blocks[BlockId(block_id)] = Block(data["blocks"][block_id], block_id)

        for costume_id in data["costumes"]:
            self.costumes.append(Costume(costume_id, self.isStage))

        self.roots = self.find_roots(self.blocks)
        self.branches: dict[BlockId, Branch] = {
            root: Branch(root, self.blocks) for root in self.roots
        }

    def find_roots(self, blocks: dict[BlockId, Block]):
        start_points = set()

        for id, cmd in blocks.items():
            root = self.get_root(
                id,
                blocks
            )
            if not (root is None):
                start_points.add(root)

        return list(start_points)

    def get_root(self, block_from: (BlockId | None), blocks: dict[BlockId, Block]):
        if block_from is None:
            return None
        if blocks[block_from].parent is None:
            return block_from
        
        root = self.get_root(blocks[block_from].parent, blocks)
        return root

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

        o += f"\n\tvariables = {dict_str_all(self.variables)}"
        o += f"\n\tlists = {dict_str_all(self.lists)}"
        o += f"\n\tcostumes = {list_str_all(self.costumes)}"
        o += f"\n\tblocks = {dict_str_all(self.blocks)}"
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

class MassStorage:
    def __init__(self) -> None:
        self.opcodes: dict[str, list[str]] = {}
    
    def load_opcodes(self, path: str) -> None:
        self.opcodes = jn.load(open(path))

massStorage = MassStorage()