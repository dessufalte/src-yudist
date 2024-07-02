import qrcode

def generate_qr_symbolic_string(bytea_data):
    try:
        # Konversi data bytea ke dalam bentuk string
        data_string = bytea_data.decode('utf-8')

        # Buat QR code dari string simbolik
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_string)
        qr.make(fit=True)

        # Menghasilkan QR code dalam bentuk PNG (atau format lainnya)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Simpan QR code ke file sementara atau proses lebih lanjut
        qr_image.save('qr_code.png')
        
        # Mengembalikan nama file QR code
        return 'qr_code.png'

    except Exception as e:
        print(f'Error generating QR code: {e}')
        return None
generate_qr_symbolic_string("s")