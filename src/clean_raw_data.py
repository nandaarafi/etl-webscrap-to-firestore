import pandas as pd

substrings_to_remove = [
    "\n",
    ".",
    "PENGGUNAAN OBAT INI HARUS SESUAI DENGAN PETUNJUK DOKTER",
    "ATURAN PAKAI HARUS SESUAI DENGAN PETUNJUK DOKTER"
]

def clean_text(text):
    for substring in substrings_to_remove:
        text = text.replace(substring, "")
    return text.strip()
    

if __name__ == "__main__":
    data = pd.read_csv('../resources/produk_raw.csv')
    data['Dosis'] = data['Dosis'].apply(clean_text)
    data.to_csv('../resources/produk_clean.csv', index=False)
