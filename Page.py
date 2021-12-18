import importlib.metadata
import tkinter as tk
import PIL.Image
import PIL.ImageTk
import tkinter.messagebox
import tkinter.filedialog
import Capsule as cap

BG_CLR = '#282828'
TEXT_CLR = '#f8f8f8'
HEADER_CLR = '#a050c0'
BORDER_CLR = '#a8a8a8'


class Page:
    def __init__(self, window):
        self.window = window
        self.imgFile = ''
        self.cap = cap.Capsule()
        self.window.title('Crypt-O-Card')
        self.window.geometry('1000x600')
        self.window.resizable(0, 0)
        self.window.config(bg=BG_CLR)

        self.mainMenu = tk.Menu(self.window,
                                bg=HEADER_CLR, fg=TEXT_CLR,
                                activebackground=BG_CLR,
                                activeforeground=TEXT_CLR,
                                activeborderwidth=0,
                                font=('Script', 11, 'bold'),
                                tearoff=0, bd=0)

        self.mainMenu.add_command(label='Encrypt',command=self.encryptTab)
        self.mainMenu.add_command(label='Decrypt',command=self.decryptTab)
        self.mainMenu.add_command(label='About')

        self.window.config(menu=self.mainMenu)

        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=15)
        self.window.columnconfigure(0, weight=1)

        self.headerFrm = tk.Frame(self.window, bg=BG_CLR)
        self.bodyFrm = tk.Frame(self.window, bg=BG_CLR)

        self.headerFrm.grid(row=0, column=0, sticky=tk.NSEW)
        self.bodyFrm.grid(row=1, column=0, sticky=tk.NSEW)

        '''=============================== Header Frame =============================='''
        self.headerFrm.rowconfigure(0, weight=1)
        self.headerFrm.columnconfigure(0, weight=1)

        self.header = tk.Label(self.headerFrm,
                               text='Crypt-O-Card',
                               font=('Courier', 72, 'bold'),
                               relief=tk.FLAT,
                               bg=BG_CLR, fg=HEADER_CLR,
                               highlightbackground=BG_CLR,
                               highlightthickness=2,
                               anchor=tk.CENTER
                               )
        self.header.grid(row=0, column=0, sticky=tk.NSEW)

        '''============================= Header Frame End ============================'''

        '''=============================== Body Frame =============================='''
        self.bodyFrm.rowconfigure(0, weight=1)
        self.bodyFrm.columnconfigure(0, weight=1)
        self.bodyFrm.columnconfigure(1, weight=1)

        self.bodyFrmSub1 = tk.Frame(self.bodyFrm, bg=BG_CLR)
        self.bodyFrmSub2 = tk.Frame(self.bodyFrm, bg=BG_CLR)

        self.frmOnLeft1 = tk.Frame(self.bodyFrmSub2, bg=BG_CLR)
        self.frmOnLeft2 = tk.Frame(self.bodyFrmSub2, bg=BG_CLR)
        self.frmOnLeft3 = tk.Frame(self.bodyFrmSub2, bg=BG_CLR)

        self.browseLbl = tk.Label(self.bodyFrmSub1,
                                  text="Upload a Image ",
                                  bg=BG_CLR, fg=TEXT_CLR,
                                  font=('Script', 11, 'bold'))

        self.browseBtn = tk.Button(self.bodyFrmSub1,
                                   text='Browse a file',
                                   bg=BG_CLR, fg=TEXT_CLR,
                                   relief=tk.FLAT,
                                   activebackground=HEADER_CLR,
                                   activeforeground=TEXT_CLR,
                                   font=('Script', 11, 'bold'),
                                   command=self.browseFile)

        self.validateBtn = tk.Button(self.bodyFrmSub1,
                                     text='Validate',
                                     bg=BG_CLR, fg=TEXT_CLR,
                                     relief=tk.FLAT,
                                     activebackground=HEADER_CLR,
                                     activeforeground=TEXT_CLR,
                                     font=('Script', 11, 'bold'),
                                     command=self.validateImgFile,
                                     state=tk.DISABLED)

        self.previewBtn = tk.Button(self.bodyFrmSub1,
                                    text='Preview',
                                    bg=BG_CLR, fg=TEXT_CLR,
                                    relief=tk.FLAT,
                                    activebackground=HEADER_CLR,
                                    activeforeground=TEXT_CLR,
                                    font=('Script', 11, 'bold'),
                                    command=self.previewImg,
                                    state=tk.DISABLED)

        self.textbox = tk.Text(self.bodyFrmSub1,
                               bg='#444', fg=TEXT_CLR,
                               highlightthickness=0,
                               font=('Script', 11),
                               bd=0,
                               width=60,
                               height=20)

        self.massageLbl = tk.Label(self.bodyFrmSub1,
                                   text="Enter Your Massage Here ",
                                   bg=BG_CLR, fg=TEXT_CLR,
                                   font=('Script', 11, 'bold'))

        self.massageCount = tk.Label(self.bodyFrmSub1,
                                     text='count : 0/65536',
                                     bg=BG_CLR, fg=TEXT_CLR,
                                     font=('Script', 11, 'bold'))

        self.passwrdLbl = tk.Label(self.frmOnLeft2,
                                   text='Enter your Password :',
                                   bg=BG_CLR, fg=TEXT_CLR,
                                   font=('Script', 11, 'bold'))

        self.passwrdLbl2 = tk.Label(self.frmOnLeft2,
                                    text='Re-enter your Password : ',
                                    bg=BG_CLR, fg=TEXT_CLR,
                                    font=('Script', 11, 'bold'))

        self.passwrd = tk.Entry(self.frmOnLeft2,
                                bg='#444', fg=TEXT_CLR,
                                highlightthickness=0,
                                font=('Script', 11),
                                bd=0,
                                width=32,
                                show='*')

        self.passwrd2 = tk.Entry(self.frmOnLeft2,
                                 bg='#444', fg=TEXT_CLR,
                                 highlightthickness=0,
                                 font=('Script', 11),
                                 bd=0,
                                 width=32,
                                 show='*')

        self.encryptBtn = tk.Button(self.frmOnLeft3,
                                    text='Encrypt',
                                    bg='#008000', fg=TEXT_CLR,
                                    relief=tk.FLAT,
                                    highlightbackground='#008000',
                                    activebackground=TEXT_CLR,
                                    activeforeground='#008000',
                                    font=('Script', 36, 'bold'),
                                    state=tk.DISABLED,
                                    command=self.encryptImg)

        self.decryptBtn = tk.Button(self.frmOnLeft3,
                                    text='Decrypt',
                                    bg='#de0000', fg=TEXT_CLR,
                                    relief=tk.FLAT,
                                    highlightbackground='#de0000',
                                    activebackground=TEXT_CLR,
                                    activeforeground='#de0000',
                                    font=('Script', 36, 'bold'),
                                    state=tk.DISABLED,
                                    command=self.decryptImg)

        '''============================= Body Frame End ============================'''

    def encryptTab(self):

        for widgets in self.window.winfo_children():
            widgets.destroy()
        self.__init__(self.window)

        self.bodyFrmSub1.grid(row=0, column=0, sticky=tk.NSEW)
        self.bodyFrmSub2.grid(row=0, column=1, sticky=tk.NSEW)

        self.frmOnLeft1.grid(row=0, column=0, sticky=tk.NSEW)
        self.frmOnLeft2.grid(row=1, column=0, sticky=tk.NSEW)
        self.frmOnLeft3.grid(row=2, column=0, sticky=tk.NSEW)

        self.bodyFrmSub1.rowconfigure(0, weight=1)
        self.bodyFrmSub1.rowconfigure(1, weight=1)
        self.bodyFrmSub1.rowconfigure(2, weight=1)
        self.bodyFrmSub1.columnconfigure(0, weight=1)
        self.bodyFrmSub1.columnconfigure(1, weight=1)
        self.bodyFrmSub1.columnconfigure(2, weight=1)

        self.browseLbl.grid(row=0, column=0, sticky=tk.W, padx=5)

        self.browseBtn.grid(row=0, column=1, padx=5)

        self.previewBtn.grid(row=0, column=2, sticky=tk.E, padx=5)

        self.massageLbl.grid(row=1, column=0, sticky=tk.SW, padx=5)

        self.massageCount.grid(row=1, column=2, sticky=tk.SE, padx=5)

        self.textbox.bind('<KeyRelease>', self.wordCount)
        self.textbox.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=(5,15))

        self.bodyFrmSub2.rowconfigure(0, weight=1)
        self.bodyFrmSub2.rowconfigure(1, weight=1)
        self.bodyFrmSub2.rowconfigure(2, weight=1)
        self.bodyFrmSub2.columnconfigure(0, weight=1)

        self.frmOnLeft2.columnconfigure(0, weight=1)

        self.frmOnLeft3.rowconfigure(0, weight=1)
        self.frmOnLeft3.columnconfigure(0, weight=1)

        self.passwrdLbl.grid(row=0, column=0, sticky=tk.W, padx=5)
        self.passwrd.bind('<KeyRelease>', self.passStrength)
        self.passwrd.grid(row=1, column=0, sticky=tk.EW, padx=5)

        self.passwrdLbl2.grid(row=2, column=0, sticky=tk.W, padx=5)
        self.passwrd2.bind('<KeyRelease>', self.confirmPass)
        self.passwrd2.bind('<FocusIn>', self.confirmPass)
        self.passwrd2.grid(row=3, column=0, sticky=tk.EW, padx=5)

        self.encryptBtn.grid(row=0, column=0, sticky=tk.NSEW, padx=15, pady=15)

    def enableEncrypt(self):
        global tail, imgFlag, passFlag
        passFlag = imgFlag = False
        extnList = ['png', 'jpeg', 'jpg', 'bmp', 'tiff', 'tif']
        if (len(self.imgFile) > 3 and len(self.textbox.get('1.0', 'end-1c')) > 2):
            tail = self.imgFile.split('/')[-1].split('.')[-1]
            for x in extnList:
                if x == tail:
                    imgFlag = True
                    break
            if (self.passwrd.get() == self.passwrd2.get() and len(self.passwrd.get())>4):
                passFlag = True

        if (imgFlag and passFlag):
            self.encryptBtn.config(state=tk.NORMAL)
        else:
            self.encryptBtn.config(state=tk.DISABLED)

    def encryptImg(self):
        try:
            self.cap.setText(self.textbox.get('1.0','end-1c'))
            self.cap.setPassword(self.passwrd.get())
            self.cap.combineCardWithText()
            self.cap.card.saveCard()
            tk.messagebox.showinfo('Info','Your Encrypted File has been saved.\n'
                                          'Please find your file in encrypted folder.\n'
                                          'Thank You for using Cryp-O-Card')
        except:
            tk.messagebox.showerror("Error",'Some error occur please try again later')

    def decryptTab(self):

        for widgets in self.window.winfo_children():
            widgets.destroy()
        self.__init__(self.window)

        self.bodyFrmSub1.grid(row=0, column=0, sticky=tk.NSEW)
        self.bodyFrmSub2.grid(row=0, column=1, sticky=tk.NSEW)

        self.frmOnLeft1.grid(row=0, column=0, sticky=tk.NSEW)
        self.frmOnLeft2.grid(row=1, column=0, sticky=tk.NSEW)
        self.frmOnLeft3.grid(row=2, column=0, sticky=tk.NSEW)

        self.bodyFrmSub1.rowconfigure(0, weight=1)
        self.bodyFrmSub1.rowconfigure(1, weight=1)
        self.bodyFrmSub1.rowconfigure(2, weight=1)
        self.bodyFrmSub1.columnconfigure(0, weight=1)
        self.bodyFrmSub1.columnconfigure(1, weight=1)
        self.bodyFrmSub1.columnconfigure(2, weight=1)

        self.browseLbl.grid(row=0, column=0, sticky=tk.W, padx=5)

        self.browseBtn.grid(row=0, column=1, padx=5)

        self.previewBtn.grid(row=0, column=2, sticky=tk.E, padx=5)

        self.massageLbl.config(text='Extracted Text :')
        self.massageLbl.grid(row=1, column=0, sticky=tk.SW, padx=5)

        self.validateBtn.grid(row=1, column=2, padx=5, sticky=tk.E)

        # self.textbox.config(state=tk.DISABLED)
        self.textbox.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW, padx=5, pady=(5,15))

        self.bodyFrmSub2.rowconfigure(0, weight=1)
        self.bodyFrmSub2.rowconfigure(1, weight=1)
        self.bodyFrmSub2.rowconfigure(2, weight=1)
        self.bodyFrmSub2.columnconfigure(0, weight=1)

        self.frmOnLeft2.columnconfigure(0, weight=1)

        self.frmOnLeft3.rowconfigure(0, weight=1)
        self.frmOnLeft3.columnconfigure(0, weight=1)

        self.passwrdLbl.grid(row=0, column=0, sticky=tk.W, padx=5)
        self.passwrd.grid(row=1, column=0, sticky=tk.EW, padx=5)

        self.decryptBtn.grid(row=0, column=0, sticky=tk.NSEW, padx=15, pady=15)

    def decryptImg(self):
        if(not self.cap.authenticate(self.passwrd.get())):
            tk.messagebox.showerror('Stop','Password is incorrect')
            return
        try:
            self.cap.separateCardFromText(self.passwrd.get())
            self.textbox.insert(tk.END,self.cap.text)
            print(self.cap.text)
        except:
            tk.messagebox.showerror("Error",'Some error occur please try again later')


    def validateImgFile(self):
        if(self.cap.checkValidity()):
            self.decryptBtn.config(state=tk.NORMAL)
        else:
            tk.messagebox.showerror('Error','Your selected file is not encrypted')


    def browseFile(self):
        try:
            imgFile = tk.filedialog.askopenfilename(initialdir='~/Documents/',
                                                    title='Select a file',
                                                    filetypes=(('All Files', '*.*'),
                                                               ('PNG', '*.png'),
                                                               ('JPG', '*.jp*'),
                                                               ('BMP', '*.bmp'),
                                                               ('TIFF', '*.tif*')))

            if (len(imgFile) > 3):
                self.imgFile = imgFile
                imgFile = imgFile.split('/')[-1]
                if(len(imgFile)>10):
                    imgFile = imgFile[:10]+'...'
                self.browseLbl.config(text='Uploaded File : ' + imgFile)
                self.cap.card.uploadCard(self.imgFile)
                self.previewBtn.config(state=tk.NORMAL)
                self.validateBtn.config(state=tk.NORMAL)
            self.enableEncrypt()
        except:
            tk.messagebox.showerror('Error','Please Check Your file type...')

    def previewImg(self):
        global imgPrevWin
        try:
            imgPrevWin = tk.Toplevel()
            imgPrevWin.title('Image Preview')
            img = PIL.ImageTk.PhotoImage(PIL.Image.open(self.imgFile))
            imgContainer = tk.Label(imgPrevWin,
                                    image=img,
                                    relief=tk.FLAT,
                                    highlightbackground=BG_CLR,
                                    bg=BG_CLR,
                                    bd=0)
            imgContainer.image = img
            imgContainer.pack()
        except:
            imgPrevWin.destroy()
            tk.messagebox.showerror("Can't Open File", 'Your file is not opening... '
                                                       '\nPlease check filetype and try again...')

    def wordCount(self, event):
        self.massageCount.config(text='Count : ' + str(len(self.textbox.get('1.0', 'end-1c'))) + '/65536')
        self.enableEncrypt()

    def passStrength(self, event):
        length = len(self.passwrd.get())
        if (length > 16):
            grade = 'Stronger'
        elif (length > 10):
            grade = 'Strong'
        elif (length > 5):
            grade = 'Average'
        elif (length > 0):
            grade = 'Weak'
        else:
            grade = ''

        self.passwrdLbl.config(text='Enter your Password : ' + grade)
        self.enableEncrypt()

    def confirmPass(self, event):
        if (self.passwrd.get() == self.passwrd2.get()):
            self.passwrdLbl2.config(text='Re-enter your Password : Valid')
            self.enableEncrypt()
        else:
            self.passwrdLbl2.config(text='Re-enter your Password : ')
            self.enableEncrypt()


if __name__ == "__main__":
    root = tk.Tk()

    p =Page(root)
    #p.encryptTab()
    #p.decryptTab()

    root.mainloop()
