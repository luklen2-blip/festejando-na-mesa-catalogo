#!/usr/bin/env python3
"""
Motor de Renderização de Vídeo Promocional 9:16 Vertical para Festejando na Mesa
Gera animação com mão humana real, transições suaves, narração e trilha sonora.
"""

import os
import shutil
import subprocess
from PIL import Image, ImageDraw
import numpy as np

base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(base_dir)
hand_path = os.path.join(base_dir, "perfect_real_hand.png")
ffmpeg_bin = r"C:\Users\luciano\.gemini\antigravity\brain\60c9c2db-d485-4829-b419-4d3a923940e0\scratch\node_modules\ffmpeg-static\ffmpeg.exe"

desktop = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")
if not os.path.exists(desktop):
    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")

out_public_mp4 = os.path.join(project_dir, "public", "assets", "video_promo.mp4")
out_desktop_mp4 = os.path.join(desktop, "VIDEO_PROMO_FESTEJANDO_NA_MESA.mp4")

# Load base scenes
print("🎬 Carregando cenas do catálogo Festejando na Mesa...")
shot1 = Image.open(os.path.join(base_dir, "shot_1.png")).convert("RGBA")
shot2 = Image.open(os.path.join(base_dir, "shot_2.png")).convert("RGBA")
shot3 = Image.open(os.path.join(base_dir, "shot_3.png")).convert("RGBA")
shot4 = Image.open(os.path.join(base_dir, "shot_4.png")).convert("RGBA")
shot5 = Image.open(os.path.join(base_dir, "shot_5.png")).convert("RGBA")
hand = Image.open(hand_path).convert("RGBA")

W, H = 480, 854
shot1 = shot1.resize((W, H), Image.Resampling.LANCZOS)
shot2 = shot2.resize((W, H), Image.Resampling.LANCZOS)
shot3 = shot3.resize((W, H), Image.Resampling.LANCZOS)
shot4 = shot4.resize((W, H), Image.Resampling.LANCZOS)
shot5 = shot5.resize((W, H), Image.Resampling.LANCZOS)

# Prepare hand size
hand_w = int(W * 0.58)
hand_h = int(hand.height * (hand_w / hand.width))
hand_resized = hand.resize((hand_w, hand_h), Image.Resampling.LANCZOS)

fps = 25
total_duration = 20.0
total_frames = int(fps * total_duration) # 500 frames

frames_temp = os.path.join(base_dir, "temp_render_frames")
if os.path.exists(frames_temp):
    shutil.rmtree(frames_temp)
os.makedirs(frames_temp, exist_ok=True)

print(f"🚀 Renderizando {total_frames} frames em 9:16 vertical a {fps} fps...")

frame_idx = 0

# Cena 1: Vitrine Principal (0s a 3.8s) = 95 frames
s1_frames = 95
for i in range(s1_frames):
    zoom = 1.0 + (i / float(s1_frames)) * 0.04
    zw, zh = int(W * zoom), int(H * zoom)
    im_zoomed = shot1.resize((zw, zh), Image.Resampling.BILINEAR)
    x = (zw - W) // 2
    y = (zh - H) // 2
    frame = im_zoomed.crop((x, y, x + W, y + H)).copy()
    frame.convert("RGB").save(os.path.join(frames_temp, f"frame_{frame_idx:04d}.jpg"), quality=95)
    frame_idx += 1

# Cena 2: Toque com Mão Real nos Produtos (3.8s a 8.0s) = 105 frames
s2_frames = 105
for i in range(s2_frames):
    frame = shot2.copy()
    prog = min(1.0, i / 20.0)
    t = 1 - (1 - prog) ** 2
    hx = int((W + 60) + ((W * 0.45) - (W + 60)) * t)
    hy = int((H + 60) + ((H * 0.48) - (H + 60)) * t)

    tap = 0
    if 25 <= i <= 45:
        tap = int(np.sin((i - 25) / 20.0 * np.pi) * 8)
        # Ripple circle
        draw = ImageDraw.Draw(frame)
        r = min(40, (i - 25) * 3)
        draw.ellipse((hx - r, hy - r, hx + r, hy + r), outline=(225, 29, 72, 220), width=4)

    frame.paste(hand_resized, (hx - int(hand_w * 0.18), hy + tap), hand_resized)
    frame.convert("RGB").save(os.path.join(frames_temp, f"frame_{frame_idx:04d}.jpg"), quality=95)
    frame_idx += 1

# Cena 3: Checkout Modal com Sinal 50% & PIX (8.0s a 12.0s) = 100 frames
s3_frames = 100
for i in range(s3_frames):
    frame = shot3.copy()
    prog = min(1.0, i / 18.0)
    t = 1 - (1 - prog) ** 2
    hx = int((W + 60) + ((W * 0.50) - (W + 60)) * t)
    hy = int((H + 60) + ((H * 0.72) - (H + 60)) * t)

    tap = 0
    if 22 <= i <= 40:
        tap = int(np.sin((i - 22) / 18.0 * np.pi) * 7)
        draw = ImageDraw.Draw(frame)
        r = min(35, (i - 22) * 3)
        draw.ellipse((hx - r, hy - r, hx + r, hy + r), outline=(16, 185, 129, 230), width=4)

    frame.paste(hand_resized, (hx - int(hand_w * 0.20), hy + tap), hand_resized)
    frame.convert("RGB").save(os.path.join(frames_temp, f"frame_{frame_idx:04d}.jpg"), quality=95)
    frame_idx += 1

# Cena 4: Tela de Conversa e Pedido WhatsApp (12.0s a 16.0s) = 100 frames
s4_frames = 100
for i in range(s4_frames):
    zoom = 1.0 + (i / float(s4_frames)) * 0.05
    zw, zh = int(W * zoom), int(H * zoom)
    im_zoomed = shot4.resize((zw, zh), Image.Resampling.BILINEAR)
    x = (zw - W) // 2
    y = (zh - H) // 2
    frame = im_zoomed.crop((x, y, x + W, y + H)).copy()
    frame.convert("RGB").save(os.path.join(frames_temp, f"frame_{frame_idx:04d}.jpg"), quality=95)
    frame_idx += 1

# Cena 5: Outro 3D Comercial com Smartphone (16.0s a 20.0s) = 100 frames
while frame_idx < total_frames:
    i = frame_idx - 400
    zoom = 1.06 - (i / 100.0) * 0.06
    zw, zh = int(W * max(1.0, zoom)), int(H * max(1.0, zoom))
    im_zoomed = shot5.resize((zw, zh), Image.Resampling.BILINEAR)
    x = (zw - W) // 2
    y = (zh - H) // 2
    frame = im_zoomed.crop((x, y, x + W, y + H)).copy()
    frame.convert("RGB").save(os.path.join(frames_temp, f"frame_{frame_idx:04d}.jpg"), quality=95)
    frame_idx += 1

print(f"✨ Todos os {frame_idx} frames gerados! Sintetizando áudio masterizado...")

# 1. Gerar voz via PowerShell SAPI
tts_script = os.path.join(base_dir, "_gen_voice.ps1")
voice_wav = os.path.join(base_dir, "voice_festejando.wav")

ps_code = f'''
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile("{voice_wav}")
$synth.Speak("Procurando o bolo perfeito ou aquela mini festa inesquecivel? Conheça a Festejando na Mesa! Bolos decorados artesanais, bolinho de festa por apenas cem reais, docinhos gourmet e kits pegue e monte completos! Escolha seus sabores favoritos, reserve sua data com apenas cinquenta por cento de sinal e receba direto no WhatsApp! Festejando na Mesa: doces momentos, lembranças que ficam!")
$synth.Dispose()
'''

with open(tts_script, "w", encoding="utf-8") as f:
    f.write(ps_code)

subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", tts_script], capture_output=True)
if os.path.exists(tts_script):
    os.remove(tts_script)

# Trilha sonora de fundo
bg_music = r"c:\Users\luciano\.gemini\antigravity\scratch\catalogo-video-engine-template\engine-video\assets\audio_promo.m4a"
mixed_audio = os.path.join(base_dir, "final_master_audio.wav")

if os.path.exists(voice_wav) and os.path.exists(bg_music):
    print("🎶 Mixando voz de estúdio com trilha sonora de fundo...")
    cmd_audio = [
        ffmpeg_bin,
        "-i", voice_wav,
        "-i", bg_music,
        "-filter_complex", "[0:a]volume=1.3[v];[1:a]volume=0.25[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[out]",
        "-map", "[out]",
        "-t", "20.0",
        mixed_audio,
        "-y"
    ]
    subprocess.run(cmd_audio, capture_output=True)
elif os.path.exists(bg_music):
    mixed_audio = bg_music
elif os.path.exists(voice_wav):
    mixed_audio = voice_wav

print("🎥 Codificando vídeo oficial H.264 em alta performance com FFmpeg...")

cmd_video = [
    ffmpeg_bin,
    "-framerate", str(fps),
    "-i", os.path.join(frames_temp, "frame_%04d.jpg"),
    "-i", mixed_audio,
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "20",
    "-preset", "medium",
    "-profile:v", "high",
    "-level", "3.1",
    "-g", "50",
    "-c:a", "aac",
    "-b:a", "192k",
    "-ar", "44100",
    "-channel_layout", "stereo",
    "-brand", "mp42",
    "-movflags", "+faststart",
    "-t", "20.0",
    out_public_mp4,
    "-y"
]

res = subprocess.run(cmd_video, capture_output=True, text=True)

if res.returncode == 0 and os.path.exists(out_public_mp4):
    shutil.copyfile(out_public_mp4, out_desktop_mp4)
    size_mb = os.path.getsize(out_public_mp4) / (1024 * 1024)
    print(f"🎉 SUCESSO! Vídeo gerado em: {out_public_mp4} ({size_mb:.2f} MB)")
    print(f"🖥️ Salvo também na Área de Trabalho: {out_desktop_mp4}")
    shutil.rmtree(frames_temp, ignore_errors=True)
    if os.path.exists(voice_wav):
        os.remove(voice_wav)
    if os.path.exists(mixed_audio) and mixed_audio.endswith(".wav"):
        os.remove(mixed_audio)
else:
    print("❌ Falha na codificação do vídeo:", res.stderr)
