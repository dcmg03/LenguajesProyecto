from flask import Flask, render_template, request, redirect
import PyPDF2
import re
from PyPDF2 import PdfReader


app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No ha selecionado un archivo'

    if file:
        file.save(file.filename)
        pdf_file = open(file.filename, 'rb')
        pdf_reader = PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        pdf_file.close()

        # Expresiones regulares para extraer la información
        cliente_regex = r'Cliente\s+(.*?)\s*Nit\.?\s*C\.?C\.?\s*(\d{1,2}\.?\d{3}\.?\d{3}-?\d{1,2})'
        direccion_regex = r'Dirección\s+(.*?)\s*(\d+\s*[A-Za-z]*\s*[A-Za-z]+\s*(?=N|Norte|S|Sur|E|Este|O|Oeste)?\s*\d+\s*-\s*\d+)'

        #direccion_regex = r'Dirección\s+(.*?)\s+(\d+\s*[A-Za-z]*\s*[A-Za-z]+\s*\d+\s*-\s*\d+)'

        consumo_regex = r'Consumo\s+en\s*\(KWh\)\s*(\d+)'
        valor_total_regex = r'VALOR\s+TOTAL\s+A\s+PAGAR\s+\$([\d,.]+)'
        nit_cc_regex = r'Nit\.\s*C\.C\.\s*(\d+)'
        ciudad_regex = r'Ciudad\s+(\w+)'
        fecha_corte_regex = r'PAGO\s+OPORTUNO\s+ANTES\s+DE\s+(\d{1,2}\/[A-Za-z]{3}\/\d{4})'



        try:
            consumo_match = re.search(consumo_regex, text)
            if consumo_match:
                consumo = consumo_match.group(1)
            else:
                consumo = "0"  # O cualquier otro valor por defecto que desees
        except Exception as e:
            print(f"Error al buscar el consumo: {e}")
            consumo = "0"

        try:
            cliente_match = re.search(cliente_regex, text)
            if cliente_match:
                cliente = cliente_match.group(1)
            else:
                cliente = ""

        except Exception as e:
            print(f"Error al buscar el cliente: {e}")
            cliente = "N/A"

        try:
            nit_cc_match = re.search(nit_cc_regex, text)
            if nit_cc_match:
                nit_cc = nit_cc_match.group(1)
            else:
                nit_cc = ""

        except Exception as e:
            print(f"Error al buscar el NIT/CC: {e}")
            nit_cc = "N/A"

        try:

            direccion_match = re.search(direccion_regex, text)
            if direccion_match:
                direccion = direccion_match.group(1)
            else:
                direccion = ""

        except Exception as e:
            print(f"Error al buscar la dirección: {e}")
            direccion = "N/A"

        try:
            ciudad_match = re.search(ciudad_regex, text)
            if ciudad_match:
                ciudad = ciudad_match.group(1)
            else:
                ciudad = ""
        except Exception as e:
            print(f"Error al buscar la ciudad: {e}")
            ciudad = "N/A"

        try:
            valor_total_match = re.search(valor_total_regex, text)
            if valor_total_match:
                valor_total = valor_total_match.group(1) if valor_total_match else None
            else:
                valor_total = "0"
            # valor_total = re.search(valor_total_regex, text).group(1)
        except Exception as e:
            print(f"Error al buscar el valor total: {e}")
            valor_total = "N/A"

        try:
            fecha_corte_match = re.search(fecha_corte_regex, text)
            if fecha_corte_match:
                fecha_corte = fecha_corte_match.group(1)
            else:
                fecha_corte = "0"
        except Exception as e:
            print(f"Error al buscar la fecha: {e}")
            fecha_corte = "N/A"

        return render_template('tabla.html', cliente=cliente, nit_cc=nit_cc, direccion=direccion,
                               ciudad=ciudad, consumo=consumo, valor_total=valor_total,fecha_corte=fecha_corte)


print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
