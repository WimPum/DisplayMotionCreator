# MMDElectone用テンポ画面用Motion生成器「DisplayMotionCreator」

import csv
from pprint import pprint
# import CSV2VMD as C2V

totalKeys = 0  # あとで総キーフレーム数書くとき使う
keyframes = []  # ここにキーを追加します


def round_int(x): return int((x * 2 + 1) // 2)  # 小数点第一位を四捨五入する


def add_key_name(name, frameNum, value, lists):  # csvに書き込み
    lists += [[name, frameNum, value]]
    return lists


def add_key(num, digit, frameNum, lists):
    if num == 1:  # 煩雑ですみません
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 0.0],
            [f"ShiftV2_{digit}", frameNum, 0.0],
            [f"Shift>1_{digit}", frameNum, 0.0],
            [f"Shift>2_{digit}", frameNum, 0.0],
            [f"Shift>3_{digit}", frameNum, 0.0]
        ]
    elif num == 2:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 0.0],
            [f"ShiftV2_{digit}", frameNum, 0.0],
            [f"Shift>1_{digit}", frameNum, 1.0],
            [f"Shift>2_{digit}", frameNum, 0.0],
            [f"Shift>3_{digit}", frameNum, 0.0]
        ]
    elif num == 3:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 0.0],
            [f"ShiftV2_{digit}", frameNum, 0.0],
            [f"Shift>1_{digit}", frameNum, 1.0],
            [f"Shift>2_{digit}", frameNum, 1.0],
            [f"Shift>3_{digit}", frameNum, 0.0]
        ]
    elif num == 4:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 0.0],
            [f"ShiftV2_{digit}", frameNum, 0.0],
            [f"Shift>1_{digit}", frameNum, 1.0],
            [f"Shift>2_{digit}", frameNum, 1.0],
            [f"Shift>3_{digit}", frameNum, 1.0]
        ]
    elif num == 5:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 1.0],
            [f"ShiftV2_{digit}", frameNum, 0.0],
            [f"Shift>1_{digit}", frameNum, 0.0],
            [f"Shift>2_{digit}", frameNum, 0.0],
            [f"Shift>3_{digit}", frameNum, 0.0]
        ]
    elif num == 6:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 1.0],
            [f"ShiftV2_{digit}", frameNum, 0.0],
            [f"Shift>1_{digit}", frameNum, 1.0],
            [f"Shift>2_{digit}", frameNum, 0.0],
            [f"Shift>3_{digit}", frameNum, 0.0]
        ]
    elif num == 7:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 1.0],
            [f"ShiftV2_{digit}", frameNum, 0.0],
            [f"Shift>1_{digit}", frameNum, 1.0],
            [f"Shift>2_{digit}", frameNum, 1.0],
            [f"Shift>3_{digit}", frameNum, 0.0]
        ]
    elif num == 8:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 1.0],
            [f"ShiftV2_{digit}", frameNum, 0.0],
            [f"Shift>1_{digit}", frameNum, 1.0],
            [f"Shift>2_{digit}", frameNum, 1.0],
            [f"Shift>3_{digit}", frameNum, 1.0]
        ]
    elif num == 9:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 1.0],
            [f"ShiftV2_{digit}", frameNum, 1.0],
            [f"Shift>1_{digit}", frameNum, 0.0],
            [f"Shift>2_{digit}", frameNum, 0.0],
            [f"Shift>3_{digit}", frameNum, 0.0]
        ]
    elif num == 0:
        keyframesLocal = [
            [f"ShiftV1_{digit}", frameNum, 1.0],
            [f"ShiftV2_{digit}", frameNum, 1.0],
            [f"Shift>1_{digit}", frameNum, 1.0],
            [f"Shift>2_{digit}", frameNum, 0.0],
            [f"Shift>3_{digit}", frameNum, 0.0]
        ]
    lists += keyframesLocal
    return lists


def vmd_writer(filename, keyframes):  # vmd_calcではリスト生成のみ "a"でappend（追加）
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(keyframes)


def vmd_calc(mmdFps, bpm, timSig: int, length):
    # (bpm / 60)は1秒に幾つのノートがあるか(bps)
    keyframesheader = [
        ["Vocaloid Motion Data 0002", 0],
        ["Electone3DModel"],
        [0],  # ボーン数はゼロの前提です
    ]
    global keyframes
    noteDuration = mmdFps / (bpm / 60)  # 秒で表される音符と音符との間隔。
    totalNotes = int(length * (bpm / 60))  # 合計で幾つの音符が使われるか。
    # totalNotes = int(length / mmdFps * (bpm / 60))  # フレーム数使うとき
    global totalKeys
    remain = totalNotes % timSig
    if remain != 0:
        # 繰り上げ lengthで終わるのではなくtimSigの分まで
        totalNotes = int(totalNotes - remain + timSig)
    currentFrames = 0
    roundedFrames = 0

    can_add_key2 = False
    can_add_key1 = False

    for x in range(totalNotes):
        sigValue = int((x) / timSig) + 1  # これが10や100を超えたらキーが増える
        sigDisp = float(f"{sigValue}.{x % timSig + 1}")  # 16.2とかX.x(拍子)綺麗な方

        currentTime = currentFrames / mmdFps
        print(f"{roundedFrames}f, {sigDisp}, {currentTime}s")
        if sigDisp == 1.1:
            add_key_name("Ready", roundedFrames, 1.0,
                         keyframes)  # 追加した時点でValue 1.0
            add_key_name("One_3", roundedFrames, 1.0, keyframes)
            add_key_name("One_4", roundedFrames, 1.0, keyframes)
            totalKeys += 3
        elif sigDisp == 10.1:
            add_key_name("One_2", roundedFrames - 1, 0.0, keyframes)
            add_key_name("One_2", roundedFrames, 1.0, keyframes)
            totalKeys += 2
        elif sigDisp == 100.1:
            add_key_name("One_1", roundedFrames - 1, 0.0, keyframes)
            add_key_name("One_1", roundedFrames, 1.0, keyframes)
            totalKeys += 2

        add_key(x % timSig + 1, 4, roundedFrames, keyframes)  # キー追加 000.Xの部分
        add_key(int(sigValue % 10), 3, roundedFrames, keyframes)  # 00X.0
        if sigDisp >= 10 and can_add_key2 == True:
            add_key(int(sigValue / 10 % 10), 2,
                    roundedFrames, keyframes)  # 0X0.0
            can_add_key2 = False
            totalKeys += 5
        if sigDisp >= 100 and can_add_key1 == True:
            add_key(int(sigValue / 100 % 10), 1,
                    roundedFrames, keyframes)  # X00.0
            can_add_key1 = False
            totalKeys += 5

        totalKeys += 10

        currentFrames += noteDuration
        roundedFrames = round_int(currentFrames)
        nextSigValue = int((x + 1) / timSig) + 1  # 次のキーを見る

        add_key(x % timSig + 1, 4, roundedFrames - 1, keyframes)
        add_key(int(sigValue % 10), 3, roundedFrames - 1, keyframes)

        if sigDisp >= 10 and int(sigValue / 10 % 10) != int(nextSigValue / 10 % 10):
            # print(f"2nd number: ({int(sigValue / 10 % 10)},{int(nextSigValue / 10 % 10)})")
            add_key(int(sigValue / 10 % 10), 2, roundedFrames - 1, keyframes)
            can_add_key2 = True
            totalKeys += 5
        if sigDisp >= 100 and int(sigValue / 100 % 10) != int(nextSigValue / 100 % 10):
            # print(f"1st number: ({int(sigValue / 100 % 10)},{int(nextSigValue / 100 % 10)})")
            add_key(int(sigValue / 100 % 10), 1, roundedFrames - 1, keyframes)
            can_add_key1 = True
            totalKeys += 5
        totalKeys += 10
    keyframesheader += [[totalKeys]]  # 全キー数入れる
    keyframesheader += keyframes
    print(f"TotalNotes:{totalNotes}, TotalKeys:{totalKeys}")
    return keyframesheader


# MMDキーフレームのFPS, テンポ, 拍子, 長さ(秒)からキーフレームを打つべき場所を求める。
if __name__ == "__main__":
    vmd_writer("output.csv", vmd_calc(30, 60, 4, 40))  # 本体 CSV書き出し用
    # C2V.write_vmd_file("outputExp.vmd", vmd_calc(30, 120, 2, 120))  # 本体 VMD書き出し
