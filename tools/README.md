# Herramientas de contenido (Ibiza Party Flights)

- `assets/photos/`: fotos de Unsplash con licencia libre (Rodrigo Kugnharski, David Švihovec, Rawness Grow, Ferran Feixas, Annegret Kammer). `piscina.jpg` ya tiene el logo de Ushuaïa tapado con una pelota de playa y un delfín hinchable: no uses ninguna versión sin tapar.
- Carruseles 1080×1350: `carousel_slides_example.js` define las diapositivas (cover/card/cta); `carousel_render.js` las renderiza con Playwright (Chromium en /opt/pw-browsers/chromium, fuente Poppins) a `out/*.jpg`. Copia las fotos al directorio de trabajo antes de renderizar.
- Reels 1080×1920: `reel_frames.js` genera escenas PNG; luego ffmpeg: zoompan suave por escena (~2,8 s) + xfade slideleft 0,35 s + pista de audio. Sin música comercial dentro del archivo.
- Estilo: azul noche #0E1726, naranja #E8582A / #FF8A5C, Poppins 700, logo = círculo oscuro con sol naranja.
- Medios publicados en la rama `media`, carpeta por semana `AAAA-wNN/`. URL pública: https://raw.githubusercontent.com/ibizapartyflights/social/media/<carpeta>/<archivo>
- Música de reels: `python3 tools/beat.py musica.wav <segundos> 124 <semilla>` genera una base house original sin derechos (cambia la semilla cada semana). Mézclala en el vídeo con `-c:a aac -b:a 192k`.
- Vídeo: NUNCA zoompan/Ken Burns (vibra y pierde nitidez). Escenas fijas 1080×1920 (lanczos) + xfade, libx264 -crf 16 -preset slow -tune stillimage. Sin logo/nombre arriba a la izquierda en los reels (TikTok lo tapa); la marca va en la pantalla final.
