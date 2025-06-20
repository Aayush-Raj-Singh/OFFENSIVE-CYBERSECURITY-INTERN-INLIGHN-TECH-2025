import pikepdf
import itertools
from concurrent.futures import ThreadPoolExecutor

def generate_passwords(charset, min_length, max_length):
    for length in range(min_length, max_length + 1):
        for password in itertools.product(charset, repeat=length):
            yield ''.join(password)

def load_passwords(wordlist_file):
    with open(wordlist_file, 'r') as f:
        for line in f:
            yield line.strip()

def try_password(pdf_path, password):
    try:
        with pikepdf.open(pdf_path, password=password):
            return password
    except pikepdf._core.PasswordError:
        return None
    except Exception as e:
        return f"[ERROR] {e}"

def crack_pdf(pdf_path, passwords, max_workers=4, progress_callback=None):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_pwd = {executor.submit(try_password, pdf_path, pwd): pwd for pwd in passwords}
        for i, future in enumerate(future_to_pwd):
            result = future.result()
            if progress_callback:
                progress_callback(i + 1)
            if result and not result.startswith("[ERROR]"):
                return result
    return None
