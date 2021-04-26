import soundfile as sf


def audioRead(path):
    """Reads an audio file from its location (path)
    Formats supported: .wav

    Returns the following information:
    data: audio data
    path: File path, name and its extension
    duration: duration of the file in seconds
    samplerate: sampling frequency in Hz
    frames: number of samples
    channels: 1 (mono) or 2 (stereo)"""
    data, samplerate = sf.read(path)
    frames = data.shape[0]
    channels = len(data.shape)
    duration = 1/samplerate*frames
    return data, samplerate, path, duration, frames, channels
