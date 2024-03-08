import unittest
import io
from flask import Flask, request
import re
from main import app, cliente_regex, direccion_regex, consumo_regex, valor_total_regex, nit_cc_regex, ciudad_regex, fecha_corte_regex

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Inicializar la aplicación Flask para pruebas
        self.app = app.test_client()

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_index_route(self):

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)  # Verifica si la respuesta tiene algún contenido
        #self.assertIn(b'<title>Subir Factura </title>', response.data)





    def test_regex_patterns(self):
        # Texto de prueba
        test_text = "NIT. 891.800.219-1 www.ebsa.com.co O:R: EBSA E.S.P. Cra 10 No.15-87 Tunja Tel 7405000 Somos Autorretenedores Res. DIAN 0547 de 2002 y grandes contribuyentes Res. 076 de 2016. Vigilada Superservicios.30537 NÚMERO DE CUENTA 959206473 DOCUMENTO EQUIVALENTE N° 000194311161 PERIODO DEL SERVICIO 17/12/2023 - 16/01/2024 PERIODO FACTURADO ENE-2024 A ENE-2024 FECHA DE EMISIÓN 19/ENE/2024 TIPO DE FACTURA: FACTURACIÓN: Mensual INFORMACIÓN CLIENTE EVOLUCIÓN DE SU CONSUMO Cliente MORENO RAMIREZ CARLOS HUMBERTO Nit. C.C. 79240660 Nit. A. Dirección Urbano C 3S N 15 - 07 Ciudad Sogamoso Contacto APTipo Código DIC NOV OCT SEP AGO JUL Promedio 3 activa 0 32 69 82 2 0 30 INFORMACIÓN TÉCNICA DETERMINACIÓN DE SU CONSUMO CUENTA 959206473 Ruta Entrega 005- 0000019620500 Estrato 2-B Clase Servicio Residencial Cargo (kw) 4.0 Nivel Tensión Secundaria Medidor No. HOLLEY 051306299 Medidor No. Tipo Medidor medidor activa Tipo Medidor Circuito 14843 Nodo Conexión 4599TipoCódigo InternoLectura AnteriorLectura ActualFactor Mult.Consumo en (KWh)Observ. Lectura AS Contador-3 10536 10575 1 39 14 0 CALIDAD DEL SERVICIO DETALLE DE SU CUENTA Mes Diu Dium Diug Fiu Fium Fiug 1 .7762 0 2.71 2 0 8Descripción Cantidad Periodo Subsidio / Contribución VALOR TOTAL 3-Activa-Sencilla 39 2024/01 % 50 $ 17,485 COSTO DE PRESTACIÓN DEL SERVICIO G T D R P Cv Cf CU 359.53 60.18 272.20 0.70 66.30 137.78 0.00 896.69 G+T+D+P+R+Cv+Cf INFORMACIÓN DE PAGOS VALOR TOTAL CONSUMO $ 34,971 VALOR (SUBSIDIO/CONTRIBUCIÓN) % 50 $ -17,486 VALOR CONSUMO FACTURADO $ 17,485Valor Último Pago $ 9,510 Fecha 2023-12-28 00:00:00 Saldo esta Factura $ 0Remanente Recaudo $ 0 Periodo Cobro: ENE-2024 hasta ENE-2024 INFORMACIÓN SUBSIDIO FOES DETALLE DE LA FACTURA Consumo (kwh) V/Total FOES ($) Valor Unitario ($/kWh) No. FacturaValor factura periodo 17,485 I.A.P AC-MPAL-032-2016 9,507 Ajuste Decena -2 0 0 0 0 0 0 0INFORMACIÓN DE INTERES En EBSA pensamos en el medio ambiente, por eso te invitamos a hacer uso racional de energia, apagando las luces de tu casa antes de salir, para conocer mas tips ingresa a nuestra pagina www.ebsa.com.co El valor por la prestación del servicio es de $912.7141 por kWh, sin embargo por la aplicación de la Resoluciones CREG 058 y la 012 del 2020 el Costo Unitario aplicado a esta factura es de $896.691 por kWh Por el no pago en la fecha establecida se procede a la suspensión del servicio, contra esta comunicación proceden los recursos de reposición ante EBSA y en subsidio al de apelación ante la superservicios dentro de los cinco días siguientes contados a partir de la estrega de esta factura.. Este documento es equivalente a la factura presta merito ejecutivo de conformidad con el Articulo 130 de la ley 142 de 1994 y de conformidad con el Artículo 772 del código de comercio. El presente documento es equivalente a la factura se asimila en sus efectos a la letra de cambio (Art. 774 del código de comercio).VALOR TOTAL A PAGAR $26,990 PAGO OPORTUNO ANTES DE 01/FEB/2024 DETALLE FINANCIACION Descripcion Valor Cuotas Cuotas Pendientes Saldo Intereses Periodicidad A partir de NIT. 891.800.219-1DOCUMENTO EQUIVALENTE N°000194311161 NÚMERO DE CUENTA 959206473 PERIODO FACTURADO ENE-2024 A ENE-2024 ÍÊIYfÇÆÂ$sp4)[4`iÊGÂÂÂezSÎ (415)7709998000483(8020)0959206473(3900)0000026990PAGO OPORTUNO ANTES DE: 01/FEB/2024 VALOR A PAGAR $26,990"
        #prueba de las exprsiones regulares
        cliente_match = re.search(cliente_regex, test_text)
        self.assertIsNotNone(cliente_match, "No se encontró la información del cliente en el texto de la factura")
        if cliente_match:
            self.assertEqual(cliente_match.group(1), "MORENO RAMIREZ CARLOS HUMBERTO")


        self.assertEqual(re.search(direccion_regex, test_text).group(1), "Urbano C ")
        self.assertEqual(re.search(consumo_regex, test_text).group(1), "39")
        self.assertEqual(re.search(valor_total_regex, test_text).group(1), "26")
        self.assertEqual(re.search(nit_cc_regex, test_text).group(1), "79240660")
        self.assertEqual(re.search(ciudad_regex, test_text).group(1), "Sogamoso")
        self.assertEqual(re.search(fecha_corte_regex, test_text).group(1), "01/FEB/2024")

if __name__ == '__main__':
    unittest.main()
