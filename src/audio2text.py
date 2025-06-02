import os
import requests
import warnings
import whisper
from typing import Any, Dict, List, cast
from urllib.parse import urlparse

# ignore user warning regarding floats
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class Audio2Text:
    """
    A class to handle downloading audio from a URL and transcribing it into
    utterance-level segments using OpenAI's Whisper model.
    
    Attributes:
        model (whisper.model.Whisper): The Whisper model used for transcription.
    """

    def __init__(self, model_size: str = 'base'):
        """
        Initializes the Audio2Text object with a specified Whisper model size.

        Args:
            model_size (str): The size of the Whisper model to load (e.g., 'tiny', 'base', 'small', 'medium', 'large').
        """
        self.model = whisper.load_model(model_size)


    def get_audio_filename_from_url(self, url: str) -> str:
        """
        Parse the url for the audio filename.

        Args:
            url (str): The URL of the audio file to download.

        Returns:
            str: The audio filename
        """
        parsed_url = urlparse(url)
        audio_filename = os.path.basename(parsed_url.path)
        return audio_filename


    def download_audio(self, url: str, filename: str = 'audio.mp3') -> str:
        """
        Downloads an audio file from a given URL and saves it locally.

        Args:
            url (str): The URL of the audio file to download.
            filename (str): The name to use for the saved audio file.

        Returns:
            str: The path to the saved audio file.
        """
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=65536):
            #for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)
        return filename


    def transcribe(self, filepath: str, delete_file: bool = True) -> List[Dict]:
        """
        Transcribes the audio file into utterance-level segments using the Whisper model.

        Args:
            filepath (str): The path to the audio file to transcribe.

        Returns:
            List[Dict]: A list of dictionaries, each containing metadata for one utterance:
                - whisper_segment_id (int): Whisper segment identifier.
                - start (float): Start time of the utterance in seconds.
                - end (float): End time of the utterance in seconds.
                - text (str): Transcribed text of the utterance.

        Raises:
            RuntimeError: If ffmpeg is not installed or if transcription fails.
        """
        utterances = []
        try:
            result = self.model.transcribe(filepath)
        except FileNotFoundError as e:
            if 'ffmpeg' in str(e):
                raise RuntimeError(
                    "ffmpeg not found. Please install ffmpeg and ensure it is available on your system's PATH."
                ) from e
            raise
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {e}") from e
        else:
            for seg in result.get("segments", []):  
                seg = cast(Dict[str, Any], seg)
                utterances.append({
                    "whisper_segment_id": seg["id"],
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip()
                })
            return utterances
        finally:
            if delete_file and os.path.exists(filepath):
                os.remove(filepath)


def main():
    """
    Demonstrates how to use the Audio2Text class to download and transcribe
    a podcast episode into utterance-level segments.
    """
    # example podcast episode mp3 url
    url = "https://www.podtrac.com/pts/redirect.mp3/pdst.fm/e/chrt.fm/track/524GE/traffic.megaphone.fm/VMP3400936095.mp3?updated=1734638337"

    # instantiate the transcriber
    transcriber = Audio2Text(model_size="base")

    # step 1: download the audio file
    audio_file = transcriber.download_audio(url, \
                                            filename=transcriber.get_audio_filename_from_url(url))
    print(f"Downloaded audio to: {audio_file}")

    # step 2: transcribe the audio
    utterances = transcriber.transcribe(audio_file)

    # step 3: print the first few utterances
    print("\n--- Transcript Segments (First 3) ---")
    for seg in utterances[:3]:
        print(f"[{seg['start']} - {seg['end']}] {seg['text']}")

if __name__ == "__main__":
    main()
