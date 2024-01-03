#  CSV to VMD (Only for Morph keys)
#  参考：https://qiita.com/Fujitsu_IncubationCenter/items/fa387786b443a6f5caf7
#  リンク切れしたのでWayback Machine使って閲覧してください。

# モーフ用です

import struct


def write_vmd_file(filename, keyframes):

    fout = open(filename, "wb")  # wb is "write bytes"

    # header
    fout.write(b'Vocaloid Motion Data 0002\x00\x00\x00\x00\x00')
    fout.write(b'Electone3DModel     ')  # Char 20Bytes
    fout.write(struct.pack('<L', 0))  # ボーンのキー数はゼロ前提

    # skin keypoints
    totalKeys = int(keyframes[3][0])
    fout.write(struct.pack('<L', totalKeys))  # モーフのキー数 # //!５行目

    for x in range(totalKeys):  # 各キーポイントの情報を格納 xはゼロから始まる
        """
        print(keyframes[4 + x][0])
        print(keyframes[4 + x][1])
        print(keyframes[4 + x][2])
        """
        keyName = (keyframes[4 + x][0]).encode()
        fout.write(keyName)  # モーフ名 # //! 1st
        # モーフ名15Byteの残りを\0で埋める
        fout.write(bytearray([0 for i in range(len(keyName), 15)]))
        fout.write(struct.pack('<L', keyframes[4 + x][1]))  # フレーム番号 # //! 2nd
        # パラメータ(0~1) # //! 3rd
        fout.write(struct.pack('<f', keyframes[4 + x][2]))

    fout.close()
