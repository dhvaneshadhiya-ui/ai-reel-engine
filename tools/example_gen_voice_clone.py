#!/usr/bin/env python3
import shutil
from pathlib import Path
from gradio_client import Client, handle_file
ROOT = Path(__file__).resolve().parent.parent
REF = str(ROOT / "_private/voice/voice-ref.wav")
OUT = ROOT / "public/assets/kleo/vo.wav"
TEXT = ("A senior engineer in London just traded his thirty-third floor apartment "
        "for his childhood bedroom. Ninety days later, he was making sixty-two "
        "thousand dollars a month. His name is Cameron Trew, and the product is "
        "Kleo, an AI tool that writes LinkedIn posts. The first version was a "
        "free extension with sixty thousand users, until LinkedIn hit it with a "
        "cease and desist. So he rebuilt the entire thing from scratch, in four "
        "weeks, with Claude Code. Beta pricing was fifty-nine dollars a month. "
        "Five hundred spots. Sold out in four days. Now, here's the part everyone "
        "gets wrong. He wasn't solo. Three co-founders brought half a million "
        "LinkedIn followers. That was the distribution. But every single line of "
        "the product? One engineer. Everyone's going to credit the AI tools. And "
        "sure, they helped. But this man moved back in with his parents to afford "
        "a bet on himself. The tools got cheap. The nerve never did. Would you "
        "move back home to bet on yourself?")
c = Client("vibingvoice/vibe-voice-custom-voices")
res = c.predict(text=TEXT, speaker1_audio_path=handle_file(REF),
                speaker2_audio_path=None, speaker3_audio_path=None, speaker4_audio_path=None,
                seed=42, diffusion_steps=24, cfg_scale=1.3, use_sampling=False,
                temperature=0.95, top_p=0.95, max_words_per_chunk=250,
                api_name="/generate_speech_gradio")
src = res if isinstance(res, str) else (res[0] if isinstance(res, (list, tuple)) else res.get("value"))
shutil.copy(src, OUT); print("saved", OUT)
