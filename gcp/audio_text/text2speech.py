import google.cloud.texttospeech as tts
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcp/credentials/visual-chatbot-464090e61dce.json"

def text2speech(voice_name,text):
    language_code="-".join(voice_name.split("-")[-2])
    text_input=tts.SynthesisInput(text=text)
    voice_params=tts.VoiceSelectionParams(language_code=language_code,name=voice_name)
    audio_config=tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client=tts.TextToSpeechClient()
    response=client.synthesize_speech(input=text_input,voice=voice_params,audio_config=audio_config)
    
    resp=response.audio_content
    # buf=np.frombuffer(resp,dtype=np.int16)
    # a=buf.astype(np.float32)

    # max=2**15
    # norm=a/np.iinfo(np.int16).max
    # print(norm)
    # print(len(norm))
    # sig=np.asarray(buf)
    
    # i=np.iinfo(sig.dtype)
    # abs_max=2**(i.bits-1)
    # offset=i.min + abs_max
    # r=(sig.astype('float64') - offset)/abs_max
    
    # print(sig.astype('float64'))
    # print(len(sig))
    # sd.play(r)
    # mem_f=io.BytesIO()
    # mem_f=io.StringIO()
    # mem_f.write(resp)
    # with open(mem_f,'wb') as out:
    #     out.write(response.audio_content)
    # sd.play(mem_f)
    return resp
    # au=pydub.AudioSegment.from_file(io.BytesIO(resp),format='wav')
    # pydub.play(au)
    # print(*au)
    
    # return resp
    # print(type(resp))
    
    




# data,rate=sf.read('test.wav')
# print(len(data))                                                                       