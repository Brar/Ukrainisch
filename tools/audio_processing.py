# SPDX-License-Identifier: MIT
"""Shared audio processing for the recording tools.

Trims leading and trailing silence, evens out the loudness and saves MP3, so
recordings made with `record_audio.py` and recordings imported with
`import_recordings.py` sound the same.
"""

import os

import numpy as np
import soundfile as sf

FRAME_SECONDS = 0.01        # analysis frame for silence detection
SPEECH_BELOW_PEAK_DB = 35   # frames quieter than this below the loudest frame count as silence
MIN_SPEECH_DB = -50         # if even the loudest frame is below this, nothing was said
PAD_START_SECONDS = 0.10    # silence kept before the first sound
PAD_END_SECONDS = 0.20      # silence kept after the last sound
FADE_SECONDS = 0.01         # fade in/out against clicks at the cut points
TARGET_RMS_DB = -20.0       # loudness of the spoken part after normalisation
MAX_PEAK_DB = -1.0          # never louder than this
CLIP_LEVEL = 0.99           # input peak at or above this means the take clipped


def db(value):
    return 20 * np.log10(max(value, 1e-12))


def trim_silence(audio, samplerate):
    """Cut leading and trailing silence. Returns None if no speech was found."""
    frame = int(FRAME_SECONDS * samplerate)
    count = len(audio) // frame
    if count == 0:
        return None
    frames = audio[: count * frame].reshape(count, frame)
    levels = 20 * np.log10(np.sqrt(np.mean(frames**2, axis=1)) + 1e-12)
    if levels.max() < MIN_SPEECH_DB:
        return None
    speech = np.flatnonzero(levels > levels.max() - SPEECH_BELOW_PEAK_DB)
    start = max(0, speech[0] * frame - int(PAD_START_SECONDS * samplerate))
    end = min(len(audio), (speech[-1] + 1) * frame + int(PAD_END_SECONDS * samplerate))
    trimmed = audio[start:end].copy()
    fade = min(int(FADE_SECONDS * samplerate), len(trimmed) // 2)
    if fade:
        ramp = np.linspace(0.0, 1.0, fade, dtype=trimmed.dtype)
        trimmed[:fade] *= ramp
        trimmed[-fade:] *= ramp[::-1]
    return trimmed


def normalise(audio, samplerate):
    """Scale the take so the spoken part has the target loudness, without clipping."""
    frame = int(FRAME_SECONDS * samplerate)
    count = max(1, len(audio) // frame)
    frames = audio[: count * frame].reshape(count, -1)
    rms = np.sqrt(np.mean(frames**2, axis=1))
    spoken = rms[20 * np.log10(rms + 1e-12) > db(rms.max()) - SPEECH_BELOW_PEAK_DB]
    gain = 10 ** ((TARGET_RMS_DB - db(np.sqrt(np.mean(spoken**2)))) / 20)
    peak = np.max(np.abs(audio)) * gain
    if peak > 10 ** (MAX_PEAK_DB / 20):
        gain *= 10 ** (MAX_PEAK_DB / 20) / peak
    return (audio * gain).astype("float32")


def process(raw, samplerate):
    """Turn a raw take into the file content. Returns (audio or None, warnings)."""
    warnings = []
    if len(raw) and np.max(np.abs(raw)) >= CLIP_LEVEL:
        warnings.append("The take clipped (too loud). Lower the input gain and redo it.")
    audio = trim_silence(raw - np.mean(raw) if len(raw) else raw, samplerate)
    if audio is None:
        return None, warnings + ["No speech detected. Check the microphone and the input channel."]
    if len(audio) / samplerate > 8:
        warnings.append("Longer than 8 s. Did the recording start too early or stop too late?")
    return normalise(audio, samplerate), warnings


def save_mp3(audio, samplerate, path):
    tmp = path.with_name(path.name + ".tmp")
    sf.write(tmp, audio, samplerate, format="MP3", subtype="MPEG_LAYER_III",
             bitrate_mode="VARIABLE", compression_level=0.2)
    os.replace(tmp, path)
