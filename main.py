from PIL import Image, ImageDraw, ImageFont


class certificategenerator:
    def __init__(self):
        # self.name = input("Enter your name: ")
        self.templateno = int(input("Enter template number: "))
        self.name = "Karan Kumar Agrawal"
        self.generate_certificate(self.name, self.templateno)

    def generate_certificate(self, name, templateno):
        if (templateno == 1):
            certificate_img = Image.open("templates/certificate_template.png")
            draw = ImageDraw.Draw(certificate_img)
            font_path = "fonts/BrittanySignature.ttf"

            text = name
            font = ImageFont.truetype(font_path, 500)
            text_position = (
                (certificate_img.width - draw.textlength(text, font=font)) / 2, 1800)
            draw.text(text_position, text, fill="black", font=font)

        elif (templateno == 2):
            certificate_img = Image.open("templates/certificate_template2.png")
            draw = ImageDraw.Draw(certificate_img)
            font_path = "fonts/horizon.otf"

            certificate_text = name
            certificate_font = ImageFont.truetype(font_path, 200)
            certificate_text_position = (
                (certificate_img.width - draw.textlength(certificate_text, font=certificate_font)) / 2, 2100)
            draw.text(certificate_text_position, certificate_text,
                      fill="white", font=certificate_font)

            certificate_text = "This certificate is awarded to his/her for participating in"
            certificate_font = ImageFont.truetype(font_path, 75)
            certificate_text_position = (
                (certificate_img.width - draw.textlength(certificate_text, font=certificate_font)) / 2, 2500)
            draw.text(certificate_text_position, certificate_text,
                      fill="white", font=certificate_font)

            certificate_text = "MIRAGE 1.0"
            certificate_font = ImageFont.truetype(font_path, 75)
            certificate_text_position = (
                (certificate_img.width - draw.textlength(certificate_text, font=certificate_font)) / 2, 2600)
            draw.text(certificate_text_position, certificate_text,
                      fill="white", font=certificate_font)

        certificate_img.save(f"certificates/{name}_certificate.png")
        print("Certificate generated successfully!")


if __name__ == "__main__":
    app = certificategenerator()
