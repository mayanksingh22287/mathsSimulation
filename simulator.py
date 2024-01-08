#Assembly:
#var X
#mov R1 $10
#mov R2 $100
#mul R3 R2 R1
#st R3 X
#hlt

#Binary file:
#0001000100001010
#0001001001100100
#0011000011010001
#0010101100000101
#1101000000000000

#1byte=8bits, 2 byte=16 bits ,Total memory size=256 bytes.

import assembler
total_memory_size = 256  # Total memory size in bytes
    
# Memory allocation sizes
initial_instruction_memory_size =remaining_instruction_memory_size= 128 #initial
initial_data_memory_size = remaining_data_memory_size=64 #initial
initial_stack_memory_size =remaining_stack_memory_size= 32 #initial 

# Calculate remaining memory size
initial_remaining_memory_size=remaining_remaining_memory_size= total_memory_size - initial_instruction_memory_size - initial_data_memory_size - initial_stack_memory_size

# Memory division
#memory_allocation = {
    #'Instruction Memory': initial_instruction_memory_size,
    #'Data Memory': initial_data_memory_size,
    #'Stack Memory': initial_stack_memory_size,
    #'Remaining Memory': remaining_memory_size
#}

# Display memory allocation
#for memory_type, memory_size in memory_allocation.items():
    #print(f"{memory_type}: {memory_size} bytes"

#assembler.op_inst->dictionary of opcodes(operation codes)
#assembler.reg->dictionary of register addresses
#assembler.reg_list-> list of registers
#assembler.operand_list->list of operations
#assembler.var_dict->dictionay specifies address pointed by variables
#assembler.mem_add_dict->dictionary containing address of each line of assembly code.

#-----------------------------------------------
#TOTAL_MEMORY_ARRAY
#-----------------------------------------------
l=[bin(i)[2:] for i in range(0,128)]
zero='0'
for i in range(0,len(l)):
    l[i]=zero*(7-len(l[i]))+l[i]

MEMORY=dict()
for i in range(0,128):
    MEMORY[l[i]]="0000000000000000"
#------------------------------------------------
#self.REGISTERS
#------------------------------------------------
REGISTERS={'000':"0000000000000000",'001':"0000000000000000",'010':"0000000000000000",'011':"0000000000000000",
           '100':"0000000000000000",'101':"0000000000000000",'110':"0000000000000000",'111':"0000000000000000"}
#------------------------------------------------
f1=open("Binary_file.txt",'r')
Prog_Counter=0
#Half_of_the memory is instruction memory
Memory_addresses=list(MEMORY.keys())
while(True):
    lines=f1.readline()
    if (not lines) or (remaining_instruction_memory_size<0):
        break
    MEMORY[Memory_addresses[(initial_instruction_memory_size)-(remaining_instruction_memory_size)]]=lines[0:len(lines)-1]
    remaining_instruction_memory_size-=1

#print(assembler.var_dict)

'''print(MEMORY)
print("\n\n")
print(REGISTERS)'''
#------------------------------------------------
class Simulator:
    def __init__(self,MEMORY,REGISTERS):
        self.Program_counter = "0000000"
        self.HALTED = False
        self.MEM=MEMORY
        self.REGISTERS=REGISTERS

    def fetch_inst(self):
        return self.MEM[self.Program_counter]

    def update_PC(self, new_PC):
        self.Program_counter = new_PC

    def return_MEMORY(self):
        return self.MEM

    def return_REGISTERS(self):
        return self.REGISTERS

    def return_PC(self):
        return self.Program_counter

    def decimal_to_binary(self,decimal_num):
        binary_num = bin(decimal_num)[2:]  # Convert decimal to binary string
        binary_num = binary_num.zfill(16)  # Pad with leading zeros to make it 16 bits
        return binary_num

    def binary_to_decimal(self,binary_num):
        decimal_num = int(binary_num, 2)
        return decimal_num

    def xor_binary(self,binary_num1, binary_num2):
        if len(binary_num1) != 16 or len(binary_num2) != 16:
            raise ValueError("Both binary numbers should be 16 bits long.")
    
        result = ""
        for bit1, bit2 in zip(binary_num1, binary_num2):
            if bit1 == bit2:
                result += "0"
            else:
                result += "1"
    
        return result

    def or_binary(self,binary_num1, binary_num2):
        if len(binary_num1) != 16 or len(binary_num2) != 16:
            raise ValueError("Both binary numbers should be 16 bits long.")

        result = ""
        for bit1, bit2 in zip(binary_num1, binary_num2):
            if bit1 == "1" or bit2 == "1":
                result += "1"
            else:
                result += "0"

        return result

    def and_binary(self,binary_num1, binary_num2):
        if len(binary_num1) != 16 or len(binary_num2) != 16:
            raise ValueError("Both binary numbers should be 16 bits long.")

        result = ""
        for bit1, bit2 in zip(binary_num1, binary_num2):
            if bit1 == "1" and bit2 == "1":
                result += "1"
            else:
                result += "0"

        return result

    def right_shift_binary(self,binary_num, shift_num):
        if len(binary_num) != 16 or len(shift_num) != 7:
            raise ValueError("The binary number should be 16 bits long and the shift number should be 7 bits long.")

        shift_amount = int(shift_num, 2)
        result = binary_num[-shift_amount:] + "0" * shift_amount

        return result

    def left_shift_binary(self,binary_num, shift_num):
        if len(binary_num) != 16 or len(shift_num) != 7:
            raise ValueError("The binary number should be 16 bits long and the shift number should be 7 bits long.")

        shift_amount = int(shift_num, 2)
        result = "0" * shift_amount + binary_num[:-shift_amount]

        return result

    def divide_binary(self,dividend, divisor):
        if len(dividend) != 16 or len(divisor) != 16:
            raise ValueError("Both dividend and divisor should be 16 bits long.")
    
        quotient = ""
        remainder = dividend
    
        while len(remainder) >= len(divisor):
            # Find the leftmost position of divisor in remainder
            index = len(remainder) - len(divisor)
        
            # Subtract divisor from the leftmost position in remainder
            subtraction = ""
            for i in range(len(remainder)):
                if i == index:
                    subtraction += divisor
                else:
                    subtraction += "0"
        
            # Perform binary subtraction
            difference = ""
            carry = 0
            for bit1, bit2 in zip(remainder, subtraction):
                xor = int(bit1) ^ int(bit2) ^ carry
                difference += str(xor)
                carry = (int(bit1) & int(bit2)) | (int(bit1) & carry) | (int(bit2) & carry)
        
            # Update remainder with the difference
            remainder = difference.lstrip("0")
        
            # Append 1 or 0 to quotient based on carry value
            if carry == 0:
                quotient += "1"
            else:
                quotient += "0"
    
            # Fill the remaining bits in quotient with zeros
            quotient += "0" * (16 - len(quotient))
    
            return quotient, remainder

    def bitwise_not(self,binary_number):
        """Performs the NOT operation on a 16-bit binary number.

           Args:
                binary_number (str): The 16-bit binary number to apply the NOT operation to.

           Returns:
                str: The resulting binary number after applying the NOT operation.
        """
        # Convert the binary number to a list of characters
        binary_list = list(binary_number)

        # Apply the NOT operation by flipping each bit
        for i in range(len(binary_list)):
            if binary_list[i] == '0':
                binary_list[i] = '1'
            else:
                binary_list[i] = '0'

        # Convert the list back to a string and return the result
        return ''.join(binary_list)

    def Set_FLAG(self,flag_no):
        s=""
        for i in range(0,len(self.REGISTERS["111"])):
            if(i ==11+flag_no):
                s+="1"
            else:
                s+=self.REGISTERS["111"][i]
                
        self.REGISTERS["111"]=s

    def float_to_binary(number):
        # Check for special cases
        if number == 0.0:
            return '0' * 8
        elif number == float('inf'):
            return '1' * 8

        # Convert the number to binary representation
        binary = ''

        # Determine the sign bit (always positive in this case)
        binary += '0'

        # Convert the absolute value of the number to binary
        absolute_value = abs(number)

        # Determine the exponent and adjust the number accordingly
        exponent = 0
        while absolute_value >= 2.0:
            absolute_value /= 2.0
            exponent += 1

        # Convert the mantissa to binary
        mantissa = absolute_value - 1.0
        mantissa_binary = ''
        for _ in range(5):
            mantissa *= 2.0
            if mantissa >= 1.0:
                mantissa_binary += '1'
                mantissa -= 1.0
            else:
                mantissa_binary += '0'

        # Convert the exponent to binary
        exponent_binary = bin(exponent)[2:].zfill(3)

        # Combine the mantissa and exponent to form the final binary representation
        binary += mantissa_binary + exponent_binary

        # Pad with zeros if the binary representation is shorter than 8 bits
        binary = binary.ljust(8, '0')

        return binary


    def binary_to_float(binary):
        # Extract the mantissa and exponent from the binary representation
        mantissa_binary = binary[1:6]
        exponent_binary = binary[6:]

        # Convert the mantissa to decimal
        mantissa = 1.0
        for i in range(5):
            if mantissa_binary[i] == '1':
                mantissa += 1.0 / (2 ** (i + 1))

        # Convert the exponent to decimal
        exponent = int(exponent_binary, 2)

        # Calculate the final floating-point number
        number = mantissa * (2 ** exponent)

        # Check if the number is negative (it shouldn't be in this format)
        if binary[0] == '1':
            number *= -1

        return number


    def Execute_Engine(self):
        while(not self.HALTED):
            instruction=self.fetch_inst()
            op_code=instruction[0:5]
            if op_code not in ["01111","11100","11101","11111"]:
                REGISTERS["111"]="0000000000000000"
            if op_code!="11010":
                print(f"{self.Program_counter}",end="        ")
            if(op_code in ["00000","00001","00110","01010","01011","01100","10000","10001"]):
                #ADD,SUB,MUL,XOR,OR,AND
                #3-register_type
                reg1=instruction[7:10]
                reg2=instruction[10:13]
                reg3=instruction[13:]
                if(op_code=="00000"):
                    #ADD
                   result=self.binary_to_decimal(self.REGISTERS[reg2])+self.binary_to_decimal(self.REGISTERS[reg3])
                   if(result<=2**16-1):
                       self.REGISTERS[reg1]=self.decimal_to_binary(result)
                   else:
                       self.Set_FLAG(1)
                       
                   new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                   self.update_PC(new_PC)
                   
                elif(op_code=="00001"):
                    #SUB
                   result=self.binary_to_decimal(self.REGISTERS[reg2])-self.binary_to_decimal(self.REGISTERS[reg3])
                   if(result<=2**16-1 and result>=0):
                       self.REGISTERS[reg1]=self.decimal_to_binary(result)
                   else:
                       self.Set_FLAG(1)
                       
                   new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                   self.update_PC(new_PC)
                   
                elif(op_code=="00110"):
                    #MUL
                    result=self.binary_to_decimal(self.REGISTERS[reg2])*self.binary_to_decimal(self.REGISTERS[reg3])
                    if(result<=2**16-1 and result>0):
                       self.REGISTERS[reg1]=self.decimal_to_binary(result)
                    else:
                       self.Set_FLAG(1)
                       
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="01010"):
                    #XOR
                    self.REGISTER[reg1]=self.xor_binary(self.REGISTERS[reg2],self.REGISTERS[reg3])
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="01011"):
                    #OR
                    self.REGISTER[reg1]=self.or_binary(self.REGISTERS[reg2],self.REGISTERS[reg3])
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="01100"):
                    #AND
                    self.REGISTER[reg1]=self.and_binary(self.REGISTERS[reg2],self.REGISTERS[reg3])
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)

                elif(op_code=="10000"):
                    #F_Addition
                    result=self.binary_to_float(self.REGISTERS[reg2][8:])+self.binary_to_float(self.REGISTERS[reg3][8:])
                    if(result<=31 and result>0.0625):
                        self.REGISTERS[reg1]="00000000"+self.float_to_binary(result)
                    else:
                        self.Set_FLAG(1)
                       
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)

                elif(op_code=="10001"):
                    #F_subtraction
                    result=self.binary_to_float(self.REGISTERS[reg2][8:])-self.binary_to_float(self.REGISTERS[reg3][8:])
                    if(result<=31 and result>0.0625):
                        self.REGISTERS[reg1]="00000000"+self.float_to_binary(result)
                    else:
                        self.Set_FLAG(1)
                       
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
            elif(op_code in ["00010","01000","01001","10010"]):
                #MOVE_IMM,RIGHT_SHIFT,LEFT_SHIFT
                #register and immediate type
                reg1=instruction[6:9]
                imm_val=instruction[9:]
                if(op_code=="00010"):
                    #MOVE_IMM
                    self.REGISTERS[reg1]=self.decimal_to_binary(self.binary_to_decimal(imm_val))
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="01000"):
                    #RIGHT_SHIFT
                    self.REGISTERS[reg1]=self.right_shift_binary(self.REGISTERS[reg1],imm_val)
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="01001"):
                    #LEFT_SHIFT
                    self.REGISTERS[reg1]=self.left_shift_binary(self.REGISTERS[reg1],imm_val)
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)

                elif(op_code=="10010"):
                    #Move_Float_immediate
                    self.REGISTERS[reg1]="00000000"+self.float_to_binary(self.binary_to_float(imm_val))
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
            elif(op_code in ["00011","00111","01101","01110"]):
                #MOVE_REG,DIV,NOT,CMP
                #2-registers
                reg1=instruction[10:13]
                reg2=instruction[13:]
                if(op_code=="00011"):
                    #MOVE_REG
                    self.REGISTERS[reg1]=self.REGISTERS[reg2]
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="00111"):
                    #DIV
                    if (reg2=="0000000000000000"):
                        self.REGISTERS["111"]["V"]="1"
                        self.REGISTERS["001"]="0"
                    else:
                        quo,rema=self.divide_binary(self.REGISTERS[reg1],self.REGISTERS[reg2])
                        self.REGISTERS["001"]=rema
                        self.REGISTERS["000"]=quo
                        
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="01101"):
                    #NOT
                    self.REGISTERS[reg1]=self.bitwise_not(self.REGISTERS[reg2])
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="01110"):
                    #CMP
                    val1,val2=self.REGISTERS[reg1],self.REGISTERS[reg2]
                    if (val1==val2):
                        self.Set_FLAG(4)
                    elif(val1>val2):
                        self.Set_FLAG(3)
                    else:
                        self.Set_FLAG(2)
                    
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
            elif(op_code in ["00100","00101"]):
                #LOAD,STORE
                #register and memory_address type
                reg1=instruction[6:9]
                memory_address=instruction[9:]
                if(op_code=="00100"):
                    #LOAD
                    self.REGISTERS[reg1]=self.MEM[memory_address]
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
                elif(op_code=="00101"):
                    #STORE
                    self.MEM[memory_address]=self.REGISTERS[reg1]
                    new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                    self.update_PC(new_PC)
                    
            elif(op_code in ["01111","11100","11101","11111"]):
                # JMP,JMP_L,JMP_G,JMP_E
                memory_address=instruction[9:]
                if(op_code=="01111"):
                    #JMP
                    new_PC=memory_address
                    self.update_PC(new_PC)
                    REGISTERS["111"]="0000000000000000"
                    
                elif(op_code=="11100"):
                    #JMP_L
                    if (self.REGISTERS["111"][13]=="1"):
                        new_PC=memory_address
                        self.update_PC(new_PC)
                    else:
                       new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                       self.update_PC(new_PC)
                    REGISTERS["111"]="0000000000000000"
                       
                elif(op_code=="11101"):
                    #JMP_G
                    if (self.REGISTERS["111"][14]=="1"):
                        new_PC=memory_address
                        self.update_PC(new_PC)
                    else:
                       new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                       self.update_PC(new_PC)
                    REGISTERS["111"]="0000000000000000"
                       
                elif(op_code=="11111"):
                    #JMP_E
                    if (self.REGISTERS["111"][15]=="1"):
                        new_PC=memory_address
                        self.update_PC(new_PC)
                    else:
                       new_PC=self.decimal_to_binary(self.binary_to_decimal(self.Program_counter)+1)[9:]
                       self.update_PC(new_PC)
                    REGISTERS["111"]="0000000000000000"
                
            elif(op_code=="11010"):
                #HALT
                self.HALTED=True
                
                print(f"{self.Program_counter}",end="        ")
                print(f"{REGISTERS['000']} {REGISTERS['001']} {REGISTERS['010']} {REGISTERS['011']} {REGISTERS['100']} {REGISTERS['101']} {REGISTERS['110']} {REGISTERS['111']}")
            if op_code!="11010":
                print(f"{REGISTERS['000']} {REGISTERS['001']} {REGISTERS['010']} {REGISTERS['011']} {REGISTERS['100']} {REGISTERS['101']} {REGISTERS['110']} {REGISTERS['111']}")

#Main Code
Simulator1=Simulator(MEMORY,REGISTERS)
Simulator1.Execute_Engine()
MEM=Simulator1.return_MEMORY()
values=MEM.values()
for memory_lines in values:
    print(memory_lines)
    
