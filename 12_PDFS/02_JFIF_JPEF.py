from pathlib import Path
from PIL import Image, ImageOps

src = Path(r"C:\Users\User\Desktop\GenAI Prep\Images\03_RAG_Implementations")          # folder with your .jfif files
out = Path(r"C:\Users\User\Desktop\GenAI Prep\Images\03_RAG_Implementations\Insta") 

out.mkdir(parents=True, exist_ok=True)

TARGET = (1080, 1350)   # 4:5 portrait
MODE = "crop"           # "crop" = fill and trim edges, "pad" = keep full image with borders
PAD_COLOR = (255, 255, 255)  # white borders; use (0, 0, 0) for black

for f in src.glob("*"):
    if f.suffix.lower() not in {".jfif", ".jpg", ".jpeg", ".png"}:
        continue

    img = Image.open(f)
    img = ImageOps.exif_transpose(img).convert("RGB")  # fixes rotated phone photos

    if MODE == "crop":
        # Scales to fill 1080x1350, then center-crops the excess
        result = ImageOps.fit(img, TARGET, Image.LANCZOS, centering=(0.5, 0.5))
    else:
        # Scales to fit inside 1080x1350, then adds borders
        result = ImageOps.pad(img, TARGET, Image.LANCZOS, color=PAD_COLOR, centering=(0.5, 0.5))

    result.save(out / f"{f.stem}.jpg", "JPEG", quality=95)
    print("Saved:", f.name)