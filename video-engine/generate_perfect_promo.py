#!/usr/bin/env python3
"""
Motor de Renderização do Vídeo Promocional Oficial - Festejando na Mesa
- 1 Única Voz de Estúdio Clara e Sincronizada (sem vozes sobrepostas)
- Todas as 10 Imagens Reais dos Produtos dos Panfletos
- Trilha Sonora Instrumental Sintetizada Suave e Festiva (Zero Vocais)
- Animação da Mão Humana Real e Efeitos de Toque
- Sincronização Segundo a Segundo entre Áudio e Imagem
"""

import os
import shutil
import subprocess
import wave
import math
import struct
import numpy as np
from PIL import Image, ImageDraw

base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(base_dir)
assets_dir = os.path.join(project_dir, "public", "assets")
hand_path = os.path.join(base_dir, "perfect_real_hand.png")
ffmpeg_bin = r"C:\Users\luciano\.gemini\antigravity\brain\60c9c2db-d485-4829-b419-4d3a923940e0\scratch\node_modules\ffmpeg-static\ffmpeg.exe"
edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

desktop = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")
if not os.path.exists(desktop):
    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")

out_public_mp4 = os.path.join(assets_dir, "video_promo.mp4")
out_desktop_mp4 = os.path.join(desktop, "VIDEO_PROMO_FESTEJANDO_NA_MESA.mp4")

# 1. Definir Cenas e Roteiro Sincronizado
# Cada cena possui texto exato e tempo delimitado
SCENES = [
    {
        "id": 1,
        "name": "Combos Mini Festa",
        "audio_text": "Procurando a festa perfeita? Na Festejando na Mesa você encontra combos completos de mini festa com bolo, doces e painel a partir de quarenta reais!",
        "html_file": "scene1_combos.html"
    },
    {
        "id": 2,
        "name": "Bolos Decorados & Bolinho R$ 100",
        "audio_text": "Bolos decorados artesanais sob medida com topo simples incluso, e o famoso bolinho de festa de trinta fatias por apenas cem reais!",
        "html_file": "scene2_bolos.html"
    },
    {
        "id": 3,
        "name": "Docinhos Gourmet & Mini Trufas",
        "audio_text": "Deliciosos centos de docinhos tradicionais e gourmet, pirulitos de chocolate e mini trufas recheadas que derretem na boca!",
        "html_file": "scene3_docinhos.html"
    },
    {
        "id": 4,
        "name": "Kits Pegue e Monte",
        "audio_text": "Cenários temáticos apaixonantes: Princesas, Sonic, Mulher Maravilha e Borboleta Azul, pegue e monte ou montagem completa!",
        "html_file": "scene4_temas.html"
    },
    {
        "id": 5,
        "name": "Interação & Sinal 50% PIX",
        "audio_text": "Você escolhe os produtos no catálogo e garante sua data com cinquenta por cento de sinal no PIX e o restante na retirada!",
        "html_file": "scene5_checkout.html"
    },
    {
        "id": 6,
        "name": "WhatsApp Oficial & Fechamento",
        "audio_text": "Tudo rápido e direto no WhatsApp! Festejando na Mesa: doces momentos, lembranças que ficam!",
        "html_file": "scene6_whatsapp.html"
    }
]

print("🎙️ 1. Gerando narração única e exclusiva para cada cena...")

ps_script_lines = [
    'Add-Type -AssemblyName System.Speech',
    '$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer',
    '$synth.Rate = 0'
]

for s in SCENES:
    wav_path = os.path.join(base_dir, f"audio_scene_{s['id']}.wav").replace('\\', '/')
    ps_script_lines.append(f'$synth.SetOutputToWaveFile("{wav_path}")')
    ps_script_lines.append(f'$synth.Speak("{s["audio_text"]}")')

ps_script_lines.append('$synth.Dispose()')

ps_file = os.path.join(base_dir, "_tts_gen.ps1")
with open(ps_file, "w", encoding="utf-8-sig") as f:
    f.write("\n".join(ps_script_lines))

subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], capture_output=True)
if os.path.exists(ps_file):
    os.remove(ps_file)

# Medir durações dos áudios
scene_durations = []
for s in SCENES:
    wav_path = os.path.join(base_dir, f"audio_scene_{s['id']}.wav")
    if os.path.exists(wav_path):
        with wave.open(wav_path, 'rb') as w:
            dur = w.getnframes() / float(w.getframerate())
            # Adicionar 0.4s de margem de respiro para transição suave
            adjusted_dur = round(dur + 0.4, 2)
            scene_durations.append(adjusted_dur)
            print(f"   • Cena {s['id']} ({s['name']}): {dur:.2f}s áudio -> {adjusted_dur:.2f}s vídeo")
    else:
        scene_durations.append(4.5)

total_video_duration = sum(scene_durations)
print(f"⏱️ Duração total sincronizada: {total_video_duration:.2f} segundos")

# 2. Criar Trilha Sonora Instrumental Festiva e Suave (Zero Vozes)
print("🎵 2. Sintetizando trilha sonora instrumental pura (harmonia acústica e sinos festivos)...")

sample_rate = 44100
total_samples = int(sample_rate * total_video_duration)
music_samples = np.zeros(total_samples, dtype=np.float32)

# Progressão de acordes: Dó Maior (C), Sol Maior (G), Lá Menor (Am), Fá Maior (F)
chord_progression = [
    [261.63, 329.63, 392.00, 523.25], # C
    [196.00, 246.94, 293.66, 392.00], # G
    [220.00, 261.63, 329.63, 440.00], # Am
    [174.61, 220.00, 261.63, 349.23], # F
]

chord_duration = 2.0 # segundos por acorde
num_chords = int(math.ceil(total_video_duration / chord_duration))

for c_idx in range(num_chords):
    chord_notes = chord_progression[c_idx % len(chord_progression)]
    c_start = int(c_idx * chord_duration * sample_rate)
    c_end = min(total_samples, int((c_idx + 1) * chord_duration * sample_rate))
    n_samples = c_end - c_start
    if n_samples <= 0:
        continue
    
    t = np.linspace(0, n_samples / sample_rate, n_samples, endpoint=False)
    
    # Arpejo suave estilo caixinha de música / piano acústico
    chord_signal = np.zeros(n_samples, dtype=np.float32)
    for note_i, freq in enumerate(chord_notes):
        envelope = np.exp(-1.8 * (t % 0.5)) # Decaimento suave
        note_sound = np.sin(2 * np.pi * freq * t) * 0.15 + np.sin(4 * np.pi * freq * t) * 0.05
        chord_signal += note_sound * envelope

    # Sinos de celebração suaves a cada compasso
    bell_freq = chord_notes[-1] * 2.0
    bell_env = np.exp(-3.5 * t)
    chord_signal += np.sin(2 * np.pi * bell_freq * t) * 0.12 * bell_env

    music_samples[c_start:c_end] += chord_signal

# Fade in e Fade out na música
fade_len = int(sample_rate * 1.0)
fade_in = np.linspace(0, 1, fade_len)
fade_out = np.linspace(1, 0, fade_len)
music_samples[:fade_len] *= fade_in
music_samples[-fade_len:] *= fade_out

# Salvar música instrumental de fundo
bg_music_wav = os.path.join(base_dir, "pure_instrumental_bg.wav")
music_int16 = np.int16(np.clip(music_samples * 0.22, -1.0, 1.0) * 32767)

with wave.open(bg_music_wav, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    wf.writeframes(music_int16.tobytes())

# 3. Concatenar as falas em sequência perfeita
print("🔗 3. Concatenando narração e mixando com a trilha instrumental...")
concat_voice_list = os.path.join(base_dir, "voice_concat.txt")
with open(concat_voice_list, "w", encoding="utf-8") as f:
    for s in SCENES:
        w_name = f"audio_scene_{s['id']}.wav"
        f.write(f"file '{w_name}'\n")

full_voice_wav = os.path.join(base_dir, "full_voice_only.wav")
cmd_concat = [
    ffmpeg_bin,
    "-f", "concat",
    "-safe", "0",
    "-i", concat_voice_list,
    "-c", "copy",
    full_voice_wav,
    "-y"
]
subprocess.run(cmd_concat, capture_output=True)

# Mixar a voz única com a trilha instrumental suave
final_audio_master = os.path.join(base_dir, "master_audio_perfect.wav")
cmd_mix = [
    ffmpeg_bin,
    "-i", full_voice_wav,
    "-i", bg_music_wav,
    "-filter_complex", "[0:a]volume=1.4[v];[1:a]volume=0.25[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[out]",
    "-map", "[out]",
    "-t", str(total_video_duration),
    final_audio_master,
    "-y"
]
subprocess.run(cmd_mix, capture_output=True)

# 4. Capturar as 6 Cenas em Alta Resolução 480x854 com o Microsoft Edge Headless
print("📸 4. Capturando imagens das 6 cenas do catálogo com o Microsoft Edge...")
for s in SCENES:
    html_path = f"file:///{os.path.join(base_dir, s['html_file']).replace('\\', '/')}"
    out_png = os.path.join(base_dir, f"shot_{s['id']}.png")
    cmd_edge = [
        edge_bin,
        "--headless",
        f"--screenshot={out_png}",
        "--window-size=480,854",
        html_path
    ]
    subprocess.run(cmd_edge, capture_output=True)
    if os.path.exists(out_png):
        print(f"   ✓ Capturada Cena {s['id']} ({s['name']}) -> {os.path.getsize(out_png)} bytes")

# 5. Animação e Renderização dos Frames de Vídeo Sincronizados
print("🎬 5. Animando quadros com sincronia perfeita de áudio e imagem...")

W, H = 480, 854
fps = 25
hand = Image.open(hand_path).convert("RGBA")
hand_w = int(W * 0.58)
hand_h = int(hand.height * (hand_w / hand.width))
hand_resized = hand.resize((hand_w, hand_h), Image.Resampling.LANCZOS)

frames_dir = os.path.join(base_dir, "perfect_frames")
if os.path.exists(frames_dir):
    shutil.rmtree(frames_dir)
os.makedirs(frames_dir, exist_ok=True)

frame_idx = 0

for s_idx, s in enumerate(SCENES):
    dur = scene_durations[s_idx]
    num_frames = int(dur * fps)
    shot_img = Image.open(os.path.join(base_dir, f"shot_{s['id']}.png")).convert("RGBA")
    shot_img = shot_img.resize((W, H), Image.Resampling.LANCZOS)

    print(f"   • Renderizando Cena {s['id']} ({s['name']}): {num_frames} quadros...")

    for f in range(num_frames):
        frame = shot_img.copy()

        # Efeitos específicos por cena
        if s['id'] in [1, 2, 3, 4]:
            # Zoom suave sutil para dinamismo comercial
            zoom = 1.0 + (f / float(num_frames)) * 0.04
            zw, zh = int(W * zoom), int(H * zoom)
            im_zoomed = shot_img.resize((zw, zh), Image.Resampling.BILINEAR)
            x = (zw - W) // 2
            y = (zh - H) // 2
            frame = im_zoomed.crop((x, y, x + W, y + H)).copy()

        elif s['id'] == 5:
            # Cena 5: Animação da Mão Real tocando no item e selecionando
            prog = min(1.0, f / 22.0)
            t_ease = 1 - (1 - prog) ** 2
            hx = int((W + 60) + ((W * 0.48) - (W + 60)) * t_ease)
            hy = int((H + 60) + ((H * 0.45) - (H + 60)) * t_ease)

            tap = 0
            if 25 <= f <= 50:
                tap = int(np.sin((f - 25) / 25.0 * np.pi) * 8)
                # Onda de toque (ripple)
                draw = ImageDraw.Draw(frame)
                r = min(45, (f - 25) * 3)
                draw.ellipse((hx - r, hy - r, hx + r, hy + r), outline=(225, 29, 72, 220), width=4)

            frame.paste(hand_resized, (hx - int(hand_w * 0.18), hy + tap), hand_resized)

        elif s['id'] == 6:
            # Cena 6: Outro Comercial com aproximação suave
            zoom = 1.05 - (f / float(num_frames)) * 0.05
            zw, zh = int(W * max(1.0, zoom)), int(H * max(1.0, zoom))
            im_zoomed = shot_img.resize((zw, zh), Image.Resampling.BILINEAR)
            x = (zw - W) // 2
            y = (zh - H) // 2
            frame = im_zoomed.crop((x, y, x + W, y + H)).copy()

        frame.convert("RGB").save(os.path.join(frames_dir, f"frame_{frame_idx:04d}.jpg"), quality=95)
        frame_idx += 1

print(f"✨ Total de {frame_idx} quadros gerados com sucesso!")

# 6. Codificação Final com FFmpeg H.264 CRF 20
print("🎞️ 6. Compilando com FFmpeg (H.264 CRF 20, AAC 192k stereo)...")

cmd_compile = [
    ffmpeg_bin,
    "-framerate", str(fps),
    "-i", os.path.join(frames_dir, "frame_%04d.jpg"),
    "-i", final_audio_master,
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
    "-shortest",
    out_public_mp4,
    "-y"
]

res = subprocess.run(cmd_compile, capture_output=True, text=True)

if res.returncode == 0 and os.path.exists(out_public_mp4):
    shutil.copyfile(out_public_mp4, out_desktop_mp4)
    size_mb = os.path.getsize(out_public_mp4) / (1024 * 1024)
    print(f"🎉 SUCESSO ABSOLUTO! Vídeo final gerado:")
    print(f"   • Catálogo Web: {out_public_mp4} ({size_mb:.2f} MB)")
    print(f"   • Área de Trabalho: {out_desktop_mp4} ({size_mb:.2f} MB)")
    
    # Limpeza de arquivos intermediários temporários
    shutil.rmtree(frames_dir, ignore_errors=True)
    for s in SCENES:
        w_tmp = os.path.join(base_dir, f"audio_scene_{s['id']}.wav")
        if os.path.exists(w_tmp):
            os.remove(w_tmp)
    for tmp_f in [bg_music_wav, concat_voice_list, full_voice_wav, final_audio_master]:
        if os.path.exists(tmp_f):
            os.remove(tmp_f)
else:
    print("❌ Erro FFmpeg:", res.stderr)
