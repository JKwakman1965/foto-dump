import os
import subprocess
import base64
from ftplib import FTP

def connect_to_wifi(ssid, bssid, encoded_password):
    """
    Verbinding maken met een Wi-Fi-netwerk met behulp van ssid, bssid en een Base64-gecodeerd wachtwoord.
    """
    try:
        wifi_password = base64.b64decode(encoded_password).decode('utf-8')

        # Voeg een nieuwe verbinding toe
        subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'bssid', bssid, 'password', wifi_password], check=True)
        print("Verbonden met Wi-Fi")
    except subprocess.CalledProcessError as e:
        print(f"Kon geen verbinding maken met Wi-Fi: {e}")
        exit(1)

def upload_photos_to_ftp(ftp_server, username, password, local_folder, remote_folder):
    """
    Upload foto's naar een FTP-server.
    """
    try:
        ftp = FTP(ftp_server)
        ftp.login(user=username, passwd=password)
        ftp.cwd(remote_folder)
        print("Verbonden met FTP-server")

        for filename in os.listdir(local_folder):
            if filename.lower().endswith(('png', 'jpg', 'jpeg')):
                filepath = os.path.join(local_folder, filename)
                with open(filepath, 'rb') as file:
                    ftp.storbinary(f'STOR {filename}', file)
                    print(f"{filename} geüpload")

        ftp.quit()
        print("Upload voltooid")
    except Exception as e:
        print(f"Fout bij FTP-upload: {e}")
        exit(1)

if __name__ == "__main__":
    # Wi-Fi instellingen
    ssid = "draadloos"
    bssid = "00:11:2F:A2:97:67"
    encoded_wifi_password = "RGl0X2lzX25pZXRfaGVlbF92ZWlsaWc="

    # FTP instellingen
    ftp_server = "Nog FTP server maken"
    ftp_username = "Jacko_debeste"
    ftp_password = "GeheimW@chtwoord!2024"
    local_folder = "/pad/naar/foto's"
    remote_folder = "/pad/naar/upload/map"

    # Verbinden met Wi-Fi
    connect_to_wifi(ssid, bssid, encoded_wifi_password)

    # Foto's uploaden naar FTP-server
    upload_photos_to_ftp(ftp_server, ftp_username, ftp_password, local_folder, remote_folder)
