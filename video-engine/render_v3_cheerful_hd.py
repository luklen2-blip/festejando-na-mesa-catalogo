#!/usr/bin/env python3
"""
Motor de Vídeo Promocional HD v3.0 - Festejando na Mesa
- Voz Neural Humana Expressiva e Alegre (pt-BR-FranciscaNeural via Edge-TTS)
- 1 Única Voz de Estúdio (Zero conflito de áudio)
- Fotos Gigantes dos 10 Panfletos com Preços Grandes e Legíveis
- Trilha Sonora Instrumental Festiva Sintetizada Suave
- Sincronização Absoluta Segundo a Segundo
"""

import os
import shutil
import subprocess
import wave
import math
import asyncio
import numpy as np
from PIL import Image, ImageDraw
import edge_tts

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

SCENES_CONFIG = [
    {
        "id": 1,
        "name": "Combos Mini Festa",
        "text": "Procurando a festa perfeita sem gastar muito? Na Festejando na Mesa você encontra a Promoção Mini Festa Completa com bolo, painel e docinhos por apenas cento e cinquenta reais, ou duzentos e vinte na opção completa!",
        "html": "scene1_combos_large.html"
    },
    {
        "id": 2,
        "name": "Bolinho de Festa R$ 100",
        "text": "E olha esse sucesso: o nosso Bolinho de Festa super fofinho com duas camadas generosas de recheio, servindo trinta fatias por apenas cem reais! Paçoca, brigadeiro ou beijinho!",
        "html": "scene2_bolinho_large.html"
    },
    {
        "id": 3,
        "name": "Bolos Decorados Doce Lembrança",
        "text": "Bolos decorados sob medida de vinte a cinquenta fatias, com massas artesanais, sete opções de recheios e o topo de bolo simples já incluso de presente pra você!",
        "html": "scene3_bolos_decorados_large.html"
    },
    {
        "id": 4,
        "name": "Docinhos & Mini Trufas",
        "text": "Centos de docinhos tradicionais por cento e dez reais, docinhos gourmet com Ninho e Nutella por cento e sessenta e cinco, pirulitos e mini trufas deliciosas!",
        "html": "scene4_doces_trufas_large.html"
    },
    {
        "id": 5,
        "name": "Kits Temáticos Pegue e Monte",
        "text": "Para a decoração, temos cenários temáticos incríveis: Princesas, Sonic, Mulher Maravilha e Borboleta Azul, no pegue e monte a partir de oitenta reais ou com montagem completa!",
        "html": "scene5_kits_temas_large.html"
    },
    {
        "id": 6,
        "name": "Reserva com 50% de Sinal PIX",
        "text": "Monte sua festa no catálogo e reserve sua data com apenas cinquenta por cento de sinal no PIX! O restante você paga na retirada em Senador Vasconcelos!",
        "html": "scene6_carrinho_sinal_large.html"
    },
    {
        "id": 7,
        "name": "Catálogo na Bio & WhatsApp",
        "text": "Monte seu pedido agora mesmo no nosso Catálogo Digital no link da bio ou peça pelo nosso WhatsApp! Festejando na Mesa: doces momentos, lembranças que ficam!",
        "html": "scene7_whatsapp_outro_large.html"
    }
]

# 1. Gerar as 7 locuções neurais com FranciscaNeural
async def generate_all_voices():
    print("🎙️ 1. Gerando locução alegre e expressiva com voz humana neural (pt-BR-FranciscaNeural)...")
    for s in SCENES_CONFIG:
        mp3_out = os.path.join(base_dir, f"francisca_scene_{s['id']}.mp3")
        wav_out = os.path.join(base_dir, f"francisca_scene_{s['id']}.wav")
        communicate = edge_tts.Communicate(s['text'], "pt-BR-FranciscaNeural", rate="+6%", pitch="+2Hz")
        await communicate.save(mp3_out)
        
        # Converter para wav estéreo 44100Hz
        cmd = [ffmpeg_bin, "-i", mp3_out, "-ar", "44100", "-ac", "1", wav_out, "-y"]
        subprocess.run(cmd, capture_output=True)
        if os.path.exists(mp3_out):
            os.remove(mp3_out)

asyncio.run(generate_all_voices())

# Medir durações
scene_durations = []
for s in SCENES_CONFIG:
    wav_path = os.path.join(base_dir, f"francisca_scene_{s['id']}.wav")
    with wave.open(wav_path, 'rb') as w:
        dur = w.getnframes() / float(w.getframerate())
        adj = round(dur + 0.35, 2)
        scene_durations.append(adj)
        print(f"   • Cena {s['id']} ({s['name']}): {dur:.2f}s fala -> {adj:.2f}s vídeo")

total_video_duration = sum(scene_durations)
print(f"⏱️ Duração total da narrativa sincronizada: {total_video_duration:.2f} segundos")

# 2. Gerar Trilha Sonora Instrumental Suave e Festiva (Zero Vocais)
print("🎵 2. Sintetizando trilha sonora instrumental (piano e sinos festivos)...")
sample_rate = 44100
total_samples = int(sample_rate * total_video_duration)
music_samples = np.zeros(total_samples, dtype=np.float32)

chord_progression = [
    [261.63, 329.63, 392.00, 523.25], # C
    [196.00, 246.94, 293.66, 392.00], # G
    [220.00, 261.63, 329.63, 440.00], # Am
    [174.61, 220.00, 261.63, 349.23], # F
]

chord_duration = 2.0
num_chords = int(math.ceil(total_video_duration / chord_duration))

for c_idx in range(num_chords):
    chord_notes = chord_progression[c_idx % len(chord_progression)]
    c_start = int(c_idx * chord_duration * sample_rate)
    c_end = min(total_samples, int((c_idx + 1) * chord_duration * sample_rate))
    n_samples = c_end - c_start
    if n_samples <= 0:
        continue
    
    t = np.linspace(0, n_samples / sample_rate, n_samples, endpoint=False)
    chord_signal = np.zeros(n_samples, dtype=np.float32)
    for note_i, freq in enumerate(chord_notes):
        envelope = np.exp(-1.8 * (t % 0.5))
        note_sound = np.sin(2 * np.pi * freq * t) * 0.15 + np.sin(4 * np.pi * freq * t) * 0.05
        chord_signal += note_sound * envelope

    bell_freq = chord_notes[-1] * 2.0
    bell_env = np.exp(-3.5 * t)
    chord_signal += np.sin(2 * np.pi * bell_freq * t) * 0.10 * bell_env

    music_samples[c_start:c_end] += chord_signal

fade_len = int(sample_rate * 1.0)
music_samples[:fade_len] *= np.linspace(0, 1, fade_len)
music_samples[-fade_len:] *= np.linspace(1, 0, fade_len)

bg_music_wav = os.path.join(base_dir, "instrumental_bg.wav")
music_int16 = np.int16(np.clip(music_samples * 0.20, -1.0, 1.0) * 32767)

with wave.open(bg_music_wav, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    wf.writeframes(music_int16.tobytes())

# Concatenar as falas
print("🔗 3. Concatenando narração e mixando com a trilha...")
concat_list = os.path.join(base_dir, "francisca_concat.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for s in SCENES_CONFIG:
        f.write(f"file 'francisca_scene_{s['id']}.wav'\n")

full_voice_wav = os.path.join(base_dir, "francisca_full_voice.wav")
subprocess.run([ffmpeg_bin, "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", full_voice_wav, "-y"], capture_output=True)

# Mixar voz e trilha
final_master_audio = os.path.join(base_dir, "final_master_audio_v3.wav")
cmd_mix = [
    ffmpeg_bin,
    "-i", full_voice_wav,
    "-i", bg_music_wav,
    "-filter_complex", "[0:a]volume=1.35[v];[1:a]volume=0.22[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[out]",
    "-map", "[out]",
    "-t", str(total_video_duration),
    final_master_audio,
    "-y"
]
subprocess.run(cmd_mix, capture_output=True)

# 4. Capturar as 7 cenas com fotos e preços grandes via Edge headless
print("📸 4. Capturando imagens das 7 cenas do catálogo com o Microsoft Edge...")
for s in SCENES_CONFIG:
    html_url = f"file:///{os.path.join(base_dir, s['html']).replace('\\', '/')}"
    out_png = os.path.join(base_dir, f"shot_large_{s['id']}.png")
    cmd_edge = [
        edge_bin,
        "--headless",
        f"--screenshot={out_png}",
        "--window-size=480,854",
        html_url
    ]
    subprocess.run(cmd_edge, capture_output=True)
    if os.path.exists(out_png):
        print(f"   ✓ Cena {s['id']} capturada com sucesso ({os.path.getsize(out_png)} bytes)")

# 5. Renderização dos frames com dinamismo e zoom nos preços
print("🎬 5. Animando quadros com foco nos preços e imagens dos produtos...")
W, H = 480, 854
fps = 25
hand = Image.open(hand_path).convert("RGBA")
hand_w = int(W * 0.58)
hand_h = int(hand.height * (hand_w / hand.width))
hand_resized = hand.resize((hand_w, hand_h), Image.Resampling.LANCZOS)

frames_dir = os.path.join(base_dir, "v3_frames")
if os.path.exists(frames_dir):
    shutil.rmtree(frames_dir)
os.makedirs(frames_dir, exist_ok=True)

frame_idx = 0

for s_idx, s in enumerate(SCENES_CONFIG):
    dur = scene_durations[s_idx]
    num_frames = int(dur * fps)
    shot_img = Image.open(os.path.join(base_dir, f"shot_large_{s['id']}.png")).convert("RGBA")
    shot_img = shot_img.resize((W, H), Image.Resampling.LANCZOS)

    print(f"   • Renderizando Cena {s['id']} ({s['name']}): {num_frames} quadros...")

    for f in range(num_frames):
        frame = shot_img.copy()

        # Efeito de aproximação suave e dinâmico na imagem e no preço
        zoom = 1.0 + (f / float(num_frames)) * 0.05
        zw, zh = int(W * zoom), int(H * zoom)
        im_zoomed = shot_img.resize((zw, zh), Image.Resampling.BILINEAR)
        x = (zw - W) // 2
        y = (zh - H) // 2
        frame = im_zoomed.crop((x, y, x + W, y + H)).copy()

        # Na cena 6 (Checkout), animar o toque da mão real no botão de PIX
        if s['id'] == 6:
            prog = min(1.0, f / 22.0)
            t_ease = 1 - (1 - prog) ** 2
            hx = int((W + 60) + ((W * 0.48) - (W + 60)) * t_ease)
            hy = int((H + 60) + ((H * 0.48) - (H + 60)) * t_ease)

            tap = 0
            if 25 <= f <= 50:
                tap = int(np.sin((f - 25) / 25.0 * np.pi) * 8)
                draw = ImageDraw.Draw(frame)
                r = min(45, (f - 25) * 3)
                draw.ellipse((hx - r, hy - r, hx + r, hy + r), outline=(16, 185, 129, 230), width=4)

            frame.paste(hand_resized, (hx - int(hand_w * 0.18), hy + tap), hand_resized)

        frame.convert("RGB").save(os.path.join(frames_dir, f"frame_{frame_idx:04d}.jpg"), quality=95)
        frame_idx += 1

print(f"✨ Total de {frame_idx} quadros renderizados!")

# 6. Compilação FFmpeg de Alta Performance
print("🎞️ 6. Compilando vídeo oficial H.264 CRF 20 com áudio masterizado...")
cmd_compile = [
    ffmpeg_bin,
    "-framerate", str(fps),
    "-i", os.path.join(frames_dir, "frame_%04d.jpg"),
    "-i", final_master_audio,
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
    print(f"🎉 SUCESSO TOTAL! Vídeo promocional v3.0 gerado:")
    print(f"   • Catálogo Web: {out_public_mp4} ({size_mb:.2f} MB)")
    print(f"   • Área de Trabalho: {out_desktop_mp4} ({size_mb:.2f} MB)")
    
    # Limpeza
    shutil.rmtree(frames_dir, ignore_errors=True)
    for s in SCENES_CONFIG:
        w_tmp = os.path.join(base_dir, f"francisca_scene_{s['id']}.wav")
        if os.path.exists(w_tmp):
            os.remove(w_tmp)
    for tmp_f in [bg_music_wav, concat_list, full_voice_wav, final_master_audio]:
        if os.path.exists(tmp_f):
            os.remove(tmp_f)
else:
    print("❌ Erro FFmpeg:", res.stderr)
