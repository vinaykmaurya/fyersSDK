import struct
import websockets


class HsmWebsocket:

    def __init__(self,access_token,scrips):
        self.url = ""
        self.access_token = access_token
        self.Source = ""
        self.channelNum = 1
        self.scrips = scrips
    
    def TokenToBytes(self):
        XAccessToken = self.access_token
        Source = self.Source
        buffer_size = 18 + len(XAccessToken) + len(Source)
        byteMsg = bytearray(buffer_size)

        data_len = buffer_size - 2 
        struct.pack_into("!H", byteMsg, 0, data_len)

        byteMsg[2] = 1 

        byteMsg[3] = 4  

        # Field-1: XAccessToken
        field1_id = 1
        field1_size = len(XAccessToken)
        struct.pack_into("!B", byteMsg, 4, field1_id)
        struct.pack_into("!H", byteMsg, 5, field1_size)
        struct.pack_into(f"!{field1_size}s", byteMsg, 7, XAccessToken.encode())

        # Field-2: Constant byte value 78
        field2_id = 2
        field2_size = 1
        struct.pack_into("!B", byteMsg, 7+field1_size, field2_id)
        struct.pack_into("!H", byteMsg, 8+field1_size, field2_size)
        byteMsg[10+field1_size] = 78

        # Field-3: Constant byte value 1
        field3_id = 3
        field3_size = 1
        struct.pack_into("!B", byteMsg, 11+field1_size, field3_id)
        struct.pack_into("!H", byteMsg, 12+field1_size, field3_size)
        byteMsg[14+field1_size] = 1

        # Field-4: Source
        field4_id = 4
        field4_size = len(Source)
        struct.pack_into("!B", byteMsg, 15+field1_size, field4_id)
        struct.pack_into("!H", byteMsg, 16+field1_size, field4_size)
        struct.pack_into(f"!{field4_size}s", byteMsg, 18+field1_size, Source.encode())

        return byteMsg
    

    def SubscriptionMsgByte(self):
        scrips = self.scrips
        ChNum = self.channelNum
        scripsData = bytearray()
        scripsData.append(len(scrips) >> 8 & 0xFF)
        scripsData.append(len(scrips) & 0xFF)
        for scrip in scrips:
            scripBytes = scrip.encode("ascii")
            scripsData.append(len(scripBytes))
            scripsData.extend(scripBytes)

        dataLen = 18 + len(scripsData) + len(self.access_token) + len(self.Source)
        reqType = 4
        fieldCount = 2
        buffer = bytearray()
        buffer.extend(struct.pack(">H", dataLen))
        buffer.append(reqType)
        buffer.append(fieldCount)

        # Field-1
        buffer.append(1) 
        buffer.extend(struct.pack(">H", len(scripsData)))
        buffer.extend(scripsData)

        # Field-2
        buffer.append(2) 
        buffer.extend(struct.pack(">H", 1))
        buffer.append(ChNum)

        return buffer
     
    def ByteToJson(self, data):
        response = []
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

            self.ackCount = ack_count
            json_obj = data[14+field_length:].decode()
            print("JSON object:", json_obj)
        elif restype == 4:
            pass #Subscription 
        elif restype == 5:
            pass # unsubscription
        elif restype == 6:
            #datafeed
            self.ackCount
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
                        response["Field"+str(index)] = value
                        print(f"Field {index+1}: {value}")
                    print(response)
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
                        response.append(value)
                        print(f"Field {index+1}: {value}")
                    print("response : ", response)
                # elif dataType == 76:
                #     offset += 1
                #     topicId = struct.unpack('H', data[offset:offset+2])[0]
                #     print(topicId)
                #     offset += 2
                #     fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                #     print(fieldCount)
                #     offset += 1
                #     for index in range(fieldCount):
                #         value = struct.unpack('>I', data[offset:offset+4])[0]
                #         offset += 4
                #         response["Field"+str(index)] = value
                #         print(f"Field {index+1}: {value}")
                else:
                    print("Invalid Datatype Error")


print(BytetoJson)


WsResponse = {}
resp = {

}

depth = []