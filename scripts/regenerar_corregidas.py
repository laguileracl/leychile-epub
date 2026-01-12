#!/usr/bin/env python3
"""Script para regenerar archivos XML con idNorma corregidos."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from leychile_epub.xml_generator import BibliotecaXMLGenerator

leyes_corregidas = {
    "codigo_aeronautico": {
        "url": "https://www.leychile.cl/Navegar?idNorma=30287",
        "nombre": "Ley 18.916 - Codigo Aeronautico",
        "descripcion": "Aprueba Codigo Aeronautico.",
    },
    "ley_17235_impuesto_territorial": {
        "url": "https://www.leychile.cl/Navegar?idNorma=128563",
        "nombre": "DFL 1 - Ley 17.235 Impuesto Territorial",
        "descripcion": "Fija texto refundido de la Ley 17.235 sobre Impuesto Territorial.",
    },
    "ley_18834_estatuto_administrativo": {
        "url": "https://www.leychile.cl/Navegar?idNorma=236392",
        "nombre": "DFL 29 - Estatuto Administrativo (Ley 18.834)",
        "descripcion": "Fija texto refundido de la Ley 18.834, sobre Estatuto Administrativo.",
    },
    "ley_18933_isapres": {
        "url": "https://www.leychile.cl/Navegar?idNorma=249177",
        "nombre": "DFL 1 - Ley de Isapres",
        "descripcion": "Texto refundido del DL 2.763 y Leyes de Isapres.",
    },
    "ley_19728_seguro_desempleo": {
        "url": "https://www.leychile.cl/Navegar?idNorma=184979",
        "nombre": "Ley 19.728 - Seguro de Desempleo",
        "descripcion": "Establece un seguro de desempleo.",
    },
    "ley_19865_financiamiento_urbano": {
        "url": "https://www.leychile.cl/Navegar?idNorma=208927",
        "nombre": "Ley 19.865 - Financiamiento Urbano Compartido",
        "descripcion": "Sobre financiamiento urbano compartido.",
    },
    "ley_21327_modernizacion_dt": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1158983",
        "nombre": "Ley 21.327 - Modernizacion Direccion del Trabajo",
        "descripcion": "Modernizacion de la Direccion del Trabajo.",
    },
    "ley_21400_matrimonio_igualitario": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1169572",
        "nombre": "Ley 21.400 - Matrimonio Igualitario",
        "descripcion": "Regula el matrimonio entre personas del mismo sexo.",
    },
    "ley_21459_delitos_informaticos": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1177743",
        "nombre": "Ley 21.459 - Delitos Informaticos",
        "descripcion": "Establece normas sobre delitos informaticos.",
    },
    "ley_21545_tea": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1190123",
        "nombre": "Ley 21.545 - Ley TEA",
        "descripcion": "Proteccion de personas con trastorno del espectro autista.",
    },
    "ley_3918_sociedades_responsabilidad_limitada": {
        "url": "https://www.leychile.cl/Navegar?idNorma=24349",
        "nombre": "Ley 3.918 - Sociedades de Responsabilidad Limitada",
        "descripcion": "Autoriza sociedades con responsabilidad limitada.",
    },
    "dl_825_iva": {
        "url": "https://www.leychile.cl/Navegar?idNorma=6369",
        "nombre": "DL 825 - Ley del IVA",
        "descripcion": "Ley sobre Impuesto a las Ventas y Servicios.",
    },
}

if __name__ == "__main__":
    print("Regenerando archivos XML con idNorma corregidos...")
    gen = BibliotecaXMLGenerator()
    gen.generate(
        leyes=leyes_corregidas,
        output_dir="./biblioteca_xml",
        nombre="Correccion de leyes"
    )
    print("Completado!")
