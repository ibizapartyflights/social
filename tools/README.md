# Herramientas de contenido (Ibiza Party Flights)

- `assets/photos/`: fotos de Unsplash con licencia libre (Rodrigo Kugnharski, David Švihovec, Rawness Grow, Ferran Feixas, Annegret Kammer). `piscina.jpg` ya tiene el logo de Ushuaïa tapado con una pelota de playa y un delfín hinchable: no uses ninguna versión sin tapar.
- Carruseles 1080×1350: `carousel_slides_example.js` define las diapositivas (cover/card/cta); `carousel_render.js` las renderiza con Playwright (Chromium en /opt/pw-browsers/chromium, fuente Poppins) a `out/*.jpg`. Copia las fotos al directorio de trabajo antes de renderizar.
- Reels 1080×1920: `reel_scenes.js spec.json outdir` (escenas foto / personajes de bloques isométricos propios / pantalla final de marca, sin logo arriba a la izquierda) + ffmpeg con escenas fijas y xfade. `reel_frames.js` es antiguo (lleva marca arriba y zoompan): no usar.
- Estilo: azul noche #0E1726, naranja #E8582A / #FF8A5C, Poppins 700, logo = círculo oscuro con sol naranja.
- Medios publicados en la rama `media`, carpeta por semana `AAAA-wNN/`. URL pública: https://raw.githubusercontent.com/ibizapartyflights/social/media/<carpeta>/<archivo>
- Música de reels: `python3 tools/beat.py musica.wav <segundos> 124 <semilla>` genera una base house original sin derechos (cambia la semilla cada semana). Mézclala en el vídeo con `-c:a aac -b:a 192k`.
- Vídeo: NUNCA zoompan/Ken Burns (vibra y pierde nitidez). Escenas fijas 1080×1920 (lanczos) + xfade, libx264 -crf 16 -preset slow -tune stillimage. Sin logo/nombre arriba a la izquierda en los reels (TikTok lo tapa); la marca va en la pantalla final.

## Identidad de marca (aprobada por Rubén el 23/10/2026)
Identidad flexible, no un logo fijo. Ver assets/brand/sistema_marca.png y tools/brand_tiles.js (funciones badge, waves, stack, vert).
- Logo: sello circular "IBIZA PARTY FLIGHTS • YOUR IBIZA DEAL HUNTERS" alrededor de un sol naranja con franjas (assets/brand/perfil_sello_oscuro.png / _claro.png).
- Tipografía: Poppins 700, MAYÚSCULAS, apilada y cortando palabras con guiones (IBI-ZA / PAR-TY, DEAL HUN-TERS, IBIZA SOR-TED), interlineado .86, tracking -0.04em. Texto pequeño en vertical como acompañamiento.
- Patrón: olas gruesas repetidas (mar de Ibiza).
- Paleta: azul noche #0E1726, naranja #E8582A, arena #F4E3C8, azul neón #4FE3FF (acento rosa #FF3D8B solo puntual).
- Uso en vídeos: gancho del primer segundo y pantalla final con estas piezas (bloques de color plano, tipografía apilada, sello). Varía combinaciones; que cada post sea distinto pero reconocible. Nada de avión dibujado.
