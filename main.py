from scratch_src import massStorage
import scratch_src as scratch

def command(block: scratch.Block) -> tuple[tuple[str | None, int | None], scratch.BlockId, list[str | None]]:
    return (
        block.opcode.tokenize(), 
        block.id,
        [i.value for i in block.inputs.values()]
    )

if __name__ == "__main__":
    massStorage.load_opcodes("./assets/opcodes.json")
    project = scratch.ScratchProject(
        "./Projects/Loop/project.json"
    )

    project.load()
    
    sprite = project.targets[1]
    blocks = sprite.blocks
    starts = sprite.roots
    branch = sprite.branches[starts[0]]

    cmds = {}
    program = {}

    for parent_id, block in branch.branch.items():
        cmds[parent_id] = command(
            branch.all_blocks[parent_id]
        )
        for child_id in block:
            cmds[child_id] = command(
                branch.all_blocks[child_id]
            )
            
    for block_id, cmd in cmds.items():
        print(f"{block_id} : {cmd}")


    tab_level = 0
    compiled = {}

    for name, programs in program.items():
        compiled[name] = ""
        for cmd in programs:
            compiled[name] += '\t'*cmd[1] + cmd[0] + '\n'
    
    for name, code in compiled.items():
        with open("./compiled/generated.py", "w") as f:
            f.write(f"# Thread {name}\n\n")
            f.write(code)

            f.write("\nif __name__ == \"__main__\":\n\tmain()")

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