#!/usr/bin/env python3
"""Render the round-2 newspaper image for news-image-20261125.

One page, 1024x1024: masthead, a tall left hero panel on the flooded Bogor
gold mine (mine-shaft cross-section drawn below the headline), two stacked
stories in the right column (Huawei verdict, Ukraine's 2027 funding gap),
a three-column row (Colombia, Bangladesh, North Korea) and a light
"ALSO TODAY" strip. Drawn from scratch with PIL + DejaVu fonts.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30

PAPER = (245, 240, 227)      # warm newsprint
PAPER_DARK = (236, 229, 211) # slightly darker panel
INK = (25, 25, 25)
RED = (163, 22, 33)
GREY = (96, 92, 84)
HERO_BG = (32, 36, 44)       # charcoal, not the round-1 navy
HERO_LINE = (232, 163, 61)   # amber
CREAM = (244, 238, 224)
WATER = (46, 95, 122)
AMBER = (232, 163, 61)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color=RED, size=17):
    f = font(SANS_B, size)
    draw.line([(x, y + 8), (x + 26, y + 8)], fill=color, width=4)
    draw.text((x + 34, y), text, font=f, fill=color)
    return y + 24


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # double outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---------- masthead (auto-fit so the title never overflows) ----------
    title = "THE WORLD IN ONE IMAGE"
    msize = 62
    while msize > 40:
        mast = font(SERIF_B, msize)
        tw = d.textlength(title, font=mast)
        if tw <= 940:
            break
        msize -= 2
    d.text(((W - tw) / 2, 30), title, font=mast, fill=INK)
    d.line([(MARGIN, 104), (W - MARGIN, 104)], fill=INK, width=3)
    d.line([(MARGIN, 109), (W - MARGIN, 109)], fill=INK, width=1)
    date_f = font(SANS_B, 25)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 118), date, font=date_f, fill=RED)
    sub_f = font(SANS, 15)
    sub = "ALL THE DAY'S NEWS — IN ONE PICTURE"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 148), sub, font=sub_f, fill=GREY)

    # ---------- hero row (y 178..566) ----------
    hero_y0, hero_y1 = 178, 566
    hero_x0, hero_x1 = MARGIN, 606
    right_x0, right_x1 = 624, W - MARGIN

    # left hero panel: flooded mine
    d.rounded_rectangle([hero_x0, hero_y0, hero_x1, hero_y1], radius=10,
                        fill=HERO_BG, outline=HERO_LINE, width=2)
    hx = hero_x0 + 22
    # kicker
    d.line([(hx, hero_y0 + 30), (hx + 26, hero_y0 + 30)], fill=AMBER, width=4)
    d.text((hx + 34, hero_y0 + 20), "INDONESIA  •  BOGOR",
           font=font(SANS_B, 17), fill=AMBER)
    # headline, three stacked lines (43px so the longest line clears the panel edge)
    hl = font(SERIF_B, 43)
    y = hero_y0 + 52
    for line in ["THREE DEAD", "AS FLOOD TRAPS 26", "IN GOLD MINE"]:
        d.text((hx, y), line, font=hl, fill=CREAM)
        y += 46
    d.line([(hx, y + 2), (hx + 210, y + 2)], fill=AMBER, width=3)
    # deck, kept to two lines so it never reaches the illustration band
    deck_f = font(SANS, 17)
    deck = ("Three bodies pulled from a 100-metre shaft after a river burst "
            "into an illegal mine. Twenty-three men still trapped.")
    y = draw_lines(d, wrap(d, deck, deck_f, hero_x1 - hx - 22), hx, y + 12,
                   deck_f, CREAM, 23)
    # mine-shaft cross-section band at the bottom of the panel
    band_y0 = hero_y1 - 106
    d.line([(hero_x0 + 14, band_y0), (hero_x1 - 14, band_y0)], fill=(70, 76, 88), width=1)
    # ground + shaft
    d.rectangle([hero_x0 + 14, band_y0 + 12, hero_x1 - 14, band_y0 + 16], fill=(70, 76, 88))
    shaft_x = hero_x0 + 300
    d.rectangle([shaft_x, band_y0 + 12, shaft_x + 46, hero_y1 - 14], fill=(12, 13, 16))
    # flood water in the shaft
    d.rectangle([shaft_x, hero_y1 - 46, shaft_x + 46, hero_y1 - 14], fill=WATER)
    d.line([(shaft_x, hero_y1 - 46), (shaft_x + 46, hero_y1 - 46)], fill=(120, 180, 210), width=2)
    # headlamp glows
    for lx, ly in [(shaft_x + 12, hero_y1 - 66), (shaft_x + 34, hero_y1 - 58)]:
        d.ellipse([lx - 4, ly - 4, lx + 4, ly + 4], fill=AMBER)
    # rain drops above ground
    for rx in range(hero_x0 + 40, hero_x1 - 40, 46):
        d.line([(rx, band_y0 + 2), (rx - 4, band_y0 + 9)], fill=(140, 160, 180), width=2)
    # rescue pump + hose on the surface (hose runs below the label, never through it)
    d.rectangle([hero_x0 + 52, band_y0 - 16, hero_x0 + 96, band_y0 + 12], fill=(120, 30, 38))
    d.line([(hero_x0 + 96, band_y0 + 8), (shaft_x + 8, band_y0 + 18)], fill=(200, 200, 200), width=3)
    d.text((hero_x0 + 108, band_y0 - 14), "PUMPS RUN ALL NIGHT",
           font=font(SANS_B, 13), fill=(160, 165, 175))
    shaft_note = "SHAFT 100 M DEEP  •  11 ESCAPED"
    sn_f = font(SANS_B, 12)
    d.text((hero_x1 - 14 - d.textlength(shaft_note, font=sn_f), hero_y1 - 30),
           shaft_note, font=sn_f, fill=(160, 165, 175))

    # right column: two stacked stories
    # --- Huawei ---
    y = hero_y0 + 2
    y = kicker(d, right_x0, y, "UNITED STATES")
    h_f = font(SERIF_B, 30)
    y = draw_lines(d, wrap(d, "HUAWEI GUILTY ON 10 OF 12 COUNTS", h_f, right_x1 - right_x0),
                   right_x0, y, h_f, INK, 36)
    deck2 = ("A Brooklyn jury convicts the Chinese giant of bank fraud, wire "
             "fraud, sanctions breaches and conspiring to steal trade secrets. "
             "Sentencing in September 2027.")
    y = draw_lines(d, wrap(d, deck2, font(SANS, 16), right_x1 - right_x0), right_x0,
                   y + 6, font(SANS, 16), INK, 22)
    d.line([(right_x0, y + 10), (right_x1, y + 10)], fill=GREY, width=1)
    # --- Ukraine ---
    y = y + 26
    y = kicker(d, right_x0, y, "UKRAINE")
    y = draw_lines(d, wrap(d, "KYIV NEEDS €115BN FOR 2027", h_f, right_x1 - right_x0),
                   right_x0, y, h_f, INK, 36)
    deck3 = ("Zelensky says Ukraine needs €115 billion in outside support next "
             "year. The EU has promised €90 billion — a €25 billion gap remains.")
    y = draw_lines(d, wrap(d, deck3, font(SANS, 16), right_x1 - right_x0), right_x0,
                   y + 6, font(SANS, 16), INK, 22)

    # ---------- three-column row (y 588..796) ----------
    d.line([(MARGIN, 580), (W - MARGIN, 580)], fill=INK, width=2)
    cols = [
        ("COLOMBIA", "ALL HOSTAGES FREED IN CARTAGENA SIEGE",
         "Troops storm an Exito supermarket after a day-long standoff and "
         "rescue every remaining captive. One kidnapper is killed; four are arrested."),
        ("BANGLADESH", "GARMENT PAY RISES 36% TO 17,000 TAKA",
         "Dhaka lifts the minimum wage for four million garment workers after "
         "weeks of protests that shut factories."),
        ("NORTH KOREA", "PYONGYANG EXPELS SWISS ENVOY IN 48 HRS",
         "Kim Jong Un's regime orders Switzerland's diplomatic office shut and "
         "its envoy out, in a row over sanctions on a children's camp."),
    ]
    col_w = (W - 2 * MARGIN - 2 * 18) // 3
    for i, (kick, head, body) in enumerate(cols):
        cx = MARGIN + i * (col_w + 18)
        y = 596
        y = kicker(d, cx, y, kick, size=16)
        hf = font(SERIF_B, 25)
        y = draw_lines(d, wrap(d, head, hf, col_w), cx, y, hf, INK, 30)
        y = draw_lines(d, wrap(d, body, font(SANS, 14), col_w), cx, y + 4,
                       font(SANS, 14), INK, 19)

    # ---------- ALSO TODAY strip (y 812..948), light panel ----------
    d.rectangle([MARGIN, 812, W - MARGIN, 948], fill=PAPER_DARK, outline=RED, width=2)
    d.text((MARGIN + 16, 822), "ALSO TODAY", font=font(SANS_B, 19), fill=RED)
    items = [
        ("ANTHROPIC", "Shares slide below the $83 IPO price, near $77."),
        ("RIYADH", "Houthis claim new strikes on a Saudi refinery."),
        ("BRITAIN", "UK warns firms backing Kyiv to expect sabotage."),
        ("HODEIDAH", "Coalition says it hit the port and Saada targets."),
        ("SHANGHAI", "China probes party chief Chen Jining."),
        ("EUROZONE", "Inflation rises to 4.0%, Eurostat reports."),
    ]
    cell_w = (W - 2 * MARGIN - 32 - 2 * 16) // 3
    for i, (lead, text) in enumerate(items):
        cx = MARGIN + 16 + (i % 3) * (cell_w + 16)
        cy = 852 + (i // 3) * 48
        lead_f = font(SANS_B, 13)
        d.text((cx, cy), lead, font=lead_f, fill=RED)
        lw = d.textlength(lead + "  ", font=lead_f)
        body_f = font(SANS, 13)
        lines = wrap(d, text, body_f, cell_w - lw)
        draw_lines(d, lines[:2], cx + lw, cy, body_f, INK, 17)

    # ---------- footer ----------
    foot = "Sources: Reuters  •  AP  •  AFP  •  Compiled from the day's wires, 25 November 2026  •  make.fun news-image-20261125"
    ff = font(SANS, 13)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 966), foot, font=ff, fill=GREY)

    img.save("entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
