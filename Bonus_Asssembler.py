import sys
global new_man
global new_exp
lines=sys.stdin.readlines()
def converter(s):
    y=s[1:]
    #num_lst seperated at . 11.01=[11,01]
    num_lst=y.split(".")
    #print(num_lst)
    num1=int(num_lst[0])
    #list of binary of integer part
    bin_int=[]
    while(num1//2!=0):
        bin_int.append(num1%2)
        num1=num1//2
    bin_int.append(num1%2)
    bin_int.reverse()
    #print("binary of int",bin_int)
    num2=(num_lst[1])
    num2=str(".")+num2
    num2=float(num2)
    #print("Number after point",num2)
    bin_deci=[]
    while(True):
        num2=num2%1
        num2=num2*2
        a=int(num2)
        bin_deci.append(a)
        if(num2%1==0.0):
            break
    #print("Bin of deci",bin_deci)
    cnt=0
    for i in bin_deci:
        if(i!=1):
            cnt+=1
        else:
            break
    if (cnt>=3):
        print("more bits used than the assigned")
        return False; 
    else:
        y=len(bin_int)-1
        exp=3+y
        lst4=bin_int+bin_deci
        lst4.remove(lst4[0])
        lst5=[]
        #print(exp)
        while(exp//2!=0):
            lst5.append(exp%2)
            exp=exp//2
        lst5.append(exp%2)
        lst5.reverse()
        #print("Print 5",lst5)
        exponent=""
        for i in range(0,len(lst5)):
            exponent+=str(lst5[i])
        mantissa=""
        #print("ist4",lst4)
        for i in range(0,len(lst4)):
            mantissa+=str(lst4[i])
        mantissa=int(mantissa)
        exponent=int(exponent)
        #print(mantissa,exponent)
        #for leading zero removal
        global new_man
        new_man=""
        global new_exp
        new_exp=""
        if(len(str(exponent))>3 or len(str(mantissa))>5):
            print("more bits used than the assigned")
            return False    
        else:
            new_man=str(mantissa)+((5-len(str(mantissa)))*"0")
            new_exp=str(exponent)+((3-len(str(exponent)))*"0")
            print(new_exp,new_man)
            return True

def check(lines):
    global bool
    bool=True
    whole_lst=[]
    for i in lines:
        word=i.split()
        for j in range(0,len(word)):
            if(word[0]=="jmp" or word[0]=="jlt" or word[0]=="jgt" or word[0]=="je"):
                continue
            else:
                whole_lst.append((word[j]))
    var_list=[]
    var_line_no=0
    #print(whole_lst)
    for i in range(0,len(lines)):
        word=lines[i].split()
        if(word[0]!="var"):
            var_line_no=i+1
            break
        if(len(word)!=2):
            print(f"Error in line 1 var is not defined correctly\n")
            bool=False
        var_list.append(word[1])
    reg_list=["R0","R1","R2","R3","R4","R5","R6","FLAGS"]
    operand_list=["var","add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt","addf","subf","movf","andi","nandi","jz","ldi","mulf"]
    for i in range(0,len(lines)):
        word=lines[i].split()
        z=i+1
        #print(word)
        if(i>var_line_no and word[0]=="var"):
            print(f"Error in line {z} : Var must be declared at begin\n")
            bool=False
        elif(word[0] not in operand_list and word[0][-1]!=":"):
            print(f"Error in line {z} : Invalid operand\n")
            bool=False
        elif(word[0]=="add" or word[0]=="sub" or word[0]=="mul" or word[0]=="xor" or word[0]=="or" or word[0]=="and" or word[0]=="addf" or word[0]=="subf" or word[0]=="mulf" ):
            if(len(word)!=4):
                print(f"Error in line {z} : {word[0]} must contain 3 parameters.\n")
                bool=False
            elif(word[1][0]!="R" or word[2][0]!="R" or word[3][0]!="R"):
                print(f"Error in line {z} : {word[3]} is not a register\n")
                bool=False
            elif((int(word[1][1::])>6) or (int(word[2][1::])>6) or (int(word[3][1::])>6)):
                print(f"Error in line {z} : {word[3]} is not a valid register\n")
                bool=False
        elif(word=="andi" or word=="nandi" or word=="ldi"):
            if(len(word!=3)):
                print(f"Error in line {z} : {word[0]} must contain 3 parameters.\n")
                bool=False
            elif(word[1][0]!="R"and word[1][0]!="F"):
                print(f"Error in line {z} : {word[3]} is not a register\n")
                bool=False
            elif(word[2][0]!="$" and (int(word[2][1::])>127)):
                print(f"Error in line {z} : {word[3]} imm value out of range\n")
                bool=False
        elif(word[0]=="mov" or word[0]=="ld" or word[0]=="st" or word[0]=="div" or word[0]=="rs" or word[0]=="ls" or word[0]=="not" or word[0]=="cmp" or word[0]=="jz"):
            if(len(word)!=3):
                print(f"Error in line {z} : {word[0]} must contain 2 parameters.\n")
                bool=False
            elif(word[0]=="ld" and (word[2] not in var_list)):
                print(f"Error in line {z} : the variable {word[2]} is not defined\n")
                bool=False
            elif(word[0]=="ld" and (word[1] not in reg_list)):
                print(f"Error in line {z} : the variable {word[1]} is not a correct register\n")
                bool=False
            elif(word[0]=="st" and (word[2] not in var_list)):
                print(f"Error in line {z} : the variable {word[2]} is not defined\n")
                bool=False
            elif(word[0]=="st" and (word[1] not in reg_list)):
                print(f"Error in line {z} : the variable {word[1]} is not a correct register\n")
                bool=False
            elif(word[0]=="mov" and (word[1] not in reg_list)):
                print(f"Error in line {z} : the variable {word[1]} is not a valid register\n")
                bool=False
            elif(word[0]=="mov" and (word[2][0]!="R" and word[2][0]!="F") and (word[2][0]!="$")):
                print(f"Error in line {z} the variable {word[2]} is not defined\n")
                bool=False
            elif(word[0]=="mov" and (word[2] not in reg_list) and (word[2][0]!="$")):
                print(f"Error in line {z} the variable {word[1]} is not a valid register\n")
                bool=False
            elif(word[0]=="mov" and (word[2][0]!="R" and word[2][0]!="F") and (word[2][0]=="$")):
                if(int(word[2][1::])>127 or int(word[2][1::])<0):
                    print(f"Error in line {z} : the imm value out of range\n")
                    bool=False
            elif(word[0]=="ld" and (word[2] not in var_list)):
                print(f"Error in line {z} : the variable {word[2]} is not defined\n")
                bool=False
            elif(word[0]=="jz" and (word[1] not in reg_list)):
                print(f"Error in line {z} : the variable {word[1]} is not a correct register\n")
                bool=False
            elif(word[0]=="jz" and (word[2] not in var_list)):
                print(f"Error in line {z} : the variable {word[2]} is not defined\n")
                bool=False
        #condition same as mov but from here for movf
        elif(word[0]=="movf" and (word[2][0]=="$")):
            if(("." not in word[2])):
                print(f"Error in line {z} : not a floating point number\n")
                bool=False
            if("-" in word[2]):
                print(f"Error in line {z}: not a valid floating point number\n")
                bool=False
            else:
                bool=converter(word[2])
                if(bool==False):
                    print(f"Error in line {z}: not a valid floating point number\n")
        elif(word[0]=="jmp" or word[0]=="jlt" or word[0]=="jgt" or word[0]=="je"):
            if(len(word)!=2):
                print(f"Error in line {z} : {word[0]} must contain 1 parameters.\n")
                bool=False 
            elif(word[1]+":" not in whole_lst):
                print(f"Error in line {z} : No Label named {word[1]}\n")
                bool=False
        elif("hlt" not in whole_lst):
            print("Error hlt is not used\n")
            bool=False
            break
        elif("hlt" in whole_lst):
            if(whole_lst.index("hlt")!=len(whole_lst)-1):
                z=i+2
                print(f"Error in line {z}: No statement to execute after hlt\n")
                bool=False
                break
    return bool
if(check(lines)):
    #for giving the each line instruction a memory location
    #important is that if variable is defined then allocate memory at last after giving instruction memory.
    def increment_binary(binary):
        # Remove leading zeros
        binary = binary.lstrip('0')
        # Check if the binary string is empty after removing leading zeros
        if len(binary) == 0:
            return '1'
        # Convert the binary string to a list of characters
        bin_lst = list(binary)
        # Reverse the binary list
        bin_lst.reverse()
        # Perform binary addition on the list
        carry = 1
        for i in range(len(bin_lst)):
            if carry == 0:
                break
            if bin_lst[i] == '0':
                bin_lst[i] = '1'
                carry = 0
            else:
                bin_lst[i] = '0'
        
        # If there is still a carry bit, add it as a new digit
        if carry == 1:
            bin_lst.append('1')
        # Reverse the list back and convert it to a string
        bin_lst.reverse()
        return ''.join(bin_lst)

    # it will be used to convert the imm value to binary
    def to_binary(number):
        if number > 1:
            return to_binary(number//2) + str(number % 2)
        else:
            return str(number % 2)

    #main
    k="0000000"
    cnt_var_loc=0; #for counting var address as we have to give address to them at last
    var_dict={}
    len_inst=0
    #this loop is to calculate no of variables declared
    for i in lines:
        word=i.split()
        if word==[]:
            continue
        if(word[0]=="var"):
            var_dict[word[1]]="0"
            cnt_var_loc+=1
            len_inst+=1
        else:
            len_inst+=1
    var=len_inst-cnt_var_loc
    #this loop is to count the number of instructions and updating the location
    while(var!=1):
        k=increment_binary(k)
        var=var-1
    #loop is to store the var location in list 
    var_loc_list=[]
    while(cnt_var_loc!=0):
        k=increment_binary(k)
        #this computation is to make that occupy 7 bits in memory
        k=((7-len(k))*"0")+k
        var_loc_list.append(k)
        cnt_var_loc-=1
    #print("variable loc list is:",var_loc_list)
    #to store a variable in a corresponding dictionary
    for i in range(0,len(lines)):
        word=lines[i].split()
        if(word==[]):
            continue
        elif(word[0]=="var"):
            var_dict[word[1]]=var_loc_list[i]
    #print("the var_dict is : ",var_dict)
    #for storing the address in a corresponding dictionary

    #for more help in op instructions can see inn the CO project final pdf
    op_inst = {"add": "00000", "sub": "00001", "mov_imm": "00010", "mov_reg": "00011", "ld": "00100", "st": "00101", "mul": "00110", "div": "00111",
    "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100", "not": "01101", "cmp": "01110", "jmp": "01111",
    "jlt": "11100", "jgt": "11101", "je": "11111", "hlt": "11010","addf": "10000","subf":"10001","movf":"10010","andi":"10011","nandi":"10100",
    "jz":"10101","ldi":"10110","mulf":"10111"}
    #registers opcodes
    reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
    #dont convert the 0000 in int ,as it is giving error as 0001 and 1 are same so we need to use string only.

    #The main code will start from here the above portion is just the base of the question
    #and for information comments are in the code 
    mem_add_dict={}
    k="00000";count=0
    for i in lines:
        word=i.split()
        if word==[]:
            continue
        if(word[0]=="var"):
            continue
        if(word[0] not in mem_add_dict.keys()):
            if(count!=0):
                k=increment_binary(k)
                k=((7-len(str(k)))*"0")+str(k)
            count+=1
            k=((7-len(str(k)))*"0")+str(k)
            if(word[0][-1]==":"):
                mem_add_dict[word[0][:-1:]]=k
            elif(word[0][0]=="."):
                mem_add_dict[word[0][1::]]=k
            else:
                mem_add_dict[word[0]]=k
        else:
            k=increment_binary(k)
            k=((7-len(str(k)))*"0")+str(k)
    #code
    for i in range(0,len(lines)): #taking range because we have to also keep in mind about the error in which line
        word=lines[i].split()
        #print(word)
        if(word[0][-1]==":"):
            word.pop(0)
        if(word!=[]):
            #check for var
            if(word[0]=="var"):
                continue
            #checking for load 
            if(word[0]=="ld"):
                print(f"{op_inst['ld']}0{reg[word[1]]}{var_dict[word[2]]}\n")
            #check for addition
            if(word[0]=="add"):
                print(f"{op_inst['add']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #check for float addition
            if(word[0]=="addf"):
                print(f"{op_inst['addf']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #check for subtraction
            if(word[0]=="sub"):
                print(f"{op_inst['sub']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #check for float subtraction
            if(word[0]=="subf"):
                print(f"{op_inst['subf']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #check for multiplication
            if(word[0]=="mul"):
                print(f"{op_inst['mul']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #for floating point multiplication
            if(word[0]=="mulf"):
                print(f"{op_inst['mulf']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #check for store
            if(word[0]=="st"):
                print(f"{op_inst['st']}0{reg[word[1]]}{var_dict[word[2]]}\n")
            #check for jump if re value is 1
            if(word[0]=="jz"):
                try:
                    print(f"{op_inst['jz']}0{reg[word[1]]}{var_dict[word[2]]}\n")
                except:
                    print("No memory at such memory location")
            #check for division
            if(word[0]=="div"):
                print(f"{op_inst['div']}00000{reg[word[1]]}{reg[word[2]]}\n")
            #check for not
            if(word[0]=="not"):
                print(f"{op_inst['not']}00000{reg[word[1]]}{reg[word[2]]}\n")
            #check for compare
            if(word[0]=="cmp"):
                print(f"{op_inst['cmp']}00000{reg[word[1]]}{reg[word[2]]}\n")
            #check for xor
            if(word[0]=="xor"):
                print(f"{op_inst['xor']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #check for or
            if(word[0]=="or"):
                print(f"{op_inst['or']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #check for and
            if(word[0]=="and"):
                print(f"{op_inst['and']}00{reg[word[1]]}{reg[word[2]]}{reg[word[3]]}\n")
            #check hlt instruction
            if(word[-1]=="hlt"):
                print(f"{op_inst['hlt']}00000000000\n")
            #all imm cases are here
            if(word[0]=="rs" or (word[0]=="mov" and word[2][0]=="$") or word[0]=="ldi" or word[0]=="ls"or word[0]=="andi" or word[0]=="nandi"):
                word[-1]=word[-1][1::]
                num=((7-len(str(to_binary(int(word[-1])))))*"0") + str(to_binary(int(word[-1])))
                if(word[0]=="rs"):
                    print(f"{op_inst['rs']}0{reg[word[1]]}{num}\n")
                elif(word[0]=="ls"):
                    print(f"{op_inst['ls']}0{reg[word[1]]}{num}\n")
                elif(word[0]=="mov"):
                    print(f"{op_inst['mov_imm']}0{reg[word[1]]}{num}\n")
                elif(word[0]=="andi"):
                    print(f"{op_inst['andi']}0{reg[word[1]]}{num}\n")
                elif(word[0]=="nandi"):
                    print(f"{op_inst['nandi']}0{reg[word[1]]}{num}\n")
                elif(word[0]=="ldi"):
                    print(f"{op_inst['ldi']}0{reg[word[1]]}{num}\n")
            #float move (need to improve)
            if(word[0]=="movf"):
                print(f"{op_inst['movf']}{reg[word[1]]}{new_exp}{new_man}\n")
            if(word[0]=="mov" and (word[2][0] =="R" or word[2][0]=="F")):
                print(f"{op_inst['mov_reg']}00000{reg[word[1]]}{reg[word[2]]}\n")
            #all opcode to memory commands
            if(word[0]=="jmp"):
                print(f"{op_inst['jmp']}0000{mem_add_dict[word[1]]}\n")
            if(word[0]=="jlt"):
                print(f"{op_inst['jlt']}0000{mem_add_dict[word[1]]}\n")
            if(word[0]=="jgt"):
                print(f"{op_inst['jgt']}0000{mem_add_dict[word[1]]}\n")
            if(word[0]=="je"):
                print(f"{op_inst['je']}0000{mem_add_dict[word[1]]}\n")
