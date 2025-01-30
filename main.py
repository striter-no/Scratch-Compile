import scratch_src as scratch

def get_root(block_from: str, blocks: dict[str, scratch.Block]):
    if blocks[block_from].parent is None:
        return block_from
    
    root = get_root(blocks[block_from].parent, blocks)
    return root

if __name__ == "__main__":
    project = scratch.ScratchProject(
        "./Project/Loop/project.json"
    )

    project.load()
    
    sprite = project.targets[1]
    
    blocks = sprite.blocks
    cmds = {}
    program = {}

    for name, block in blocks.items():
        cmds[name] = (block.opcode, block.parent, [i.value for i in block.inputs.values()])
    
    tab_level = 0
    for name, cmd in cmds.items():
        
        print(name, cmd)

        if cmd[1] is None:
            program[name] = []

        if cmd[0] == "event_whenflagclicked":
            program[get_root(name, blocks)].append(
                ("def main():", tab_level)
            )
            tab_level += 1
        elif cmd[0] == "looks_say":
            program[get_root(name, blocks)].append(
                ("print(f\"{[" + ','.join([f'"{i}"' for i in cmd[2]]) + "]}\")", tab_level)
            )
    
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