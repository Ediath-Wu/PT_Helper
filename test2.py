from bencode import decode, encode
import datetime
import hashlib

class GetTorrent():
    def getBT(self, file_path):
        with open(file_path, "rb") as f:
            # print(type(decode(f.read())))
            message = decode(f.read())
            return message

    def getMessage(self, message, mode='print'):
        print("发现了以下信息:")
        i_list = []
        if mode == "print":
            
            for i in message:
                i_list.append(i)
                print(i)
        elif mode == "return":
            return i_list

    def getannounce(self, message, mode="print"):
        if mode == "print":
            print("="*50, "announce", "="*50)
            print("announce 的数据类型为:", type(message[b'announce']))
            print("tracker 服务器列表:")
            print(message[b'announce'].decode())
        elif mode == "return":
            return message[b'announce'].decode()

    def getannouncelist(self, message, mode="print"):
        if mode == "print":
            print("="*50, "announce", "="*50)
            print("announce 的数据类型为:", type(message[b'announce-list']))
            print("tracker 服务器列表:")
            for a in message[b'announce-list']:
                for li in a:
                    print(li.decode())
        elif mode == "return":
            return message[b'announce-list'].decode()

    def getcomment(self, message, mode="print"):
        if mode == "print":
            print("="*50, "comment", "="*51)
            print(message[b'comment'].decode())
        elif mode == "return":
            return message[b'comment'].decode()

    def getcreatedby(self, message, mode="print"):
        if mode == "print":
            print("=" * 50, "created by", "=" * 48)
            print("由:", message[b'created by'].decode()," 创建")
        elif mode == 'return':
            return message[b'created by'].decode()

    def getcreationdate(self,message,mode="print"):
        if mode == "print":
            print("=" * 50, "creation date", "=" * 45)
            print(datetime.datetime.fromtimestamp(message[b'creation date']).strftime("%Y %m %d"))

    def getencoding(self,message,mode="print"):
        if mode == "print":
            print("=" * 50, "encoding", "=" * 50)
            print(message[b'encoding'].decode())

    def getinfo(self, message):
        # 获得每个文件里面的类容方法
        def getfilename(files_v):
            # 判断值是否为列表
            if isinstance(files_v, list):
                # 历遍列表
                for file_name in files_v:
                    # 如果列表里面的字符串是bytes类型的则转码，否则直接输出
                    if type(file_name) == bytes:
                        return file_name.decode()
                    else:
                        return file_name
            # 当不是列表时，直接输出（一般为int型目前没发现其他类型）
            else:
                return files_v

        print("=" * 50, "info", "=" * 54)
        # print("info的数据类型为:", type(message[b'info']))
        # 历遍所有的keys
        for k in message[b'info'].keys():
            # print("key:", k)
            # print(message[b'info'].key())
            value = message[b'info'][k]
            # print("value", value)
            # 如果是files
            if k == b'files':
                # 遍历files列表
                print("该BT种子里总共有%d个文件" % len(value))
                v_i = 0
                for v_list_dic in value:
                    # 遍历列表里的字典得到每一个文件
                    print("第%d个文件" % v_i)
                    for files_k, files_v in v_list_dic.items():
                        data = getfilename(files_v)
                        if files_k == b'length':
                            print("文件大小：%0.2f%s" % (data / 1024 / 1024, "MB"))
                        elif files_k == b'path':
                            print("文件名：", data)
                        else:
                            print(files_k, "：", data)
                    v_i += 1;

            # 如果是是文件名：
            elif k == b'name':
                print("文件名:", value.decode())
            # 如果是文件的MD5校验和：
            elif k == b'md5sum  ':
                # print(type(value))
                print("长32个字符的文件的MD5校验和：", value)
            # 文件长度
            elif k == b'length':
                # print(type(value))
                print("文件长度，单位字节：", value / 1024, "KB")
            elif k == b'path':
                # print(type(value))
                print("文件的路径和名字：", value)
            elif k == b'piece length':
                # print(type(value))
                print("每个块的大小:", value / 1024 / 1024, "MB")
            elif k == b'pieces':
                # print(type(value))
                print("每个块的20个字节的SHA1 Hash的值(二进制格式) ：", str(value.decode()))
            elif k == b'piece length':
                # print(type(value))
                print("每个块的大小，单位字节：", value, "B")

            # print("value", v)
            
    def getw(self,message):
        
        def print_dict(a_dict):
            # print(a_dict,"is a dict.")
            for key in a_dict:
                if isinstance(a_dict[key],dict):
                    print("key:",key,"value:")
                    print_dict(a_dict[key])
                elif isinstance(a_dict[key],list):
                    print("key:",key,"value:")
                    print_list(a_dict[key])
                else:
                    if isinstance(a_dict[key],bytes):
                        try:
                            a_dict[key]=a_dict[key].decode()
                        except UnicodeEncodeError:
                            pass               
                    print("key: ",key.decode(),", value: ",a_dict[key])
        
        def print_list(a_list):
            # print(a_list,"is a list.")
            for item in a_list:
                if isinstance(item,dict):
                    print_dict(item)
                elif isinstance(item,list):
                    print_list(item)
                else:
                    if isinstance(item,bytes):
                        print("\titem: ", item.decode())
                    else:
                        print("\titem: ", item)
        

        for key in message:
            print(key,"    type: ", type(message[key]))
            if isinstance(message[key],list):
                # print(message[key],"is a list")
                print_list(message[key])
                
            elif isinstance(message[key],dict):
                # print(message[key],"is a dict")
                print_dict(message[key])
    
    def gethash(self,message):
        info=message[b'info']
        # 得到hash的计算方法:计算bytes格式下的整个info信息
        print(hashlib.sha1(encode(info)).hexdigest())


a = GetTorrent()

a.getMessage(a.getBT("PT_Helper/abc.torrent"))
a.getannounce(a.getBT("PT_Helper/abc.torrent"))
# a.getcomment(a.getBT("PT_Helper/abcd.torrent"))
# a.getcreatedby(a.getBT("PT_Helper/abcd.torrent"))
# a.getcreationdate(a.getBT("PT_Helper/abcd.torrent"))
# a.getencoding(a.getBT("PT_Helper/abcd.torrent"))
# a.getinfo(a.getBT("PT_Helper/abcd.torrent"))
# a.getannouncelist(a.getBT("pt_Helper/abc.torrent"))

# a.getw(a.getBT("PT_Helper/abcd.torrent"))
a.gethash(a.getBT("PT_Helper/abc.torrent"))