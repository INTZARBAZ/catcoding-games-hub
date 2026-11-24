import os
import sys

def build_pdf(output_path):
    # PDF dimensions (US Letter: 612 x 792 points)
    width = 612
    height = 792

    # Streams and objects
    objects = []

    def add_object(content):
        objects.append(content)
        return len(objects)

    # We will assemble object definitions
    # Object 1: Catalog
    # Object 2: Pages
    # Object 3: Page 1
    # Object 4: Font Helvetica
    # Object 5: Font Helvetica-Bold
    # Object 6: Font Helvetica-Oblique
    # Object 7: Content stream
    # Object 8: Link annotation for Live Game
    # Object 9: Link annotation for Store

    stream_lines = []

    # Helper functions for PDF drawing
    def set_fill_color(r, g, b):
        stream_lines.append(f"{r:.3f} {g:.3f} {b:.3f} rg")

    def set_stroke_color(r, g, b):
        stream_lines.append(f"{r:.3f} {g:.3f} {b:.3f} RG")

    def set_line_width(w):
        stream_lines.append(f"{w:.2f} w")

    def draw_rect(x, y, w, h, fill=True, stroke=True):
        op = "b" if (fill and stroke) else ("f" if fill else "s")
        stream_lines.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re {op}")

    def draw_line(x1, y1, x2, y2):
        stream_lines.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def draw_text(font_name, size, x, y, text, r=0.11, g=0.10, b=0.09):
        # Escape special PDF chars
        safe_text = text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        set_fill_color(r, g, b)
        stream_lines.append("BT")
        stream_lines.append(f"/{font_name} {size} Tf")
        stream_lines.append(f"{x:.2f} {y:.2f} Td")
        stream_lines.append(f"({safe_text}) Tj")
        stream_lines.append("ET")

    # 1. Background fill: warm cream (#FAF6F0)
    set_fill_color(0.980, 0.965, 0.941)
    draw_rect(0, 0, width, height, fill=True, stroke=False)

    # 2. Outer decorative border
    set_stroke_color(0.110, 0.098, 0.090)
    set_line_width(2.5)
    draw_rect(24, 24, width - 48, height - 48, fill=False, stroke=True)

    # 3. Header Banner (#1C1917)
    set_fill_color(0.110, 0.098, 0.090)
    draw_rect(30, 680, width - 60, 82, fill=True, stroke=False)

    # Header Accent bar (Orange #EA580C)
    set_fill_color(0.918, 0.345, 0.047)
    draw_rect(30, 674, width - 60, 6, fill=True, stroke=False)

    # Header text
    draw_text("F2", 10, 50, 742, "OFFICIAL ACCESS GUIDE & OWNER MANUAL", 0.918, 0.345, 0.047)
    draw_text("F2", 22, 50, 715, "CatCoding : Interactive Cat Games Hub", 1.0, 1.0, 1.0)
    draw_text("F1", 10.5, 50, 694, "Sensory Enrichment & Interactive Touch Games for Cats", 0.85, 0.85, 0.85)

    # 4. Thank You Hero Card (White card with drop shadow effect)
    # Shadow
    set_fill_color(0.110, 0.098, 0.090)
    draw_rect(54, 538, width - 100, 114, fill=True, stroke=False)
    # White card
    set_fill_color(1.0, 1.0, 1.0)
    set_stroke_color(0.110, 0.098, 0.090)
    set_line_width(2.0)
    draw_rect(50, 542, width - 100, 114, fill=True, stroke=True)

    # Content inside Thank You Card
    draw_text("F2", 17, 72, 626, "Thank You for Your Purchase!", 0.918, 0.345, 0.047)
    draw_text("F1", 10.5, 72, 604, "We are thrilled to welcome you and your furry friend to CatCoding!", 0.20, 0.20, 0.20)
    draw_text("F1", 10.5, 72, 588, "This hub was crafted to provide stimulating, safe, and engaging entertainment", 0.20, 0.20, 0.20)
    draw_text("F1", 10.5, 72, 572, "engineered specifically for feline predatory instincts and curiosity.", 0.20, 0.20, 0.20)
    draw_text("F3", 9.5, 72, 554, "Created with care by arbaazalim | Lifetime Access Included", 0.45, 0.45, 0.45)

    # 5. Prominent Live Web Access Button / Card
    btn_x = 50
    btn_y = 440
    btn_w = width - 100
    btn_h = 76

    # Button shadow
    set_fill_color(0.110, 0.098, 0.090)
    draw_rect(btn_x + 4, btn_y - 4, btn_w, btn_h, fill=True, stroke=False)
    # Button main (Teal #0F766E background)
    set_fill_color(0.059, 0.463, 0.431)
    set_stroke_color(0.110, 0.098, 0.090)
    set_line_width(2.0)
    draw_rect(btn_x, btn_y, btn_w, btn_h, fill=True, stroke=True)

    draw_text("F2", 11, btn_x + 24, btn_y + 50, "CLICK TO LAUNCH THE WEB APP INSTANTLY (ONLINE):", 1.0, 0.85, 0.30)
    draw_text("F2", 15, btn_x + 24, btn_y + 28, "https://intzarbaz.github.io/catcoding-games-hub/", 1.0, 1.0, 1.0)
    draw_text("F1", 9.5, btn_x + 24, btn_y + 12, "Works in any modern browser on iPad, Android tablets, phones, and laptops.", 0.90, 0.95, 0.95)

    # 6. Two-Column Feature & Quickstart Cards
    col_w = (width - 116) / 2
    col_h = 250

    # Left Column: Included Games & Hub Modules
    col1_x = 50
    col1_y = 168
    # shadow
    set_fill_color(0.110, 0.098, 0.090)
    draw_rect(col1_x + 3, col1_y - 3, col_w, col_h, fill=True, stroke=False)
    # box
    set_fill_color(1.0, 1.0, 1.0)
    set_stroke_color(0.110, 0.098, 0.090)
    set_line_width(1.5)
    draw_rect(col1_x, col1_y, col_w, col_h, fill=True, stroke=True)

    # Title bar
    set_fill_color(0.98, 0.93, 0.84)
    draw_rect(col1_x, col1_y + col_h - 28, col_w, 28, fill=True, stroke=True)
    draw_text("F2", 11, col1_x + 14, col1_y + col_h - 19, "INCLUDED GAMES & MODES", 0.11, 0.10, 0.09)

    games = [
        ("Laser Pointer Chase:", "Fast-moving target with organic jitter."),
        ("Mouse & Bug Hunt:", "Scurrying prey with natural pauses."),
        ("Koi Fish Pond:", "Calming ripples & darting visual targets."),
        ("Touch Lock Protection:", "Prevents kitty from closing the game."),
        ("Sound Enrichment:", "High-frequency chirps, clicks & purrs."),
        ("Behavior Diary:", "Track playtime, mood & activity logs.")
    ]
    cur_y = col1_y + col_h - 48
    for title, desc in games:
        draw_text("F2", 9.5, col1_x + 14, cur_y, "* " + title, 0.918, 0.345, 0.047)
        draw_text("F1", 9.0, col1_x + 24, cur_y - 12, desc, 0.25, 0.25, 0.25)
        cur_y -= 31

    # Right Column: Setup Tips & Offline Play
    col2_x = 50 + col_w + 16
    col2_y = 168
    # shadow
    set_fill_color(0.110, 0.098, 0.090)
    draw_rect(col2_x + 3, col2_y - 3, col_w, col_h, fill=True, stroke=False)
    # box
    set_fill_color(1.0, 1.0, 1.0)
    set_stroke_color(0.110, 0.098, 0.090)
    set_line_width(1.5)
    draw_rect(col2_x, col2_y, col_w, col_h, fill=True, stroke=True)

    # Title bar
    set_fill_color(0.98, 0.93, 0.84)
    draw_rect(col2_x, col2_y + col_h - 28, col_w, 28, fill=True, stroke=True)
    draw_text("F2", 11, col2_x + 14, col2_y + col_h - 19, "QUICKSTART & OFFLINE USE", 0.11, 0.10, 0.09)

    tips = [
        ("1. Best Device Setup:", "Place your tablet flat on a rug or sofa."),
        ("2. Enable Screen Lock:", "Use Guided Access (iOS) or App Pin (Android)."),
        ("3. Exit Game Mode:", "Hold the exit ring for 2 seconds to unlock."),
        ("4. Play 100% Offline:", "Save the attached HTML file to your device."),
        ("   No Internet Needed:", "Double-tap the HTML file to play anywhere!"),
        ("5. Screen Protection:", "A tempered glass protector is recommended.")
    ]
    cur_y = col2_y + col_h - 48
    for title, desc in tips:
        draw_text("F2", 9.5, col2_x + 14, cur_y, title, 0.059, 0.463, 0.431)
        draw_text("F1", 9.0, col2_x + 24, cur_y - 12, desc, 0.25, 0.25, 0.25)
        cur_y -= 31

    # 7. Bottom Support & Store Card
    bot_y = 66
    bot_h = 78
    set_fill_color(1.0, 1.0, 1.0)
    set_stroke_color(0.110, 0.098, 0.090)
    set_line_width(1.5)
    draw_rect(50, bot_y, width - 100, bot_h, fill=True, stroke=True)

    draw_text("F2", 11, 68, bot_y + 54, "NEED HELP OR HAVE QUESTIONS?", 0.918, 0.345, 0.047)
    draw_text("F1", 9.5, 68, bot_y + 38, "Visit your creator store: https://arbaazalim.gumroad.com", 0.15, 0.15, 0.15)
    draw_text("F1", 9.0, 68, bot_y + 22, "Check back anytime for game updates, new levels, and more cat enrichment releases.", 0.35, 0.35, 0.35)
    draw_text("F3", 8.5, 68, bot_y + 8, "CatCoding 2026. All rights reserved. Built for happy, active cats worldwide.", 0.55, 0.55, 0.55)

    stream_data = "\n".join(stream_lines).encode("latin1")

    # Build PDF Objects
    # Obj 1: Catalog
    # Obj 2: Pages
    # Obj 3: Page 1
    # Obj 4: Font Helvetica (F1)
    # Obj 5: Font Helvetica-Bold (F2)
    # Obj 6: Font Helvetica-Oblique (F3)
    # Obj 7: Link annotation for Live Game
    # Obj 8: Link annotation for Gumroad Store
    # Obj 9: Content Stream

    pdf_body = []
    offsets = []

    def append_obj(obj_str):
        offset = sum(len(p) for p in pdf_body)
        offsets.append(offset)
        pdf_body.append(obj_str.encode("latin1"))

    # Header
    pdf_body.append(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

    # Obj 1: Catalog
    append_obj("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")

    # Obj 2: Pages
    append_obj("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")

    # Obj 3: Page 1
    page_dict = (
        "3 0 obj\n"
        "<< /Type /Page\n"
        "   /Parent 2 0 R\n"
        f"   /MediaBox [0 0 {width} {height}]\n"
        "   /Contents 9 0 R\n"
        "   /Resources <<\n"
        "      /Font <<\n"
        "         /F1 4 0 R\n"
        "         /F2 5 0 R\n"
        "         /F3 6 0 R\n"
        "      >>\n"
        "   >>\n"
        "   /Annots [7 0 R 8 0 R]\n"
        ">>\nendobj\n"
    )
    append_obj(page_dict)

    # Obj 4: Font F1 (Helvetica)
    append_obj("4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")

    # Obj 5: Font F2 (Helvetica-Bold)
    append_obj("5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")

    # Obj 6: Font F3 (Helvetica-Oblique)
    append_obj("6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique >>\nendobj\n")

    # Obj 7: Link annotation for Game URL (over the prominent teal button)
    # Button rect: [50, 440, 50+btn_w, 440+btn_h]
    append_obj(
        "7 0 obj\n"
        f"<< /Type /Annot /Subtype /Link /Rect [{btn_x} {btn_y} {btn_x + btn_w} {btn_y + btn_h}]\n"
        "   /Border [0 0 0]\n"
        "   /A << /S /URI /URI (https://intzarbaz.github.io/catcoding-games-hub/) >>\n"
        ">>\nendobj\n"
    )

    # Obj 8: Link annotation for Store URL in footer
    append_obj(
        "8 0 obj\n"
        f"<< /Type /Annot /Subtype /Link /Rect [68 {bot_y + 30} 380 {bot_y + 50}]\n"
        "   /Border [0 0 0]\n"
        "   /A << /S /URI /URI (https://arbaazalim.gumroad.com) >>\n"
        ">>\nendobj\n"
    )

    # Obj 9: Content Stream
    stream_header = f"9 0 obj\n<< /Length {len(stream_data)} >>\nstream\n"
    stream_footer = "\nendstream\nendobj\n"
    content_obj = stream_header.encode("latin1") + stream_data + stream_footer.encode("latin1")
    offset = sum(len(p) for p in pdf_body)
    offsets.append(offset)
    pdf_body.append(content_obj)

    # xref
    xref_offset = sum(len(p) for p in pdf_body)
    xref_lines = [
        "xref\n",
        f"0 {len(offsets) + 1}\n",
        "0000000000 65535 f \n"
    ]
    for o in offsets:
        xref_lines.append(f"{o:010d} 00000 n \n")
    trailer = (
        "trailer\n"
        f"<< /Size {len(offsets) + 1}\n"
        "   /Root 1 0 R\n"
        ">>\n"
        "startxref\n"
        f"{xref_offset}\n"
        "%%EOF\n"
    )

    pdf_body.append("".join(xref_lines).encode("latin1"))
    pdf_body.append(trailer.encode("latin1"))

    with open(output_path, "wb") as f:
        for chunk in pdf_body:
            f.write(chunk)

    print(f"PDF generated successfully at {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output.pdf"
    build_pdf(out)
