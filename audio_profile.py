
"""Google Cloud Text-To-Speech API sample application for audio profile.

Title: Synthesize text with audio profiles 

Description: 
Synthesize text, specifying an audio profile to optimize the synthetic speech 
for playback on different types of hardware.

Available audio profiles:
https://cloud.google.com/text-to-speech/docs/audio-profiles#available_audio_profiles

Example usage:
    python audio_profile.py --text "hello" --effects_profile_id
        "telephony-class-application" --output "output.mp3"
"""

import argparse

def synthesize_text_with_audio_profile(text, output, effects_profile_id):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(language_code="en-US")

    # Note: you can pass in multiple effects_profile_id. They will be applied
    # in the same order they are provided.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=[effects_profile_id],
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "%s"' % output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter 
    )
    parser.add_argument("--output", help="The output mp3 file.")
    parser.add_argument("--text", help="The text from which to synthesize speech.")
    parser.add_argument(
        "--effects_profile_id", help="The audio effects profile id to be applied."
    )

    args = parser.parse_args()

    synthesize_text_with_audio_profile(args.text, args.output, args.effects_profile_id)

