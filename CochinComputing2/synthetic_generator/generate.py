from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os
from faker import Faker
from datetime import datetime, timedelta
import qrcode


TEMPLATE_PATH = "/Users/abhinavk/CochinComputing2/synthetic_generator/template.png"
TEMPLATE_VOTE="/Users/abhinavk/CochinComputing2/synthetic_generator/voteridtemp.png"
TEMPLATE_PAN="/Users/abhinavk/CochinComputing2/synthetic_generator/pancardtemplate.png"
FONT_ENGLISH = "/Users/abhinavk/CochinComputing2/synthetic_generator/assets/fonts/Roboto-Black.ttf"
OUTPUT_DIR = "output/aadhaar"
OUTPUT_DIR2="output/pan"
OUTPUT_DIR3="output/voter"

font_en = ImageFont.truetype(FONT_ENGLISH, 50)
font_pan = ImageFont.truetype(FONT_ENGLISH, 20)
fake = Faker('en_IN')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_qr(data, path):
    qr = qrcode.make(data,border=0)
    qr = qr.resize((300, 300))
    qr.save(path)

def add_text(draw, position, text, font, fill=(0, 0, 0)):
    draw.text(position, text, font=font, fill=fill)

def create_aadhaar_image(index):
    # Load base template

    base = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(base)

    # Load fonts
    
    font_no = ImageFont.truetype(FONT_ENGLISH, 70)

    # Random details
    gender = random.choice(["Male", "Female"])
    name = fake.name_male() if gender == "Male" else fake.name_female()
    dob = f"{random.randint(1,28):02}/{random.randint(1,12):02}/{random.randint(1975, 2005)}"
    aadhaar_no = f"{random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"

    # Add details to template
    add_text(draw, (700, 345), f": {name}", font_en)
    add_text(draw, (680, 435), f" {dob}", font_en)
    add_text(draw, (750, 530), f" {gender}", font_en)
    add_text(draw, (500, 655), f"{aadhaar_no}", font_no)

    # Add QR code
    qr_path = f"output/qr_temp.png"
    generate_qr(f"{name}|{dob}|{aadhaar_no}", qr_path)
    qr = Image.open(qr_path)
    base.paste(qr, (1100, 450))

    # Add slight blur or noise
    if random.random() < 0.5:
        base = base.filter(ImageFilter.GaussianBlur(radius=0.5))

    # Save image
    base.save(os.path.join(OUTPUT_DIR, f"aadhaar_{index}.jpg"))
    
def create_voter_id_image(index): #voterid
    base = Image.open(TEMPLATE_VOTE).convert("RGB")
    draw = ImageDraw.Draw(base)

    name = fake.name()
    father_name = fake.name_male()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%d-%m-%Y")
    gender = random.choice(["MALE", "FEMALE"])
    epic_number = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3)) + ''.join(random.choices("0123456789", k=7))
    constituency = fake.city()

    draw.text((300, 1050), f"{name}", font=font_en, fill=(0, 0, 0))
    draw.text((650, 1170), f"{father_name}", font=font_en, fill=(0, 0, 0))
   
    draw.text((400, 1280), f"{epic_number}", font=font_en, fill=(0, 0, 0))
    draw.text(( 65, 1400), f"Constituency: {constituency}", font=font_en, fill=(0, 0, 0))

    base.save(os.path.join(OUTPUT_DIR3,f"voterid{index}.png"))

def create_pan_card_image(index):  #pancard
    base = Image.open(TEMPLATE_PAN).convert("RGB")
    draw = ImageDraw.Draw(base)

    name = fake.name()
    father_name = fake.name_male()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%d/%m/%Y")
    pan_number = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + \
                 ''.join(random.choices("0123456789", k=4)) + \
                 random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    draw.text((30, 100), f"Name: {name}", font=font_pan, fill=(0, 0, 0))
    draw.text((30, 130), f"Father's Name: {father_name}", font=font_pan, fill=(0, 0, 0))
    draw.text((30, 160), f"DOB: {dob}", font=font_pan, fill=(0, 0, 0))
    draw.text((30, 210), f"{pan_number}", font=font_pan, fill=(0, 0, 0))

    base.save(os.path.join(OUTPUT_DIR2,f"pan{index}.png"))

def create_passport_image(index): #passport
    base = Image.open("template_passport.png").convert("RGB")
    draw = ImageDraw.Draw(base)

    name = fake.name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    passport_number = random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") + ''.join(random.choices("0123456789", k=7))
    issue_date = dob + timedelta(days=18*365)
    expiry_date = issue_date + timedelta(days=10*365)

    draw.text((50, 100), f"Name: {name}", font=font_en, fill=(0, 0, 0))
    draw.text((50, 160), f"Passport No: {passport_number}", font=font_en, fill=(0, 0, 0))
    draw.text((50, 220), f"DOB: {dob.strftime('%d-%m-%Y')}", font=font_en, fill=(0, 0, 0))
    draw.text((50, 280), f"Issue Date: {issue_date.strftime('%d-%m-%Y')}", font=font_en, fill=(0, 0, 0))
    draw.text((50, 340), f"Expiry Date: {expiry_date.strftime('%d-%m-%Y')}", font=font_en, fill=(0, 0, 0))

    base.save(os.path.join(OUTPUT_DIR2,f"passport{index}.png"))
def create_drivers_license_image(index):    #driver
    base = Image.open("template_dl.png").convert("RGB")
    draw = ImageDraw.Draw(base)

    name = fake.name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%d/%m/%Y")
    dl_number = f"KL{random.randint(1, 99):02d} {datetime.now().year}00{random.randint(10000,99999)}"
    issue_date = datetime.now() - timedelta(days=random.randint(100, 3000))
    expiry_date = issue_date + timedelta(days=365 * 20)

    draw.text((50, 100), f"Name: {name}", font=font_en, fill=(0, 0, 0))
    draw.text((50, 160), f"DOB: {dob}", font=font_en, fill=(0, 0, 0))
    draw.text((50, 220), f"DL No: {dl_number}", font=font_en, fill=(0, 0, 0))
    draw.text((50, 280), f"Issue Date: {issue_date.strftime('%d-%m-%Y')}", font=font_en, fill=(0, 0, 0))
    draw.text((50, 340), f"Valid Till: {expiry_date.strftime('%d-%m-%Y')}", font=font_en, fill=(0, 0, 0))

    base.save(os.path.join(OUTPUT_DIR2,f"drivers{index}.png"))
# Generate 1000 images
for i in range(1000):
    create_aadhaar_image(i)
    create_voter_id_image(i)
    create_pan_card_image(i)
    print(i,"loop done")


print("Generated a thousand images")
