
"""Google Cloud Text-To-Speech API sample application for synthesising texts.

Title: Creating voice audio files

Description: 
Text-to-Speech allows you to convert words and sentences into base64 encoded 
audio data of natural human speech. You can then convert the audio data into a 
playable audio file like an MP3 by decoding the base64 data. The Text-to-Speech
API accepts input as raw text or Speech Synthesis Markup Language (SSML).

This document describes how to create an audio file from either text or SSML 
input using Text-to-Speech.

These samples require that you have set up gcloud and have created and activated
a service account. For information about setting up gcloud, and also creating 
and activating a service account, see Quickstart:Text-to-Speech.

Example usage:
    python synthesize_file.py --text resources/hello.txt
    python synthesize_file.py --ssml resources/hello.ssml
"""

import argparse


def synthesize_text_file(text_file):
    """
    Synthesizes speech from the input file of text, converting it into audio data.

    You can configure the output of speech synthesis in a variety of ways, 
    including selecting a unique voice or modulating the output in pitch, 
    volume, speaking rate, and sample rate.    
    """
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    with open(text_file, "r") as f:
        text = f.read()
        input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        out.write(response.audio.content)
        print('Audio content written to file "output.mp3"')


def synthesize_ssml_file(ssml_file):
    """
    Synthesizes speech from the input file of ssml, converting it into audio data.

    Using SSML in your audio synthesis request can produce audio that is more 
    similar to natural human speech. Specifically, SSML gives you finer-grain 
    control over how the audio output represents pauses in the speech or how 
    the audio pronounces dates, times, acronyms, and abbreviations.
    
    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    with open(ssml_file, "r") as f:
        ssml = f.read()
        input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="The text file from which to synthesize speech.")
    group.add_argument("--ssml", help="The ssml file from which to synthesize speech.")

    args = parser.parse_args()

    if args.text:
        synthesize_text_file(args.text)
    else:
        synthesize_ssml_file(args.ssml)    
