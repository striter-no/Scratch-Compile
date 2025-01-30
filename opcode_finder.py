import scratch_src as scratch

if __name__ == "__main__":
    project = scratch.ScratchProject(
        "./Project/Hello world/3d_project.json"
    )

    project.load()
    
    with open("./opcodes.txt", "w") as f:
        opcodes = set()
        for target in project.targets:
            for name, block in target.blocks.items():
                opcodes.add(block.opcode)
        
        for opcode in opcodes:
            f.write(f"{opcode}\n")