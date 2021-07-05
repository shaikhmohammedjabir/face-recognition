"""
face recognition gui interface
:author shaikh jabir mohammed
"""

from tkinter import Tk,PhotoImage,Frame,Button,Label,Entry,Listbox,Scrollbar,GROOVE,LEFT,IntVar,NW,SE,EXTENDED,Y
from recognize import Recognize
from os import listdir
from shutil import rmtree
from cv2 import error

class Admin(Tk):
    __secondary_frame=None
    __list_box=None
    def __init__(self):
        """initial main GUI"""
        self.recognize = Recognize()
        super().__init__(className=" FACE RECOGINITION")
        icon=PhotoImage(file='style/recog.png')
        self.iconphoto(True,icon)
        self.resizable(False, False)
        self.geometry('600x420+{}+{}'.format(self.winfo_screenwidth()//3,self.winfo_screenheight()//3))

        main_frame=Frame(self,borderwidth=2,relief=GROOVE)

        recognize=Button(main_frame,image=icon,bd=0)
        recognize.bind('<Button-1>', self.detectFace)
        recognize.bind('<Button-2>', self.detectFace)
        recognize.bind('<KP_Enter>', self.detectFace)
        recognize.bind('<Return>', self.detectFace)
        recognize.bind('<space>', self.detectFace)
        recognize.pack()

        add_user_img=PhotoImage(file='style/add.png')
        add_user=Button(main_frame,image=add_user_img,bd=0)
        add_user.bind('<Button-1>',self.addUser)
        add_user.bind('<Button-2>',self.addUser)
        add_user.bind('<KP_Enter>',self.addUser)
        add_user.bind('<Return>',self.addUser)
        add_user.bind('<space>',self.addUser)
        add_user.pack()

        delete_user_img=PhotoImage(file='style/delete.png')
        delete_user=Button(main_frame,image=delete_user_img,bd=0)
        delete_user.bind('<Button-1>', self.deleteUser)
        delete_user.bind('<Button-2>', self.deleteUser)
        delete_user.bind('<KP_Enter>', self.deleteUser)
        delete_user.bind('<Return>', self.deleteUser)
        delete_user.bind('<space>', self.deleteUser)
        delete_user.pack()

        list_user_img=PhotoImage(file='style/list.png')
        list_user=Button(main_frame,image=list_user_img,bd=0)
        list_user.bind('<Button-1>', self.listUser)
        list_user.bind('<Button-2>', self.listUser)
        list_user.bind('<KP_Enter>', self.listUser)
        list_user.bind('<Return>', self.listUser)
        list_user.bind('<space>', self.listUser)
        list_user.pack()
        main_frame.pack(side=LEFT)

        Admin.secondary_frame=Frame(self)
        Admin.secondary_frame.pack(side=LEFT)
        Label(Admin.secondary_frame, text="press F5 to regenerate model \nof an existing members", fg='green', font=('', 14)).pack()

        self.bind('<Escape>',lambda x:self.destroy())
        self.bind('<F5>',lambda x:self.recognize.createModel())
        self.mainloop()
    def clear(self):
        """clear the previous packed widget"""
        if widget:=Admin.secondary_frame.winfo_children():
            for x in widget:
                x.destroy()

    def detectFace(self,event):
        self.clear()
        try:
            self.recognize.recognize()
        except error:
            Label(Admin.secondary_frame,text="MAKE SURE CAMERA IS CONNECTED",fg='red',font=('',14)).pack()

    def addUser(self,event):
        """add new member"""
        self.clear()
        no_of_samples=IntVar()
        no_of_samples.set(30)
        Label(Admin.secondary_frame,text="name",font=('',14)).grid(row=0,column=0,sticky=NW)
        Label(Admin.secondary_frame,text="address",font=('',14)).grid(row=1,column=0,sticky=NW)
        Label(Admin.secondary_frame,text="samples ",font=('',14)).grid(row=2,column=0,sticky=NW)
        user_name=Entry(Admin.secondary_frame,highlightcolor='green',font=('',14))
        user_name.grid(row=0,column=1)
        user_address=Entry(Admin.secondary_frame,highlightcolor='green',font=('',14))
        user_address.grid(row=1,column=1)
        Entry(Admin.secondary_frame,highlightcolor='green',textvariable=no_of_samples,font=('',14)).grid(row=2,column=1)

        proceed=Button(Admin.secondary_frame,text='proceed',activebackground='gray')
        proceed.bind('<Button-1>', lambda x: self.recognize.captureSample(user_name.get(), no_of_samples.get()))
        proceed.bind('<Button-2>', lambda x: self.recognize.captureSample(user_name.get(), no_of_samples.get()))
        proceed.bind('<KP_Enter>', lambda x: self.recognize.captureSample(user_name.get(), no_of_samples.get()))
        proceed.bind('<Return>', lambda x: self.recognize.captureSample(user_name.get(), no_of_samples.get()))
        proceed.bind('<space>', lambda x: self.recognize.captureSample(user_name.get(), no_of_samples.get()))
        proceed.grid(row=4,column=1,pady=20,sticky=SE)

    def deleteUser(self,event):
        try:
            for person in Admin.__list_box.selection_get().split('\n'):
                rmtree('person/' + person)
        except (AttributeError,FileNotFoundError):
            pass
        self.listUser(None)

    def listUser(self,event):
        self.clear()
        list_box = Listbox(Admin.secondary_frame, height=26, width=59,selectmode=EXTENDED)
        for index, person in enumerate(sorted(listdir('person'))):
            list_box.insert(index, person)
        list_box.pack(side=LEFT, expand=True)
        list_box.focus_set()

        scroll = Scrollbar(Admin.secondary_frame, command=list_box.yview)
        scroll.pack(side=LEFT, fill=Y)
        list_box.config(yscrollcommand=scroll.set)
        Admin.__list_box = list_box


if __name__ == '__main__':
    Admin()
