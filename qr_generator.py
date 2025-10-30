import qrcode
from PIL import Image, ImageDraw, ImageFont

# Step 1: Input URL
url = input("Enter a URL to convert into QR Code: ")

# Step 2: Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)
img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# Step 3: Texts
text_eng = "Scan me to get Kalash Collection Information"
# text_marathi = "स्कॅन करून कलश संग्रहाची माहिती मिळवा"

# # Step 4: Load fonts
# try:
#     font_eng = ImageFont.truetype("arial.ttf", 26)
#     font_marathi = ImageFont.truetype("C:/Windows/Fonts/Nirmala.ttf", 28)
# except IOError:
#     print("⚠️ Could not load custom fonts — Marathi text may appear as boxes.")
#     font_eng = ImageFont.load_default()
#     font_marathi = ImageFont.load_default()

# Step 5: Measure both text widths
draw_tmp = ImageDraw.Draw(img_qr)
eng_bbox = draw_tmp.textbbox((0, 0), text_eng, font=font_eng)
mar_bbox = draw_tmp.textbbox((0, 0), text_marathi, font=font_marathi)

text_width = max(eng_bbox[2] - eng_bbox[0], mar_bbox[2] - mar_bbox[0])
text_height = (eng_bbox[3] - eng_bbox[1]) + (mar_bbox[3] - mar_bbox[1]) + 40

# Step 6: Adjust overall image width if text is wider than QR
qr_width, qr_height = img_qr.size
final_width = max(qr_width, text_width + 40)  # add side padding
final_height = qr_height + text_height + 20

# Step 7: Create new white image and center QR
img_with_text = Image.new("RGB", (final_width, final_height), "white")
x_offset = (final_width - qr_width) // 2
img_with_text.paste(img_qr, (x_offset, 0))

draw = ImageDraw.Draw(img_with_text)

# Step 8: Helper to center text
def center_text(draw, text, y, font, color="black"):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (final_width - text_width) / 2
    draw.text((x, y), text, fill=color, font=font)

# Step 9: Draw texts centered below QR
y_start = qr_height + 10
center_text(draw, text_eng, y_start, font_eng, "black")
center_text(draw, text_marathi, y_start + (eng_bbox[3] - eng_bbox[1]) + 15, font_marathi, "#1E3A8A")

# Step 10: Save final
img_with_text.save("qr_code_with_text.png")
print("✅ QR code with Marathi text properly centered and fitted saved as 'qr_code_with_text.png'")
