import librosa
import tensorflow as tf
import numpy as np
import os

print(os.listdir())
filename = "TestingSongs/1/song.ogg"
y, sr = librosa.load(filename)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
#y = y[]
#sr = (1.0*sr) / 100.0
beat = 60.0 / tempo
furie = tf.abs(tf.signal.stft(y, frame_length=2046, frame_step=int(sr*beat / 12.0), pad_end=True))
np_song = furie.numpy()
np.savetxt("TestingSongs/1/song.txt", np_song)
file = open("TestingSongs/1/beat.txt", "w")
file.write(str(beat))
file.close()