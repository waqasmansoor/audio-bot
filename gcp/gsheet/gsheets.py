import pygsheets
import os


REGISTRY="all_bot_sheets"
A1=f'Total Entries:{0}'
STEP=4
ADMIN='wikyversatile@gmail.com'

class GSheets():
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcp/credentials/visual-chatbot-464090e61dce.json"
    gc = pygsheets.authorize(service_file=os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
# Create empty dataframe
# df = pd.DataFrame()
    def __init__(self):
        self.total_entries=0
        

    def SheetExist(self,sheet):
        try:
            self.sh = self.gc.open(sheet)
            return True

        except pygsheets.exceptions.SpreadsheetNotFound as e:
            return False

    def createSheet(self,sheet):
        self.sh = self.gc.create(sheet)
        self.shareSheet()
    
    def shareSheet(self):
        self.sh.share(ADMIN,role='commenter',type='user')

    def getWSheet(self,sheet,num):
        wks = sheet[num]
        return wks
    
    def updateValueWithArray(self,wks,r,val):
        wks.update_value(r,val)

    def getValues(self,wks,start,end,returnas='matrix'):
        # values_mat = wks.get_values(start=(1,1), end=(20,20), returnas='matrix')
        values_mat = wks.get_values(start=start, end=end, returnas=returnas)
        return values_mat

    def getCellValue(self,wks,addr):
        c1=wks.cell(addr)
        return c1.value

    def incTotalEntries(self,wks):
        
        self.total_entries=self.total_entries+1
        c1=wks.cell("A1")
        c1.value=A1[:-1]+str(self.total_entries)
    
    def updateTotalEntries(self,wks,val):
        c1=wks.cell("A1")
        c1.value=A1[:-1]+str(val)
    
    def insertTotalEntriesInSheet(self,sheet):
        print(sheet)
        sh=self.gc.open(str(sheet))
        wks=self.getWSheet(sh,0)
        self.updateTotalEntries(wks,0)

    def register_gsheet(self,sid):
        try:
            
            sh = self.gc.open(REGISTRY)
            
            wks = sh[0]
            
            cv=self.getCellValue(wks,'A1')
            
            te=int(cv[14:])
            
            self.updateValueWithArray(wks,'A'+str((te+1)*2),str(sid))#Add ID to the REGISTRY
            
            self.updateTotalEntries(wks,te+1)#UPDATE REGISTRY ENTRIES
            # self.insertTotalEntriesInSheet(sub_sh.title)
            return False
        except:
            return True




# gs=GSheets("080d61d1230549f7ae2fdf922e3665e3")
# gs.sh.delete()
# print(gs.sh.id)
# print(gs.sh.title)
# print(gs.sh.id)
# gs.sh.share(ADMIN,role='commenter',type='user')
# wks=gs.getWSheet(gs.sh,0)
# gs.updateTotalEntries(wks,0)
# gs.sh.del_worksheet(wks)
# gs.updateTotalEntries(wks,0)
# c1=wks.cell("A1")
# print(c1.value[14:])
# if c1.value[14] == ':':
#     te=int(c1.value[-1])
# else:
#     te=int(c1.value[-2:-1])
# print(te)


# print(gs.getValues(wks,'A1','A5'))
# print(gs)
# gs=GSheets(SHEET)
# wks=gs.getSheet(0)
# gs.sh.title='new title'
# print(gs.sh.id)
# print(gs.sh.share('wikyversatile@gmail.com', role='commenter', type='user'))
# print(gs.getCellValue(wks,'A1'))
# vals=gs.getValues(wks,(4,1),(20,1))
# print(vals)
# gs.sh.share('', role='reader', type='anyone')

# while True:
#     te=gs.total_entries
#     q=str(input('ask\n'))
#     a=str(input('ans?\n'))
#     gs.updateValueWithArray(wks,'A'+str((te+1)*STEP),q)
#     gs.updateValueWithArray(wks,'E'+str((te+1)*STEP),a)
#     gs.updateTotalEntries(wks)



# print(vals)
# for val in vals[0]:

#     if val == '':
#         print("empty")
#     else:
#         print(val)
