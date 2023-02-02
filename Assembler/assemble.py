# Jesal Gandhi, Dhihan Ahmed
# CS382 Project 2: Assembler
# I pledge my honor that I have abided by the Stevens Honor System.

from os import listdir

def main():
    instruction_set = {
        "PL":"01",
        "MI":"00",
        "LD": "10"
    }

    # check that nsl file exists in directory
    nsl_file = list(filter(lambda i: i[-3:] == "nsl", listdir()))
    if not nsl_file: 
        print("No .nsl file is found. Please place a .nsl file in this directory.")
        return 1

    # retrieve instructions + data from instructions.nsl and place 
    # into their own respective lists
    instruction_list = []
    data_list = []
    
    # data flag, which is initally 0
    d = 0

    # open the instructions.nsl file
    with open(nsl_file[0]) as f:
        for line in f:
            
            # goto next iteration if .text is detected
            if line.strip() == ".text":
                continue
                
            # goto next iteration and enable d flag if .data is detected
            elif line.strip() == ".data":
                d = 1
                continue
                
            # if d flag not detected, line is an instruction
            elif d == 0:
                instruction_list.append(line.strip())
                
            # otherwise, line is a byte of data
            else:
                try:
                    data_list.append(int(line.strip()))
                except ValueError:
                    data_list.append(int(ord(line.strip())))
    f.close()

    # convert data_list to its hex values
    data_list = list(map(lambda x: hex(x)[2:].zfill(2), data_list))

    # open both memory images at the same time to write
    with open('data_mem_img', 'w') as f:
        with open('instruction_mem_img', 'w') as f2:

            # write header to data_mem_img file
            f.write("v3.0 hex words addressed")
            f.write("\n")
        
            # write header to instruction_mem_img file
            f2.write("v3.0 hex words addressed")
            f2.write("\n")

            # keep iterating until you have reached >256 instructions
            address_count = 0
            while address_count < 256:
                
                # append address and colon onto both files
                f.write(("{0:0>2x}".format(address_count)))
                f.write(": ")
                f2.write(("{0:0>2x}".format(address_count)))
                f2.write(": ")
                
                instruction_count = 0
                instruction_count2 = 0

                # while data_list not empty:
                while data_list:
                    # break if you reach >16 instructions on single line
                    if instruction_count >= 16:
                        break
                        
                    # write the data at beginning of data_list onto f, and space
                    f.write(data_list[0])
                    f.write(" ")
                    
                    # pop that data from data_list
                    data_list.pop(0)
                    
                    # increment the instruction_count by 1
                    instruction_count += 1

                # append 00's onto rest of memory row if it is not yet full
                while instruction_count < 16:
                    f.write("00 ")
                    instruction_count += 1

                # check that instruction_list not empty
                while instruction_list:
                    
                    # break if there is not enough room on current address
                    if instruction_count2 >= 16:
                        break

                    # initialize a binary buffer
                    bin_buffer = ""

                    # split the instruction into list using  "`" as delimiter
                    instruction = instruction_list[0].strip().split("`")

                    # append binary of mnemonic to bin_buffer
                    bin_buffer += instruction_set[instruction[0]]

                    # append operands of instruction onto bin_buffer
                    for i in range(1, len(instruction)):
                        bin_buffer += format(int(instruction[i][1:]), 'b').zfill(2) 

                    # append hex value of instruction into img file
                    f2.write(("{0:0>2x}".format(int(bin_buffer, 2))))
                    f2.write(" ")

                    # increment instruction_count of current memory row
                    instruction_count2 += 1

                    # dequeue the instruction you just wrote to img file from list
                    instruction_list.pop(0)

                # append 00's onto rest of memory row if it is not yet full
                while instruction_count2 < 16:
                    f2.write("00 ")
                    instruction_count2 += 1

                # increment the address_count by 16 (len of each row) + write newline    
                address_count += 16
                f.write("\n")
                f2.write("\n")

                
    f2.close()

    print("Successfully wrote instructions to image file!")
    

main()