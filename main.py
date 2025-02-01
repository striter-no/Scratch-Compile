from scratch_src import massStorage
import scratch_src as scratch

if __name__ == "__main__":
    massStorage.load_opcodes("./assets/opcodes.json")
    project = scratch.ScratchProject(
        "./Projects/Loop/project.json"
    )

    project.load()
    
    sprite = project.targets[1]
    
    blocks = sprite.blocks
    cmds = {}
    program = {}

    for name, block in blocks.items():
        cmds[name] = (
            block.opcode.tokenize(), 
            block.id,
            [i.value for i in block.inputs.values()]
        )
    
    starts = sprite.roots
    branch = sprite.branches[starts[0]]

    print(scratch.list_str_all(starts))
    print(scratch.dict_str_all(branch.branch))

    for id, block in branch.branch.items():
        print(f"Parent: {id}")
        for i in block:
            print(f"\tchild: {i}")

    tab_level = 0
    for name, cmd in cmds.items():
        
        print(name, cmd)

        # if cmd[1] is None:
        #     program[name] = []

        # if cmd[0] == "event_whenflagclicked":
        #     program[get_root(name, blocks)].append(
        #         ("def main():", tab_level)
        #     )
        #     tab_level += 1
        # elif cmd[0] == "looks_say":
        #     program[get_root(name, blocks)].append(
        #         ("print(f\"{[" + ','.join([f'"{i}"' for i in cmd[2]]) + "]}\")", tab_level)
        #     )
    
    compiled = {}

    for name, programs in program.items():
        compiled[name] = ""
        for command in programs:
            compiled[name] += '\t'*command[1] + command[0] + '\n'
    
    for name, code in compiled.items():
        with open("./compiled/generated.py", "w") as f:
            f.write(f"# Thread {name}\n\n")
            f.write(code)

            f.write("\nif __name__ == \"__main__\":\n\tmain()")


# class Queue:
#     def __init__(self):
#         self.queue = []
    
#     def is_empty(self):
#         return len(self.queue) == 0

#     def put(self, value):
#         self.queue.append(value)
    
#     def pop(self):
#         if not self.is_empty():
#             return self.queue.pop(-1)
        
    
#     def get(self):
#         if not self.is_empty():
#             print(f"returning: {self.queue[-1]}")
#             return self.queue[-1]
        
#         return None