
from google.cloud import speech
import os
import io
import pydub
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gcp/credentials/visual-chatbot-464090e61dce.json"



def speech2text(data,sr):
    
    # with io.open(file, "rb") as audio_file:
    #     content = audio_file.read()
    
    segment=pydub.AudioSegment(data.astype('float32').tobytes(),frame_rate=sr,channels=1,sample_width=4)
    flacIO=io.BytesIO()
    segment.export(flacIO,format='flac')
    # print(flacIO.getvalue())
    
    
    # print(au)
    audio = speech.RecognitionAudio(content=flacIO.getvalue())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=sr,
        language_code="en-US",
    )
    client = speech.SpeechClient()
    
    response = client.recognize(config=config, audio=audio)
    

    # # Each result is for a consecutive portion of the audio. Iterate through
    # # them to get the transcripts for the entire audio file.
    # print(response)
    if 'results' in response:
        return response.results
    return None
    # for result in response.results:
    #     # The first alternative is the most likely one for this portion.
    #     print("Transcript: {}".format(result.alternatives[0].transcript))

# nr_fname='recordings/test_rn.flac'
# speech2text(nr_fname)

# speech2text("/waqas/VSCode/python/project31/project/app/recordings/rec.flac",16000)