"""Garment/detail detection returning all matching details."""
from ._common import detect_many

VOCAB = {
    "Lace Trim": ("lace trim", "lace"), "Raw Hem": ("raw hem", "frayed hem"), "Ribbed": ("ribbed",),
    "Pleated": ("pleated",), "Ruched": ("ruched",), "Smocked": ("smocked",), "Quilted": ("quilted",),
    "Padded": ("padded",), "Woven": ("woven",), "Embroidered": ("embroidered",), "Beaded": ("beaded",),
    "Sequined": ("sequined", "sequin"), "Embellished": ("embellished",), "Cutout": ("cutout", "cut-out"),
    "Mesh Panel": ("mesh panel",), "Sheer Panel": ("sheer panel",), "Button Front": ("button front",),
    "Exposed Zipper": ("exposed zipper",), "Tie Waist": ("tie waist",), "Belted Waist": ("belted waist",),
    "Drawstring Waist": ("drawstring waist",), "Elastic Waist": ("elastic waist",), "Puff Sleeve": ("puff sleeve",),
    "V-Neck": ("v-neck", "v neck"), "Square Neck": ("square neck",), "Halter Neck": ("halter neck",),
    "Off Shoulder": ("off shoulder", "off-shoulder"), "Tailored Fit": ("tailored fit",),
    "Relaxed Fit": ("relaxed fit",), "Cinched Waist": ("cinched waist",), "Side Slit": ("side slit",),
    "Satin Finish": ("satin finish",), "Matte Finish": ("matte finish",), "Gold Hardware": ("gold hardware",),
    "Silver Hardware": ("silver hardware",), "Quiet Luxury Detail": ("quiet luxury",),
    "Statement Detail": ("statement detail",), "Refined Detail": ("refined detail",),
}

def detect_details(text: str) -> list[str]:
    return detect_many(text, VOCAB)
