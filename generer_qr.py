import qrcode

# ⚠️ REMPLACE L'URL CI-DESSOUS PAR CELLE DE TON APPLICATION
url = "https://projet-cafe-hntxjjs4mrwgvqrzm5u6fe.streamlit.app" 

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_code_cafe.png")

print("QR Code généré avec succès ! Regarde sur ton bureau.")