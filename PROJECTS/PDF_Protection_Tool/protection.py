import PyPDF2
import sys
import os

def create_password_protected_pdf(input_pdf, output_pdf, password):
    try:
        with open(input_pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            pdf_writer.encrypt(password)

            # Prevent accidental overwrite
            if os.path.exists(output_pdf):
                confirm = input(f"File '{output_pdf}' already exists. Overwrite? (y/n): ")
                if confirm.lower() != 'y':
                    print("Operation cancelled.")
                    return

            with open(output_pdf, 'wb') as output_file:
                pdf_writer.write(output_file)

            print(f"✅ Password-protected PDF saved as: {output_pdf}")

    except FileNotFoundError:
        print(f"❌ The file '{input_pdf}' was not found.")
    except PyPDF2.errors.PdfReadError:
        print(f"❌ The file '{input_pdf}' is not a valid PDF.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 protection.py <input_pdf> <output_pdf> <password>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    password = sys.argv[3]

    create_password_protected_pdf(input_pdf, output_pdf, password)

if __name__ == "__main__":
    main()
