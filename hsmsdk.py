import struct


XAccessToken = "3fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165"
Source = "PythonSDK-1.0.0"

def channelArray(channels):
    # channel_array = [2, 5, 12, 9]
    bits = 0

    for channel_num in channels:
        if 0 <= channel_num < 64:
            bits |= 1 << channel_num
    return bits

def full_mode_msg(channels):
    buffer_size = 19

    byte_buffer = bytearray(buffer_size)

    # DataLen
    data_len = buffer_size - 2  # 2 bytes for DataLen
    struct.pack_into("!H", byte_buffer, 0, data_len)
    byte_buffer[2] = 12

    byte_buffer[3] = 2
    byte_buffer[4] = 1
    byte_buffer[5] = 8
    bits = channelArray(channels)
    byte_buffer[7] = struct.pack('>Q', bits)[0]
    # for i in range(8):
    #     byte_buffer[7+i] = (bits >> (56 - i * 8)) & 0xFF
    #     print(i+7)
    byte_buffer[15] = 2
    byte_buffer[16] = 1
    byte_buffer[18] = 70

    return byte_buffer

# print(full_mode_msg([1,5,4,8,6]))

def TokenByteMsg(XAccessToken , Source):
    # Create the byte buffer
    buffer_size = 18 + len(XAccessToken) + len(Source)
    byte_buffer = bytearray(buffer_size)

    # DataLen
    data_len = buffer_size - 2  # 2 bytes for DataLen
    struct.pack_into("!H", byte_buffer, 0, data_len)
    # ReqType
    byte_buffer[2] = 1  # 1 for Authentication request type

    # FieldCount
    byte_buffer[3] = 4  # 4 fields

    # Field-1: XAccessToken
    field1_id = 1
    field1_size = len(XAccessToken)
    struct.pack_into("!B", byte_buffer, 4, field1_id)
    struct.pack_into("!H", byte_buffer, 5, field1_size)
    struct.pack_into(f"!{field1_size}s", byte_buffer, 7, XAccessToken.encode())

    # Field-2: Constant byte value 78
    field2_id = 2
    field2_size = 1
    struct.pack_into("!B", byte_buffer, 7+field1_size, field2_id)
    struct.pack_into("!H", byte_buffer, 8+field1_size, field2_size)
    byte_buffer[10+field1_size] = 78

    # Field-3: Constant byte value 1
    field3_id = 3
    field3_size = 1
    struct.pack_into("!B", byte_buffer, 11+field1_size, field3_id)
    struct.pack_into("!H", byte_buffer, 12+field1_size, field3_size)
    byte_buffer[14+field1_size] = 1

    # Field-4: Source
    field4_id = 4
    field4_size = len(Source)
    struct.pack_into("!B", byte_buffer, 15+field1_size, field4_id)
    struct.pack_into("!H", byte_buffer, 16+field1_size, field4_size)
    struct.pack_into(f"!{field4_size}s", byte_buffer, 18+field1_size, Source.encode())

    return byte_buffer


def ScripsbytesMsg(scrips , channelNumber):
    # Prepare scripsData for Field-1
    scripsData = bytearray()
    scripsData.append(len(scrips) >> 8 & 0xFF)
    scripsData.append(len(scrips) & 0xFF)
    for scrip in scrips:
        scripBytes = scrip.encode("ascii")
        scripsData.append(len(scripBytes))
        scripsData.extend(scripBytes)

    # Prepare the binary data buffer
    dataLen = 18 + len(scripsData) + len(XAccessToken) + len(Source)
    reqType = 4
    fieldCount = 2
    buffer = bytearray()
    buffer.extend(struct.pack(">H", dataLen))
    buffer.append(reqType)
    buffer.append(fieldCount)

    # Field-1
    buffer.append(1)  # Field-ID
    buffer.extend(struct.pack(">H", len(scripsData)))
    buffer.extend(scripsData)

    # Field-2
    buffer.append(2)  # Field-ID
    buffer.extend(struct.pack(">H", 1))
    buffer.append(channelNumber)

    return buffer



# "sf|nse_cm|25","dp|nse_cm|25", "sf|nse_cm|22", "dp|nse_cm|22"

scrips = ["sf|mcx_fo|249702", "dp|mcx_fo|249702",]
channelNumber = 1
print(ScripsbytesMsg(scrips, channelNumber))

# -------------------------------------------------------------------------

def responsePrint(data):
    # datasize, restype, field_count = struct.unpack('!HBB', data[:4])
    datasize, restype = struct.unpack('!HB', data[:3])

    if restype == 1:
        field_id = struct.unpack('!B', data[4:5])[0]

        field_length = struct.unpack('!H', data[5:7])[0]
        string_val = data[7:7+field_length].decode('utf-8')
        if string_val == "K":
            print("Authentication done")
        else:
            print("Authentication failed")
        field_id = struct.unpack('!B', data[7:8])[0]
        field_length = struct.unpack('!H', data[8:10])[0]
        ack_count = struct.unpack('>I', data[10+field_length:14+field_length])[0]


        json_obj = data[14+field_length:].decode()
        print("JSON object:", json_obj)
    elif restype == 4:
        field_count = struct.unpack('!B', data[3:4])[0]

        if field_count >= 1:
            field_id = struct.unpack('!B', data[4:5])[0]
            field_length = struct.unpack('!H', data[5:7])[0]
            string_val = data[7:7+field_length].decode('utf-8')
            print(string_val)
            if string_val == "K":
                print("Subscribed")
            else:
                print("error in subscibe")
    else:
        print(data)

# print()

def FeedData(data):
    ack_count =54554

    datasize, restype = struct.unpack('!HB', data[:3])
    print("resptype:", restype)
    print(list(data))
    updateCount = 0
    if ack_count > 0:
        updateCount += 1
        msgNum = struct.unpack('>I', data[3:7])[0]
        print(msgNum)
        if updateCount == ack_count:
            # send acknoledgement 
            updateCount = 0
    scripCount = struct.unpack('!H', data[7:9])[0]
    print("sripssss",scripCount)
    offset = 9
    for _ in range(scripCount):
        dataType = struct.unpack('B', data[offset:offset+1])[0]
        print(dataType)
        if dataType == 83: 
            offset += 1
            topicId = struct.unpack('H', data[offset:offset+2])[0]
            print(topicId)
            offset += 2
            topicNameLength = struct.unpack('B', data[offset:offset+1])[0]
            print(topicNameLength)
            offset += 1
            topicName = data[offset:offset+topicNameLength].decode('utf-8')
            print(topicName)
            offset += topicNameLength
            fieldCount = struct.unpack('B', data[offset:offset+1])[0]
            print(fieldCount)
            offset += 1

            for index in range(fieldCount):
                value = struct.unpack('>I', data[offset:offset+4])[0]
                offset += 4
                print(f"Field {index+1}: {value}")

            stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
            offset += 2
            multiplier = struct.unpack('H', data[offset:offset+2])[0]
            print(multiplier)
            offset += 2
            precision = struct.unpack('B', data[offset:offset+1])[0]
            print("precision",precision)
            offset += 1
            
            for _ in range(3):
                stringLength = struct.unpack('B', data[offset:offset+1])[0]
                offset += 1
                stringData = data[offset:offset+stringLength].decode('utf-8')
                print(stringData)
                offset += stringLength


# data =b'\x00\x16\x06\x00\x00\x00\x05\x00\x01L\x00\x00\x00\x02\xeb+\x00\x16\xdd\xc3dc#\xc0'
# data = b"\x00\x87\x06\x00\x00\x00\x02\x00\x01S\x00\x00\x0csf|nse_cm|25\x15\x00\x02\xea\xcc\x00\x17\xed\xb9dc+\x1bdc+\x1c\x00\x00\x00\t\x00\x00\x007\x00\x02\xea\x86\x00\x02\xea\xd1\x00\x00\x00#\x00\x03:\xba\x00\x06I\x83\x00\x02\xedr\x80\x00\x00\x00\x00\x02\xe74\x00\x02\xf3\xdc\x80\x00\x00\x00\x80\x00\x00\x00\x00\x02\x94\x82\x00\x03'D\x00\x02\xf0\xbc\x00\x02\xecu\x00\x19\x00\x01\x02\x06nse_cm\x0225\x0bADANIENT-EQ"
data = b"\x00\x87\x06\x00\x00\x00\x02\x00\x01S\x00\x00\x0csf|nse_cm|25\x15\x00\x02\xea\xcc\x00\x17\xed\xb9dc+\x1bdc+\x1c\x00\x00\x00\t\x00\x00\x007\x00\x02\xea\x86\x00\x02\xea\xd1\x00\x00\x00#\x00\x03:\xba\x00\x06I\x83\x00\x02\xedr\x80\x00\x00\x00\x00\x02\xe74\x00\x02\xf3\xdc\x80\x00\x00\x00\x80\x00\x00\x00\x00\x02\x94\x82\x00\x03'D\x00\x02\xf0\xbc\x00\x02\xecu\x00\x19\x00\x01\x02\x06nse_cm\x0225\x0bADANIENT-EQ"
# print(FeedData(data))




def LiteFeedData(data):
    ack_count =6468468
    datasize, restype = struct.unpack('!HB', data[:3])
    print("resptype:", restype)
    print(list(data))
    updateCount = 0
    if ack_count > 0:
        updateCount += 1
        msgNum = struct.unpack('>I', data[3:7])[0]
        print(msgNum)
        if updateCount == ack_count:
            # send acknoledgement 
            updateCount = 0
    scripCount = struct.unpack('!H', data[7:9])[0]
    print("scripCount",scripCount)
    offset = 9
    for _ in range(scripCount):
        dataType = struct.unpack('B', data[offset:offset+1])[0]
        print(dataType)
        if dataType == 76: 
            offset += 1
            topicId = struct.unpack('H', data[offset:offset+2])[0]
            print("topicid",topicId)
            # offset += 2
            # topicNameLength = struct.unpack('B', data[offset:offset+1])[0]
            # print(topicNameLength)
            # offset += 1
            # topicName = data[offset:offset+topicNameLength].decode('utf-8')
            # print(topicName)
            # offset += topicNameLength
            fieldCount = struct.unpack('B', data[offset:offset+1])[0]
            print("fieldcount",fieldCount)
            offset += 1
            # fieldCount = 12
            # for _ in range(fieldCount):
            #     value = struct.unpack('i', data[offset:offset+4])[0]
            #     print("value :",value)
            #     offset += 4
            # arr = [1,3,4,5,6,9,10,11]
            for index in range(fieldCount):
                # offset = index * 4  # Each field is 4 bytes long
                value = struct.unpack('>I', data[offset:offset+4])[0]
                offset += 4
                # if index in arr:
                print(f"Field {index+1}: {value}")
                # else:
                #     print(f"Field {index+1}: {value/100}")
            stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
            offset += 2
            multiplier = struct.unpack('H', data[offset:offset+2])[0]
            print(multiplier)
            offset += 2
            precision = struct.unpack('B', data[offset:offset+1])[0]
            print(precision)
            offset += 1
            
            for _ in range(3):
                stringLength = struct.unpack('B', data[offset:offset+1])[0]
                offset += 1
                stringData = data[offset:offset+stringLength].decode('utf-8')
                print(stringData)
                offset += stringLength

def ByteToJson( data):
        response = {}
        datasize, restype = struct.unpack('!HB', data[:3])

        if restype == 1:
            field_id = struct.unpack('!B', data[4:5])[0]
            field_length = struct.unpack('!H', data[5:7])[0]
            string_val = data[7:7+field_length].decode('utf-8')
            if string_val == "K":
                print("Authentication done")
            else:
                print("Authentication failed")
            field_id = struct.unpack('!B', data[7:8])[0]
            field_length = struct.unpack('!H', data[8:10])[0]
            ack_count = struct.unpack('>I', data[10+field_length:14+field_length])[0]

            ack_count = 64446846
            json_obj = data[14+field_length:].decode()
            print("JSON object:", json_obj)
        elif restype == 4:
            pass #Subscription 
        elif restype == 5:
            pass # unsubscription
        elif restype == 6:
            #datafeed
            ack_count = 64446846
            # datasize, restype = struct.unpack('!HB', data[:3])
            print("resptype:", restype)
            print(list(data))
            updateCount = 0
            if ack_count > 0:
                updateCount += 1
                msgNum = struct.unpack('>I', data[3:7])[0]
                print(msgNum)
                if updateCount == ack_count:
                    # send acknoledgement 
                    updateCount = 0
            scripCount = struct.unpack('!H', data[7:9])[0]
            print("sripssss",scripCount)
            offset = 9
            for _ in range(scripCount):
                dataType = struct.unpack('B', data[offset:offset+1])[0]
                print("dataType",dataType)
                if dataType == 83: 
                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    print("topicid",topicId)
                    offset += 2
                    topicNameLength = struct.unpack('B', data[offset:offset+1])[0]
                    print("topicNameLength",topicNameLength)
                    offset += 1
                    topicName = data[offset:offset+topicNameLength].decode('utf-8')
                    print("topicName",topicName)
                    offset += topicNameLength
                    fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                    print(fieldCount)
                    offset += 1

                    for index in range(fieldCount):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        response["Field"+str(index)] = value
                        print(f"Field {index+1}: {value}")
                    print(response)
                    stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2
                    multiplier = struct.unpack('H', data[offset:offset+2])[0]
                    print("multiplier",multiplier)
                    offset += 2
                    precision = struct.unpack('B', data[offset:offset+1])[0]
                    print("precision",precision)
                    offset += 1
                    
                    for _ in range(3):
                        stringLength = struct.unpack('B', data[offset:offset+1])[0]
                        offset += 1
                        stringData = data[offset:offset+stringLength].decode('utf-8')
                        print("stringData",stringData)
                        offset += stringLength
                    
                elif dataType == 85:
                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    print(topicId)
                    offset += 2
                    fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                    print(fieldCount)
                    offset += 1
                    for index in range(fieldCount):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        response["Field"+str(index)] = value
                        print(f"Field {index+1}: {value}")
                elif dataType == 76:
                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    print(topicId)
                    offset += 2
                    # fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                    # print(fieldCount)
                    # offset += 1
                    for index in range(3):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        response["Field"+str(index)] = value
                        print(f"Field {index+1}: {value}")
                else:
                    print("Invalid Datatype Error")

# data = b'\x00\x95\x06\x00\x00\x00\x02\x00\x01\x00\x8eS\x00\x00\x00\x00\rsf|mcx_fo|114\x19\x00\x00\x00\x06\x03\xc2\x08\xb9dcjsdb\xed\xd7\x00\x00\x00\x00\x00\\\xdaP\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00]"\xf8\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x034\x031145\x06mcx_fo6\x04GOLD'
data = bytearray(b'\x01-\x06\x00\x00\x00\x02\x00\x02S\x00\x01\x0fdp|nse_cm|11536\x1e\x00\x05{\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x003\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x00\x01\x02\x06nse_cm\x0511536\x06TCS-EQS\x00\x00\x0fsf|nse_cm|11536\x15\x00\x05{\xde\x00\x01<\x81d_>\xffd_?~\x00\x00\x003\x00\x00\x00\x00\x00\x05{\xde\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x003\x00\x00\x00\x00\x00\x05s\x8b\x80\x00\x00\x00\x00\x04\xaf8\x00\x05}x\x80\x00\x00\x00\x80\x00\x00\x00\x00\x04L\xaa\x00\x05A<\x00\x04\xb7l\x00\x05{\xde\x00\x17\x00\x01\x02\x06nse_cm\x0511536\x06TCS-EQ')
# data = b'\x00\x16\x06\x00\x00\x00\x03\x00\x01L\x00\x00\x00\x02\xea\xcc\x00\x17\xed\xb9dc+\x1b'
# print(ByteToJson(data))




import struct

import struct

# Channels array
channels = [1, 2, 5, 12, 9]

# Initialize an empty byte array
data = bytearray()

# Add 2 bytes for data length
data.extend(struct.pack('>H', 0))

# Add 1 byte for request type (12 for Channel-Mode)
data.extend(struct.pack('B', 12))

# Add 1 byte for field count (2 fields)
data.extend(struct.pack('B', 2))

# Field 1 - Channel list as a long value
channel_bits = 0
for channel_num in channels:
    if channel_num < 64 and channel_num > 0:
        channel_bits |= 1 << channel_num

field_1 = bytearray()
field_1.extend(struct.pack('B', 1))     # Field ID
field_1.extend(struct.pack('>H', 8))    # Field size
field_1.extend(struct.pack('>Q', channel_bits))  # Field value
data.extend(field_1)

# Field 2 - Full mode feeds/updates (set to 70)
field_2 = bytearray()
field_2.extend(struct.pack('B', 2))     # Field ID
field_2.extend(struct.pack('>H', 1))    # Field size
field_2.extend(struct.pack('B', 70))    # Field value
data.extend(field_2)

# Update data length in the header
data_length = len(data) - 2
data[0] = (data_length >> 8) & 0xFF
data[1] = data_length & 0xFF

# Print the final packed data as bytes
# print(bytes(data))
