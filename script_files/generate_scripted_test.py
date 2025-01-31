import logs_for_script


#  [[0.455397367477417, 'self.drawbot.go_random_jump()'],

target_file = "scripted_test.py"

source_list = logs_for_script.temp_gesture_capture_list
print(source_list)

with open(target_file, 'w') as f:
    for inst in source_list:
        print(f"sleep({inst[0]})")
        f.write(f"sleep({inst[0]})\n")

        if len(inst) > 2:
            command = ""
            for var in inst[1:]:
                command += f"{var}, "
        else:
            command = inst[1]
        command += "\n"

        f.write(command)
        print(f"command: {command}")

f.close()



#
# with open(source_file, "r") as file:
#     with open(target_file, "w") as target:
#         for line in file:
#             for