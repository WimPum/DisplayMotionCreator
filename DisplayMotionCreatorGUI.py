# GUI版DisplayMotionCreator

import PySimpleGUI as sg  # GUI
import DisplayMotionCreator as DMC  # モーフ計算
import CSV2VMD as C2V  # リストをVMDに書き出し
import platform  # Windows, macOS, Linux OS情報取得


class ValueRangeError(Exception):  # 値の範囲でraise error
    pass


sg.theme('Dark')

layout = [[sg.Push(), sg.Text("MMDElectone", font="20"), sg.Push()],
          [sg.Push(), sg.Text("テンポ画面用Motion生成器", font="20"), sg.Push()],
          [sg.InputText("テンポを入力", key="tempo", font="16", tooltip="BPMを入力してください。"), sg.Text(
              "bpm", font="20")],
          [sg.InputText("拍子を入力", key="timsig", font="16", tooltip="拍子を整数で入力してください。\n4分の4なら'4',4分の3なら'3'と入力"), sg.Text(
              "拍", font="20")],
          [sg.InputText("長さを入力", key="length", font="16", tooltip="モーションの長さを秒単位で入力してください。"), sg.Text(
              "秒", font="20")],
          [sg.InputText("開始フレーム位置を入力", key="startframe", font="16", tooltip="変更がない場合はデフォルトは0です。"), sg.Text(
              "frame", font="20")],
          [sg.InputText("開始小節番号を入力(1以上)", key="startbar", font="16", tooltip="1以上を入力してください。\n変更がない場合はデフォルトは1です。"), sg.Text(
              "小節目", font="20")],
          [sg.InputText("出力先を選択", key="output", font="16", tooltip="右のボタンを押し出力先を選択"),
           sg.FolderBrowse("open", key="open", font="20")],
          [sg.Push(), sg.Button("実行！", key="ok", font="20"), sg.Push()]]

window = sg.Window("DisplayMotionCreator", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "open":
        sg.FolderBrowse()
    elif event == "ok":
        try:
            if str(values["tempo"]) == "" or str(values["timsig"]) == "" or \
                    str(values["length"]) == "" or str(values["output"]) == "":
                raise TypeError
            if int(values["timsig"]) < 1 or int(values["timsig"]) > 9:
                raise ValueRangeError
            if values["startbar"] != "開始小節番号を入力(1以上)" and int(values["startbar"]) < 1:
                raise ValueError
            DMC.keyframes = []
            DMC.totalKeys = 0

            tempo = float(values["tempo"])
            timsig = int(values["timsig"])
            length = float(values["length"])

            if values["startframe"] == "開始フレーム位置を入力":
                startframe = 0
            else:
                startframe = int(values["startframe"])
            if values["startbar"] == "開始小節番号を入力(1以上)":
                startbar = 1
            else:
                startbar = int(values["startbar"])
            directory = values["output"]

            VMDList = DMC.vmd_calc(30, tempo, timsig, length, startframe, startbar)  # the core
            osName = platform.system()
            print(f"Platform: {osName}")
            if osName == "Windows":
                C2V.write_vmd_file(f"{directory}\output.vmd", VMDList)
            else:
                C2V.write_vmd_file(f"{directory}/output.vmd", VMDList)

            if DMC.totalKeys >= 20000:
                sg.popup(
                    f"{tempo}bpm、{timsig}拍子、{length}秒で生成しました。キー数{DMC.totalKeys}です。\nMMDのキー登録数の上限は20000ですので注意してください。",
                    title="出力完了", font="20", keep_on_top=True)
            else:
                sg.popup(
                    f"{tempo}bpm、{timsig}拍子、{length}秒で生成しました。キー数{DMC.totalKeys}です。", title="出力完了", font="20", keep_on_top=True)

        except ValueError:
            sg.popup("数値を正しく入力してください。", title="エラー発生", font="20",
                     keep_on_top=True)
        except TypeError:
            sg.popup("数値を正しく入力し、出力先を選択してください。", title="エラー発生", font="20",
                     keep_on_top=True)
        except ValueRangeError:
            sg.popup("拍子は１〜９までの整数値で入力してください。", title="エラー発生", font="20",
                     keep_on_top=True)
        except FileNotFoundError:
            sg.popup("出力先のフォルダを選択してください。", title="エラー発生",
                     font="20", keep_on_top=True)
        except OSError:
            sg.popup("出力先にアクセスできません。別のディレクトリを指定してください。", title="エラー発生",
                     font="20", keep_on_top=True)

window.close()
