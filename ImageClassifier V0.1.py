from tkinter import *
from tkinter import filedialog
import face_recognition
import os
from shutil import copyfile
from PIL import Image
from tkinter.messagebox import showwarning,showinfo
import pathlib
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
from sys import exit

class App:
    def __init__(self, master):
        frame = Frame(master).grid(row=3, column=3)

        self.label = Label(frame, text="Name of the new folder to be created", bg='azure',font="calibri 12 bold")
        self.label.grid(row=0, column=0)

        self.textbox = Text(frame, height=1, width=10, bg='ivory2', bd=5)
        self.textbox.grid(row=0, column=1)

        self.labelopenfile = Label(frame, text="Select Sample Picture", bg='azure',font="calibri 12 bold")
        self.labelopenfile.grid(row=1, column=0)

        self.browsebutton1 = Button(frame, text="Browse", fg="teal",font="calibri 12 bold", command=self.browseimage)
        self.browsebutton1.grid(row=1, column=1)

        self.labelopenfolder = Label(frame, text="Select Target Folder", bg='azure',font="calibri 12 bold")
        self.labelopenfolder.grid(row=2, column=0)

        self.browsebutton2 = Button(frame, text="Browse", fg="teal",font="calibri 12 bold", command=self.browsefolder)
        self.browsebutton2.grid(row=2, column=1)

        self.proceedbutton = Button(frame, text="Proceed", fg="teal",font="calibri 12 bold", command=self.startprocessing)
        self.proceedbutton.grid(row=3, column=0)

        self.stopbutton = Button(frame, text="Stop", fg="red", font="calibri 12 bold",command = self.stop)
        self.stopbutton.grid(row=3, column=1)



        # starting of main code
        inputfoldername = self.textbox.get("1.0", "end-1c")
        if inputfoldername != '':
            print(inputfoldername)
        else:
            print("not given")

    def stop(self):
        showinfo("Information", "Process Terminated")
        exit(0)

    def browseimage(self):
        global filenm
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.labelfilename = Label(root, text=root.filename, bg='azure')
        self.labelfilename.grid(row=1, column=2)

        filenm = root.filename

        print(root.filename)

    def browsefolder(self):
        global folderpth
        root.folderpath = filedialog.askdirectory()
        self.labelfolderpath = Label(root, text=root.folderpath, bg='azure')
        self.labelfolderpath.grid(row=2, column=2)
        folderpth = root.folderpath
        print(root.folderpath)

    def startprocessing(self):
        inputvalue = self.textbox.get("1.0", "end-1c")
        global filenm
        global folderpth
        if inputvalue != '':
            self.labelyourname = Label(root, text=inputvalue, bg='azure')
            self.labelyourname.grid(row=0, column=2)
            print(filenm)
            print(folderpth)
        else:
            self.inputvalue = "Classifed Images"
            showwarning(title="Warning",
                        message="A Default folder with name (Classified Images)will be created if Folder name is not provided!!!")
            self.labelyourname = Label(root, text=self.inputvalue, bg='azure')
            self.labelyourname.grid(row=0, column=2)
            print(filenm)
            print(folderpth)

        path_to_sampleImage = filenm
        name_of_person = inputvalue
        Path_to_target_folder = folderpth

        basewidth = 300
        img = Image.open(path_to_sampleImage)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        path_to_sample = (Path_to_target_folder + "/Sample.jpg")
        print(path_to_sample)
        img.save(path_to_sample, 'JPEG')

        print("Image  Saved")

        # Create an encoding of sample Picture facial features that can be compared to other faces
        picture_of_me = face_recognition.load_image_file(path_to_sample, mode='RGB')
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
        # print(my_face_encoding)
        Path_to_target_folder = os.path.normpath(folderpth)
        print(Path_to_target_folder)
        directory = Path_to_target_folder

        sorteddir = directory + "\\" + name_of_person

        # Creating a new Folder with the Name provided in input
        try:
            os.mkdir(sorteddir)
        except OSError:
            print("Creation of the directory %s failed, Directory already exists" % sorteddir)
        else:
            print("Successfully created the directory %s " % sorteddir)


        #counting total number of image files in folder for progress bar
        x = 0
        for files in os.listdir(directory):
            if files.endswith('.JPG'):
                x += 1
        Totalfiles = "Total Images in folder= " + str(x)
        print(Totalfiles)

        y = 0.0   #variable to update Progress bar

        #Showing Progress Bar
        self.progress = Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate',maximum=1)
        self.progress.grid(row=4, column=0)


        # Iterate through all  pictures
        for fn in os.listdir(directory):
            if fn.endswith(".JPG"):
                #updating progress bar
                y = y + 1 / x
                self.progress['value'] = float(y)
                root.update_idletasks()
                print(y)

                file_name = fn
                print(file_name)
                actualfile = directory + "\\" + fn

                # Load this picture

                img1 = Image.open(pathlib.Path(directory + "\\" + fn))
                wpercent1 = (basewidth / float(img1.size[0]))
                hsize1 = int((float(img1.size[1]) * float(wpercent1)))
                img1 = img1.resize((basewidth, hsize1), Image.ANTIALIAS)
                img1.save('new' + fn)
                new_file_name = 'new' + fn
                new_picture = face_recognition.load_image_file(new_file_name)

                # Iterate through every face detected in the new picture
                for face_encoding in face_recognition.face_encodings(new_picture):

                    # Run the algorithm of face comparison for the detected face, with 0.5 tolerance
                    results = face_recognition.compare_faces([my_face_encoding], face_encoding, 0.5)

                    # Save the image to a separate folder if there is a match
                    if results[0] == True:
                        copyfile(actualfile, (sorteddir + "\\" + file_name))
                os.remove(new_file_name)

            else:
                continue
        showinfo("Information","Process Completed")

root = Tk()
root.wm_iconbitmap('Appicon.ico')
root.title("Image Classifier")
root.configure(background='azure')
app = App(root)
root.mainloop()
