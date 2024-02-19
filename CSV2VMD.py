#  CSV to VMD (Only for Morph keys)
#  参考：https://qiita.com/Fujitsu_IncubationCenter/items/fa387786b443a6f5caf7
#  リンク切れしたのでWayback Machine使って閲覧してください。

# モーフ用です

import struct
from pprint import pprint

def write_vmd_file(filename, keyframes):

    fout = open(filename, "wb")  # wb is "write bytes"

    # header
    fout.write(b'Vocaloid Motion Data 0002\x00\x00\x00\x00\x00')
    fout.write(b'Electone3DModel     ')  # Char 20Bytes
    fout.write(struct.pack('<L', 0))  # ボーンのキー数はゼロ前提

    # skin keypoints
    totalKeys = int(keyframes[3][0])
    fout.write(struct.pack('<L', totalKeys))  # モーフのキー数 #!５行目

    for x in range(totalKeys):  # 各キーポイントの情報を格納 xはゼロから始まる
        """
        print(keyframes[4 + x][0])
        print(keyframes[4 + x][1])
        print(keyframes[4 + x][2])
        """
        keyName = (keyframes[4 + x][0]).encode()
        fout.write(keyName)  # モーフ名 #! 1st
        # モーフ名15Byteの残りを\0で埋める
        fout.write(bytearray([0 for i in range(len(keyName), 15)]))
        fout.write(struct.pack('<L', keyframes[4 + x][1]))  # フレーム番号 #! 2nd
        # パラメータ(0~1) #! 3rd
        fout.write(struct.pack('<f', keyframes[4 + x][2]))

    fout.close()


# モーフのみのVMDをCSVに変換する
# 参考: https://daizyu.com/posts/2020-08-08-002/
def vmd_to_csv(vmdname):
    file = open(vmdname, "rb")
    binaryData = file.read()
    # print(binaryData)
    header = str(struct.unpack_from("<30sx", binaryData, 0)[0].decode()).replace("\x00", "")  # <はリトルエンディアン char 30byte
    if header != "Vocaloid Motion Data 0002\x00\x00\x00\x00\x00":
        print("THIS IS NOT A VMD FILE")
    modelName = struct.unpack_from("<20s", binaryData, 30)[0].decode() # 30byte目から読み込み
    boneCount, morphCount = struct.unpack_from("<II", binaryData, 50)
    keyframesheader = [
        [header, 0],
        [modelName],
        [boneCount],
        [morphCount]
    ]
    keyframes = [] # これが二次元配列になるやつ
    for x in range(morphCount):
        keyname, frame, value = struct.unpack_from("<15sLf", binaryData, 58+23*x)
        keyname = str(keyname.decode()).replace("\x00", "")
        keyframes += [[keyname, frame, value]]
    returnKey = keyframesheader + keyframes
    pprint(returnKey)
    return returnKey


if __name__ == "__main__":
    try:
        vmd_to_csv("outputExp.vmd")
    except FileNotFoundError:
        print("outputExp.vmd not found. Quitting")
