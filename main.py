from PIL import Image, ImageDraw, ImageFont


def generate_certificate(name):
    # Load certificate template image
    # Replace "certificate_template.png" with your template image path
    certificate_img = Image.open("certificate_template2.png")

    # Initialize drawing context
    draw = ImageDraw.Draw(certificate_img)

    # Load font
    # font_path = "BrittanySignature.ttf"
    font_path = "horizon.otf"
    font = ImageFont.truetype(font_path, 60)

    # Calculate text position
    # text = "Certificate of Completion"
    # text_position = ((certificate_img.width - draw.textlength(text, font=font)) / 2, 100)

    # Draw text
    # draw.text(text_position, text, fill="black", font=font)

    certificate_text = name
    certificate_font = ImageFont.truetype(font_path, 200)
    certificate_text_position = (
        (certificate_img.width - draw.textlength(certificate_text, font=certificate_font)) / 2, 2100)

    draw.text(certificate_text_position, certificate_text,
              fill="white", font=certificate_font)

    certificate_text = "This certificate is awarded to her/his for being winner of Fauget Esport Tournament"

    certificate_font = ImageFont.truetype(font_path, 50)
    certificate_text_position = (
        (certificate_img.width - draw.textlength(certificate_text, font=certificate_font)) / 2, 2500)

    draw.text(certificate_text_position, certificate_text,
              fill="white", font=certificate_font)

    certificate_text = "Fauget Esport Tournament"

    certificate_font = ImageFont.truetype(font_path, 50)
    certificate_text_position = (
        (certificate_img.width - draw.textlength(certificate_text, font=certificate_font)) / 2, 2500)

    draw.text(certificate_text_position, certificate_text,
              fill="white", font=certificate_font)

    certificate_img.save(f"{name}_certificate.png")


if __name__ == "__main__":
    # name = input("Enter your name: ")
    name = "Karan Kumar Agrawal"
    # names_list = ["Karan Kumar Agrawal", "Ayush Rai",
    #               "Kartik Saraf", "Prikshit Sharma", "Manmohan Kumar"]
    # for name in names_list:
    #     generate_certificate(name)
    generate_certificate(name)

    print("Certificate generated successfully!")
