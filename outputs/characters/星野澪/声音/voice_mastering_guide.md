# 声音样本与母带建议

- 录制: 48kHz / 24-bit WAV
- 每条样本: 8-15 秒
- 情绪覆盖: 平静 / 元气 / 认真 / 撒娇
- 目标响度: -16 LUFS (stereo), 峰值 <= -1 dBTP

```bash
ffmpeg -i raw.wav -af "highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.0:LRA=8" master.wav
ffmpeg -i master.wav -ar 48000 -ac 2 -c:a aac -b:a 192k publish.m4a
```
