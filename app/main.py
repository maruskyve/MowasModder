# pyinstaller App to exe: pyinstaller --noconfirm --onedir --windowed main.spec

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import get_color_from_hex as hex
import os, sys
from kivy.resources import resource_add_path

# Builder.load_file('main.kv')
dataTxt = 'data.txt'
gameScn = 'status'


class Homepage(Screen):
    clicked_difficult_level, init_difficult_level = object(), object()
    difficult_level, savegame_foldername = str(), str()
    data = str()
    executeStatus, executeSuccess = bool(), bool()
    oldActionBlSize = list()
    resultLog = str()

    def dataInit(self):
        try:
            if os.path.exists(dataTxt):
                data = open(dataTxt, 'r').readlines()
                self.data = data
        except Exception: pass
        pass

    def valueInit(self):
        # reading folderpath.txt
        try:
            if os.path.exists(dataTxt):
                self.dataInit()

                def folderpathInit():
                    _string = self.data[0][0:-1].replace('folderpath=', '')
                    self.ids.folderpath.text = _string

                def savegameFolderListInit():
                    folders = str()
                    try:
                        mainPath = self.data[0][0:-1].replace('folderpath=', '')
                        for name in os.listdir(mainPath):
                            folders += name+'\n'
                        if folders != '':
                            self.ids.savegame_folder_list.text = folders
                        else: pass
                    except Exception:
                        pass
                    print('data init')

                def savegameFoldernameInit():
                    _string = self.data[1][0:-1].replace('savegame_foldername=', '')
                    self.ids.savegame_foldername.text = _string

                def difficultButtonInit():
                    try:
                        obj = object()
                        if 'easy' in self.data[2]:
                            obj = self.ids.easy
                        elif 'medium' in self.data[2]:
                            obj = self.ids.medium
                        elif 'hard' in self.data[2]:
                            obj = self.ids.hard
                        elif 'heroic' in self.data[2]:
                            obj = self.ids.heroic
                        self.init_difficult_level = obj
                        obj.background_color = hex('#1F81CA')
                        obj.background_normal = ''
                    except Exception: print('no diff')

                folderpathInit()
                savegameFolderListInit()
                savegameFoldernameInit()
                difficultButtonInit()

        except Exception:
            print('data.txt not found')

    def dataTxtFormatter(self, folderpath, savegame_folder, difficult_level):
        return f'folderpath={folderpath}\nsavegame_foldername={savegame_folder}\ndifficult_level={difficult_level}'

    def buttonClicked(self, root, bg, fbg):
        root.background_color = hex(bg)
        # root.background_normal = ''
        root.color = hex(fbg)

    def folderpathVerify(self, folderpath, root):
        folderpath = str(folderpath)
        print(folderpath)

        def writeInformation():
            # checking if folderpath are exist
            def failChain():
                self.buttonClicked(root, 'FFFFFFFF', '098978')
                root.text = 'Verify'
            if self.ids.folderpath.text != '':
                if os.path.exists(folderpath):
                    print('Folder Exist')
                    # checking if folderpath is a folder
                    if os.path.isdir(folderpath):
                        print('Is a Folder')
                        # write to folderpath.txt
                        open(dataTxt, 'w').write(self.dataTxtFormatter(folderpath=folderpath,
                                                                       savegame_folder=None,
                                                                       difficult_level=None))
                        # self.ids.savegame_foldername.text: ''
                        self.buttonClicked(root, '51CB89', 'FFFFFFFF')
                        self.ids.savegame_foldername.text = ''
                        self.ids.folderpath_verify_button.text = 'Verified'
                        self.processSavegameFoldername(self.ids.savegame_foldername_btn)
                    else: print('Not a Folder')
                else: print('Folder !Exist')
            else: failChain()
        writeInformation()
        self.valueInit()

    def processSavegameFoldername(self, root):
        self.dataInit()
        foldername = self.ids.savegame_foldername.text
        workingPath = self.data[0][0:-1].replace('folderpath=', '')
        workingPath += f'\\{self.ids.savegame_foldername.text}'

        def failChain():
            self.buttonClicked(root, 'FFFFFFFF', '098978')
            root.text = 'Verify'
        if self.ids.savegame_foldername.text != '':
            if os.path.exists(workingPath):
                # checking if savegame foldername is a folder
                if os.path.isdir(workingPath):
                    # write to folderpath.txt
                    open(dataTxt, 'w').write(self.dataTxtFormatter(folderpath=self.data[0][0:-1].replace('folderpath=', ''),
                                                                   savegame_folder=foldername,
                                                                   difficult_level=self.difficult_level))
                    root.text = 'Verified'
                    self.buttonClicked(root, '51CB89', 'FFFFFFFF')
                else: failChain()
            else: failChain()
        else: failChain()

    def processDifficultLevel(self, root, default_btn_col):
        def animateButton():
            try:
                self.init_difficult_level.background_color = hex(default_btn_col)
            except Exception: pass
            try:
                self.clicked_difficult_level.background_color = hex(default_btn_col)
            except Exception: pass
            root.background_color = hex('#1F81CA')
            root.background_normal = ''
            self.clicked_difficult_level = root

        def processData():
            self.difficult_level = root.text.lower()

            def writeInformation():
                try:
                    open(dataTxt, 'w').write(self.dataTxtFormatter(folderpath=self.data[0][0:-1].replace('folderpath=', ''),
                                                                   savegame_folder=self.ids.savegame_foldername.text,
                                                                   difficult_level=self.difficult_level))
                except Exception: print('FAILED')
            writeInformation()
        animateButton()
        processData()

    def executeRequest(self):
        mainPath = self.ids.folderpath.text
        scnList, scnString = list(), str()

        def prequisiteInit():
            nonlocal scnList
            try:
                scnList = open(mainPath+'\\'+gameScn, 'r').readlines()
                return True
            except Exception: return False

        def result():
            from kivy.uix.button import Button
            from kivy.animation import Animation
            rootBl = self.ids.result
            resultBtn = self.ids.result
            executeBtn = self.ids.execute_request_btn

            def rootBlAnim():
                anim = Animation(pos=(rootBl.pos[0], rootBl.pos[1]+10), duration=.15)
                rootBl.size_hint_y = 1
                executeBtn.size_hint[1] += 1 * executeBtn.size_hint[1]
                anim.start(rootBl)

            def generatingResult():
                nonlocal resultBtn
                btnText = ['scripting success', 'scripting failed']
                btnBgCol = ['36CA45', 'CA4148']
                if self.executeSuccess:
                    resultBtn.text = btnText[0]
                    resultBtn.background_color = btnBgCol[0]
                    return btnText[0], btnBgCol[0]
                else:
                    resultBtn.text = 'scripting failed'
                    resultBtn.background_color = btnBgCol[1]
                    return btnText[1], btnBgCol[1]
            try:
                if not self.executeStatus:
                    self.oldActionBlSize = rootBl.size
                    self.ids.action_bl.size[1] += 30
                    result = Button(text=str(generatingResult()[0]),
                                    size_hint=(None, None),
                                    size=(rootBl.size[0], rootBl.size[1]),
                                    background_color=hex(generatingResult()[1]),
                                    background_normal='')
                    result.bind(on_release=lambda args1=False: self.displayResultLog(get_text=False))
                    self.ids['result'] = result
                    rootBlAnim()
                    rootBl.add_widget(result)
                else: pass
            except Exception: pass
            generatingResult()
            self.executeStatus = True

        def processRequest():
            nonlocal scnString
            self.resultLog = '' if self.resultLog != '' else ''
            try:
                if os.path.exists(mainPath):
                    self.resultLog += '[Success] Savegame Folderpath: Found\n'
                    if self.ids.savegame_foldername.text != '':
                        if os.path.exists(mainPath+'\\'+self.ids.savegame_foldername.text):
                            self.resultLog += '[Success] Savegame Foldername: Found\n'
                            if self.difficult_level != '':
                                self.resultLog += '[Success] Game Difficulty: Not Empty'
                                for val in scnList:
                                    val = val.replace('\n', '')
                                    if 'difficulty' in val:
                                        val = '\t\t{difficulty ' + self.difficult_level + '}'
                                    scnString += val + '\n'
                                open(mainPath + '\\status', 'w').write(scnString)
                                self.executeSuccess = True
                            else:
                                self.resultLog += '[Failed] Game Difficulty: Empty'
                        else:
                            self.resultLog += '[Failed] Savegame Foldername: Not Found\n'
                    else:
                        self.resultLog += '[Failed] Savegame Foldername: Not Found\n'
                else:
                    self.executeSuccess = False
                    self.resultLog += '[Failed] Savegame Folderpath: Not found\n'
                result()
            except Exception: self.executeSuccess = False

        prequisiteInit()
        processRequest()

    def displayResultLog(self, get_text):
        from kivy.factory import Factory
        popup = Factory.ResultLogPopup()
        label = popup.ids.result_log_label
        popup.open()
        try:
            label.text = self.resultLog
        except Exception as e:
            print(e)

    def appExit(self):
        MainApp().get_running_app().stop()
        print('app closed')


class Sm(ScreenManager):
    pass


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

    def build(self):
        return Sm()


if hasattr(sys, 'MEIPASS'):
    resource_add_path(os.path.join(sys._MEIPASS))
MainApp().run()

