from flask import Flask, render_template,request,send_file
import soundfile as sf
import scipy.signal as sps
from gcp.audio_text.speech2text import speech2text
from gcp.audio_text.text2speech import text2speech
from openai.openai import getChatGPt_response
from gcp.gsheet.gsheets import GSheets
import threading
from utils.utils import generate_uuid
import io
import json


app=Flask(__name__)
# rec=Rec()

SAMPLE_RATE = 16000
FILE_NAME="recordings/rec.flac"
TG:threading.Thread=None
GS_ID=None

def read_audio(file):
    rec,fsf=sf.read(file)
    number_of_samples=round(len(rec) * float(SAMPLE_RATE) / fsf)
    # #  Resampling to 16k
    data=sps.resample(rec,number_of_samples)
    # sf.write(FILE_NAME,data,SAMPLE_RATE)
    return data
    # f=io.BytesIO()
    # sf.write(FILE_NAME,data,SAMPLE_RATE)
    # return f
    # sd.play(data,16000,None,blocking=False)

def async_save_response(sid,rna):
    def save(sid,rna):
        with open(f"static/files/{sid}.json", 'w', encoding='utf-8') as f:
                json.dump(rna, f, ensure_ascii=False, indent=4)
    t=threading.Thread(target=save,args=(sid,rna,))
    t.start()

def async_call_to_gsheet(sid,rna):
    def call_to_gsheet(sid,rna):
        
        gs=GSheets()
        exist=gs.SheetExist(sid)
        if not exist:
            print(f"Sheet {sid} Does not Exist")
            return
        wks=gs.getWSheet(gs.sh,0)
        cv=gs.getCellValue(wks,'A1')
        te=int(cv[14:])
        gs.updateTotalEntries(wks,te+1)
        gs.updateValueWithArray(wks,'A'+str((te+1)*4),rna['q'])
        gs.updateValueWithArray(wks,'E'+str((te+1)*4),rna['a'])
    t=threading.Thread(target=call_to_gsheet,args=(sid,rna,))
    t.start()

def async_create_and_register_gsheet(sid):
    def create_and_register_gsheet(id):
        gs=GSheets()
        err=gs.register_gsheet(id)
        if err:
            print("error in registry")
        
            
    gs=GSheets()
    exist=gs.SheetExist(sid)
    if exist:
        return
    print(f"New Sheet Created with Title: {sid}")
    gs.createSheet(sid)
    gs.insertTotalEntriesInSheet(gs.sh.title)
    t=threading.Thread(target=create_and_register_gsheet,args=(gs.sh.id,))
    t.start()
    

@app.route("/",methods=["GET","POST"])
def root():
    if request.method=="GET":
        uid=generate_uuid()
        
        
        
        return render_template("index.html",uid=str(uid))
    if request.method=="POST":
        
        resp=None
        file=None
        text=None
        sid=None
        files=request.files
        
        if 'sid' in request.form:
            
            sid=str(request.form['sid'])
            print("sid",sid)

        file=files.get('audio_data')
        
        t=async_create_and_register_gsheet(sid)
        
        if 'q' in request.form:
            text=request.form['q']
            resp=text

        elif file:        
            data=read_audio(file)
            resp=speech2text(data,SAMPLE_RATE)    
            if resp:
                resp=resp[0].alternatives[0].transcript

        if resp is not None and len(resp)>10:
            ans=getChatGPt_response(resp)
            aud=text2speech('en-US-Standard-F',str(ans))

            rna={
                'q':resp,
                'a':ans,
            }
            print('this is the question',resp)
            print('this is from chatgpt',ans)
            async_call_to_gsheet(sid,rna)
            async_save_response(sid,rna)
            return send_file(io.BytesIO(aud),mimetype="audio/wav",as_attachment=True,download_name='temp.wav')
        else:
            rna={
                    'q':"Empty",
                    'a':"Empty",
                }
            return json.dumps(rna,skipkeys=False)
            
        


if __name__== '__main__':
    # app.run(host='127.0.0.1',port=8080,debug=True)# For Development
    app.run(host='0.0.0.0',debug=False)# For Production
    """
        for local development with docker use 127.0.0.1 in the flask and in gunicorn
    """
