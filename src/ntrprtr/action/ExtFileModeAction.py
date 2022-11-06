from ntrprtr.action.ActionBase import ActionBase

class ExtFlagAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["endianess"] = "little"

    def process(self, action, _bytes):
        self._mergeConfig(action)

        bits = ""
        result = ""
        endianess = self._config["endianess"]

        if(endianess == "big"):
            bits = self._cnvrtr.hexToBin(_bytes.hex(" ")).rjust(16, "0")
        elif(endianess == "little"):
            b = self._cnvrtr.toLittleEndian(_bytes.hex(" "))
            bits = self._cnvrtr.hexToBin(b).rjust(16, "0")

        # Bit 15 - Bit 12
        filetypeBits = "".join(bits[i:i+4] for i in range(0, 4, 4))
        fileType = self.__getFileType(filetypeBits)
        # Bit 11 - Bit 09
        flagBits = "".join(bits[i:i+3] for i in range(4, 7, 3))
        flags = self.__getFlags(flagBits)
        # Bit 08 - Bit 00
        permissionBits = "".join(bits[i:i+9] for i in range(7, 16, 9))
        permissions = self.__getPermissions(permissionBits)
        # For better readability add a space between each 3 bits
        permissionBits = " ".join(permissionBits[i:i+3] for i in range(0, len(permissionBits), 3))

        fileTypeStr = "  File Type: " + filetypeBits + "\n             " + fileType 
        flagStr = "      Flags: " + flagBits + "\n             " + flags 
        permissionStr = "Permissions: " + permissionBits + "\n             " + permissions 
       
        result = fileTypeStr + "\n" +  flagStr + "\n" + permissionStr

        return result

    def __getFileType(self, bits):
        result = "No match found!"
        # 0xC
        if(bits == "1100"):
            result = "Unix Socket"
        # 0xA
        elif(bits == "1010"):
            result = "Symlink"
        # 0x8
        elif(bits == "1000"):
            result = "File"
        # 0x6
        elif(bits == "0110"):
            result = "Block Device"
        # 0x4
        elif(bits == "0100"):
            result = "Directory"
        # 0x2
        elif(bits == "0010"):
            result = "Character Device"
        # 0x1
        elif(bits == "0001"):
            result = "FIFO"
        return result

    def __getFlags(self, bits):
        v = ("SUID Bit: ",  "\n             SGID Bit: ", "\n           Sticky Bit: ")
        return v[0] + bits[0] + " " + v[1] + bits[1] + " " + v[2] + bits[2]

    def __getPermissions(self, bits):
        result = ""
        count = 0
        for b in bits:
            count += 1
            if(b == "1" and count == 1):
                result += "r"
            elif(b == "1" and count == 2):
                result += "w"
            elif(b == "1" and count == 3):
                result += "x"
                count = 0
            else:
                result += "-"

        return " ".join(result[i:i+3] for i in range(0, len(result), 3))
