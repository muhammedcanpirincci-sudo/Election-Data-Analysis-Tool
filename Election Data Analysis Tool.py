from Tkinter import *   #Importing Modules
import ttk
import tkFileDialog
from clusters import *
from PIL import ImageTk,Image
class District:                                     #Creating two classes as per implementation notes
    def __init__(self, name, election_results):
        self.name = name
        self.election_results = election_results
class PoliticalParty:
    def __init__(self, acronym, election_results):
        self.acronym = acronym
        self.election_results = election_results
class DataCenter: #creating main data center class that extracts the data from the file
    def __init__(self, districts, parties):
        self.districts = districts
        self.parties = parties
    def reading(self):  #function that reads the election file
            self.acilim_main=open(tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                     filetypes=(("txt files", ".txt"), ("all files", ".*"))))
            sum = 0
            sum2 = 0
            dict_3 = {}
            mystr = ""
            dict = {}
            #those variables are for parsing data from txt file.Those are part of algorithm that we wrote so its not that much necessary.
            for i in self.acilim_main.readlines():
                sum2 = sum2 + 1
                if sum2 == 2:
                    mystr += i.rstrip()
                if i != "Kaynak: YSK\n":
                    if i == "Kis.	Parti	Aday	Oy sayisi	Oy orani\n":
                        sum = sum + 1
                    if sum == 1:
                        newlist = i.split("\t")
                        dict_3[newlist[0]] = newlist[-1].rstrip("\n")
                        if newlist[0] == "Toplam" or newlist[0] == "Gecersiz ya da bos" or newlist[
                            0] == 'Katilim orani' or \
                                newlist[0] == "BGMSZ":
                            if "Toplam" in dict_3:
                                dict_3.pop('Toplam')
                            if "Kis." in dict_3:
                                dict_3.pop('Kis.')
                            if "BGMSZ" in dict_3:
                                dict_3.pop("BGMSZ")
                            if "Gecersiz ya da bos" in dict_3:
                                dict_3.pop('Gecersiz ya da bos')
                            if "Katilim orani" in dict_3:
                                dict_3.pop("Katilim orani")
                            dict[mystr] = dict_3
                else:
                    mystr = ""
                    sum = 0
                    sum2 = 1
                    dict_3 = {}
            #Dict variable is dictinoary that parsed data from txt file.We are creating objects and filling dictinoary attributes of classes with this dictinoary.With the code below.
            for i in dict:
                for b in dict[i]:
                    object_of_districts = District(i, {b: dict[i][b]})
                    object_of_political_parties = PoliticalParty(b, {i: dict[i][b]})

                    if i not in self.districts:
                        self.districts[i] = [object_of_districts]
                    else:
                        self.districts[i].append(object_of_districts)

                    if b not in self.parties:
                        self.parties[b] = [object_of_political_parties]
                    else:
                        self.parties[b].append(object_of_political_parties)
            creating_matrix1 = open("main.txt", "w") #we are creating matrix with this variable
            newlist = [] #this variable is part of algorithm to creating matrix properly.
            for i in self.parties:
                newlist.append(i)
            creating_matrix1.write("Districts" + "\t")

            for i in newlist:
                if i == newlist[len(newlist) - 1]:
                    creating_matrix1.write(i + "\n")
                else:
                    creating_matrix1.write(i + "\t")
            for i in self.districts:
                newlist_ = []
                for_objects = []
                for b in self.districts[i]:
                    for_objects.append(b.election_results.keys()[0])
                for j in newlist:
                    if j in for_objects:
                        for c in self.districts[i]:
                            if c.election_results.keys()[0] == j:
                                newlist_.append(float(c.election_results.values()[0].replace("%","")))
                    else:
                        newlist_.append(0)
                creating_matrix1.write(i, )
                for k in newlist_:
                    creating_matrix1.write('\t%s' % k)
                creating_matrix1.write('\n')
            #at the code above,we created "main.txt",which is the matrix for clustring.
class GUI(Frame):  # Gui class that displays everything
    def __init__(self, parent):
        self.parent = parent
        self.data_center_object = DataCenter({}, {}) #creating object for data center class
        Frame.__init__(self, parent)
        self.initUI(parent)
    def initUI(self, parent):
        self.label_1 = Label(self, text="Election Data Analysis Tool v. 1.0", background="red", foreground="white",font=("Helvetica", 14, "bold"), width=80)
        self.label_1.grid(sticky=W, row=0, column=0)  # MAIN TITLE LABEL
        self.load_button = Button(self, text="Load Election Data", relief=GROOVE, width=30, height=2,background="#e1e1e1", command=self.read)
        self.load_button.grid(row=1, pady=11, sticky=W, padx=375)
        self.districts = Button(self, text='Cluster Districts', background="#e1e1e1", width=30, relief=GROOVE, height=3,command=self.display)
        self.districts.grid(row=2, sticky=W, padx=265)
        self.parties = Button(self, text='Cluster Political Parties', background="#e1e1e1", width=30, relief=GROOVE,height=3,command=self.display2)
        self.parties.grid(row=2, sticky=W, padx=487)
        self.pack()
    def display(self): #function that is called when cluster districts is clicked
        self.xscrollbar = Scrollbar(self, orient=HORIZONTAL)                            #creating display widgets
        self.xscrollbar.grid(row=4, sticky=W, ipadx=413, padx=40)
        self.yscrollbar = Scrollbar(self, orient=VERTICAL)
        self.yscrollbar.grid(row=3, sticky=W, padx=900, ipady=135)
        self.canvas = Canvas(self, height=320, width=857, background="Grey", yscrollcommand=self.yscrollbar.set,
                             xscrollcommand=self.xscrollbar.set,scrollregion=[0,0,1500,1500])
        self.canvas.grid(row=3, sticky="W", padx=40)
        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=5, sticky=W, padx=390, ipady=55)
        self.listbox = Listbox(self, yscrollcommand=self.scrollbar.set,selectmode=MULTIPLE)
        self.listbox.grid(row=5, sticky=W, padx=270)
        self.scrollbar.config(command=self.listbox.yview)
        Label(self, text='Districts:').grid(row=5, sticky=W, padx=220)
        Label(self, text="Threshold:").grid(row=5, sticky=W, padx=410)
        self.combo_box = ttk.Combobox(self, width=5, values=["0%", "1%", "10%", "20%", '30%', '40%', '50%'])
        self.combo_box.current(0)
        self.combo_box.grid(row=5, sticky=W, padx=472)
        self.refine_button = Button(self, text='Refine Analysis', relief=GROOVE, width=30, height=2,
                                    background="#e1e1e1",command=self.cluster_districts_function)
        self.refine_button.grid(row=5, sticky=W, padx=526)
        x, y, z = readfile("main.txt")      #reading the matrix file
        a = hcluster(z, distance=sim_distance)         #calling the function from clusters.py
        drawdendrogram(a, x, jpeg="picture_of_cluster.jpeg")
        img = ImageTk.PhotoImage(Image.open("picture_of_cluster.jpeg"))
        self.canvas.create_image(20, 20, anchor=NW, image=img)
        self.canvas.image = img# displaying dendogram on canvas

        for i in sorted(self.data_center_object.districts): #displaying districts in listbox
            self.listbox.insert(END, i)
    def read(self):  #function that is called to read original election file
        self.data_center_object.reading()
    def cluster_districts_function(self):#this function,creates main2,and main3.Which are going to be used for proper imaging.Either for using treshold properly.
        list=[] #this list gets listbox items
        for i in self.listbox.curselection():
         list.append(self.listbox.get(self.listbox.index(i))) #getting combo box data and adding to list for controlling.
        opening2_1=open("main2.txt","w")
        opening2_1_r = open("main2.txt", "r")
        opening2_2=open("main3.txt","w")
        opening1=open("main.txt","r")
        if len(list)!=0:  #This algorithm is for if nothing selected at listbox,you should be able to change treshold.
         for i in opening1:
             List_For_Adding_Main=i.split("\t") #L list gets persentages for comparing them  with treshold.
             List_For_Adding_Main[-1] = List_For_Adding_Main[-1].replace(List_For_Adding_Main[-1], List_For_Adding_Main[-1].rstrip())
             if List_For_Adding_Main[0] !="Districts":
                 if List_For_Adding_Main[0] in list:
                  opening2_1.write(i)
             else:
                  opening2_1.write(i)
         opening2_1.close()
         x, y, z = readfile("main2.txt")
         a = hcluster(z, distance=sim_distance)  # At this part, finally i am creating jpeg and inserting it into canvas.
         drawdendrogram(a, x, jpeg="picture_of_cluster.jpeg")
         img = ImageTk.PhotoImage(Image.open("picture_of_cluster.jpeg"))
         self.canvas.create_image(20, 20, anchor=NW, image=img)
         self.canvas.image = img#replacing dendrogram
        else:
            for i in range(len(self.data_center_object.districts)):
             list.append(self.listbox.get(i))
            for i in opening1:
                List_For_Adding_Main3 = i.split("\t")
                List_For_Adding_Main3[-1] = List_For_Adding_Main3[-1].replace(List_For_Adding_Main3[-1], List_For_Adding_Main3[-1].rstrip())
                if List_For_Adding_Main3[0] != "Districts":
                    if List_For_Adding_Main3[0] in list:
                        opening2_1.write(i)
                else:
                    opening2_1.write(i)
            opening2_1.close()
        for i in opening2_1_r.readlines():
            List_For_Proper_Adding=i.split("\t")
            List_For_Proper_Adding[-1] = List_For_Proper_Adding[-1].replace(List_For_Proper_Adding[-1], List_For_Proper_Adding[-1].rstrip())
            if List_For_Proper_Adding[0] != "Districts":
             for k in List_For_Proper_Adding:
                 if k.startswith("0") or k.startswith("1") or k.startswith("2") or k.startswith("3") or k.startswith(
                         "4") or k.startswith("5") or k.startswith("6") or k.startswith("7") or k.startswith(
                         "8") or k.startswith("9"):
                     if float(self.combo_box.get().replace("%", "")) > float(k):
                         List_For_Proper_Adding[List_For_Proper_Adding.index(k)] = "0"
             for j in range(len(List_For_Proper_Adding)):
                 if j == len(List_For_Proper_Adding) - 1:
                     opening2_2.write(List_For_Proper_Adding[j])
                 else:
                     opening2_2.write(List_For_Proper_Adding[j] + "\t")
             opening2_2.write("\n")
            else:
             opening2_2.write(i)
        opening2_1.close()
        opening2_2.close()
        x, y, z = readfile("main3.txt")
        a = hcluster(z, distance=sim_distance) #At this part, finally i am creating jpeg and inserting it into canvas.
        drawdendrogram(a, x, jpeg="picture_of_cluster.jpeg")
        img = ImageTk.PhotoImage(Image.open("picture_of_cluster.jpeg"))
        self.canvas.create_image(20, 20, anchor=NW, image=img)
        self.canvas.image = img

    def function_for_political_parties(self):#Usage of this function,for using clustring political parties.And creating reversed matrix.Which is Main22.
        acilim = open("main.txt", "r")
        acilim2 = open("Main1.txt", "w")
        acilim2_1= open("Main22.txt", "w")
        acilim2_r = open("Main1.txt", "r")
        parties = []
        districts = []
        list=[] #this list gets listbox items
        for i in self.data_center_object.parties:
            parties.append(i)
        for i in self.data_center_object.districts:
            districts.append(i)
        x, y, z = readfile("main.txt") #at this part i am rotating main matrix,and preparing it for clustring with algorithm below.
        t = rotatematrix(z)
        a = hcluster(t, distance=sim_distance)
        drawdendrogram(a, parties, jpeg="picture_of_cluster.jpeg")
        for b in self.listbox.curselection():
            list.append(self.listbox.get(self.listbox.index(b)))
        if len(list)!=0:#This algorithm is for if nothing selected at listbox,you should be able to change treshold.
         for i in acilim:
             List_for_numbers_and_districts_name=i.split() #
             if List_for_numbers_and_districts_name[0] !="Districts":
                 if List_for_numbers_and_districts_name[0] in list:
                     acilim2.write(i)
             else:
                 acilim2.write(i)
         acilim2.close()
        else:
            for i in range(len(self.data_center_object.districts)):
             list.append(self.listbox.get(i))
            for i in acilim:
                List_for_numbers_and_districts_name = i.split()
                if List_for_numbers_and_districts_name[0] != "Districts":
                    if List_for_numbers_and_districts_name[0] in list:
                        acilim2.write(i)
                else:
                    acilim2.write(i)
            acilim2.close()
        for i in acilim2_r.readlines(): #this algoritm is for making matrix controllable properly.
            List_For_Numbers_And_Districts_Name2 = i.split("\t")
            List_For_Numbers_And_Districts_Name2[-1] = List_For_Numbers_And_Districts_Name2[-1].replace(List_For_Numbers_And_Districts_Name2[-1], List_For_Numbers_And_Districts_Name2[-1].rstrip())
            if List_For_Numbers_And_Districts_Name2[0] != "Districts":
                for k in List_For_Numbers_And_Districts_Name2:
                    if k.startswith("0") or k.startswith("1") or k.startswith("2") or k.startswith("3") or k.startswith(
                            "4") or k.startswith("5") or k.startswith("6") or k.startswith("7") or k.startswith(
                        "8") or k.startswith("9"):
                        if float(self.combo_box.get().replace("%", "")) > float(k):
                            List_For_Numbers_And_Districts_Name2[List_For_Numbers_And_Districts_Name2.index(k)] = "0"
                for j in range(len(List_For_Numbers_And_Districts_Name2)):
                    if j == len(List_For_Numbers_And_Districts_Name2) - 1:
                        acilim2_1.write(List_For_Numbers_And_Districts_Name2[j])
                    else:
                        acilim2_1.write(List_For_Numbers_And_Districts_Name2[j] + "\t")
                acilim2_1.write("\n")
            else:
                acilim2_1.write(i)
        acilim2_1.close()
        x, y, z = readfile("Main22.txt")#at this part i am rotating main matrix,and making it proper for using treshold.
        t = rotatematrix(z)
        a = hcluster(t, distance=sim_distance)
        drawdendrogram(a, parties, jpeg="picture_of_cluster.jpeg")
        img = ImageTk.PhotoImage(Image.open("picture_of_cluster.jpeg"))
        self.canvas.create_image(20, 20, anchor=NW, image=img)
        self.canvas.image = img
    def display2(self):
        self.display()
        self.refine_button.configure(command=self.function_for_political_parties) #at this part i am calling display function for formatting everything,and configuring refine button for calling function_for_political_parties.At the part below, i am inserting main political parties picture to canvas.)
        parties = []
        districts = []
        for i in self.data_center_object.parties:
            parties.append(i)
        for i in self.data_center_object.districts:
            districts.append(i)
        x, y, z = readfile("main.txt")
        t = rotatematrix(z)
        a = hcluster(t, distance=sim_distance)
        drawdendrogram(a, parties, jpeg="picture_of_cluster.jpeg")
        img = ImageTk.PhotoImage(Image.open("picture_of_cluster.jpeg"))
        self.canvas.create_image(20, 20, anchor=NW, image=img)
        self.canvas.image = img
def main():  # function that runs the app by creating object of tk and third class which takes the object of tk as argument
    root = Tk()
    root.title('Clustering')
    root.geometry('950x675')
    app = GUI(root)
    root.mainloop()
main()