#!/usr/bin/env python3
"""
Script para generar una biblioteca de leyes en formato XML.

Este script genera archivos XML estructurados optimizados para
agentes de IA a partir de leyes chilenas.

Uso:
    python scripts/generar_biblioteca_xml.py
    python scripts/generar_biblioteca_xml.py --output ./mi_biblioteca
    python scripts/generar_biblioteca_xml.py --leyes comercial
    python scripts/generar_biblioteca_xml.py --leyes completa  # Todas las leyes

Author: Luis Aguilera Arteaga <luis@aguilera.cl>
"""

import argparse
import logging
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from leychile_epub.xml_generator import BibliotecaXMLGenerator, LawXMLGenerator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ============================================================================
# CATÁLOGO COMPLETO DE LEYES CHILENAS
# ============================================================================

# --- CÓDIGOS FUNDAMENTALES ---
CODIGOS = {
    "constitucion": {
        "url": "https://www.leychile.cl/Navegar?idNorma=242302",
        "nombre": "Constitución Política de la República",
        "descripcion": "Carta fundamental que establece las bases del Estado, derechos fundamentales y organización del poder.",
    },
    "codigo_civil": {
        "url": "https://www.leychile.cl/Navegar?idNorma=172986",
        "nombre": "Código Civil",
        "descripcion": "Normas fundamentales de derecho privado, obligaciones, contratos, familia, sucesiones y bienes.",
    },
    "codigo_penal": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1984",
        "nombre": "Código Penal",
        "descripcion": "Tipifica los delitos y establece las penas correspondientes.",
    },
    "codigo_trabajo": {
        "url": "https://www.leychile.cl/Navegar?idNorma=207436",
        "nombre": "Código del Trabajo",
        "descripcion": "Regula las relaciones laborales entre empleadores y trabajadores.",
    },
    "codigo_comercio": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1974",
        "nombre": "Código de Comercio",
        "descripcion": "Regula los actos de comercio, comerciantes, sociedades mercantiles y comercio marítimo.",
    },
    "codigo_tributario": {
        "url": "https://www.leychile.cl/Navegar?idNorma=6374",
        "nombre": "Código Tributario",
        "descripcion": "Normas generales sobre tributación, procedimientos y sanciones fiscales.",
    },
    "codigo_proc_civil": {
        "url": "https://www.leychile.cl/Navegar?idNorma=22740",
        "nombre": "Código de Procedimiento Civil",
        "descripcion": "Regula los procedimientos judiciales en materia civil.",
    },
    "codigo_proc_penal": {
        "url": "https://www.leychile.cl/Navegar?idNorma=176595",
        "nombre": "Código Procesal Penal",
        "descripcion": "Establece el sistema procesal penal acusatorio.",
    },
    "codigo_organico_tribunales": {
        "url": "https://www.leychile.cl/Navegar?idNorma=25563",
        "nombre": "Código Orgánico de Tribunales",
        "descripcion": "Organización y atribuciones de los tribunales de justicia.",
    },
    "codigo_aguas": {
        "url": "https://www.leychile.cl/Navegar?idNorma=5605",
        "nombre": "Código de Aguas",
        "descripcion": "Regula el dominio, uso y aprovechamiento de las aguas.",
    },
    "codigo_mineria": {
        "url": "https://www.leychile.cl/Navegar?idNorma=29668",
        "nombre": "Código de Minería",
        "descripcion": "Regula la exploración, explotación y beneficio de minerales.",
    },
    "codigo_sanitario": {
        "url": "https://www.leychile.cl/Navegar?idNorma=5595",
        "nombre": "Código Sanitario",
        "descripcion": "Normas sobre salud pública, higiene y seguridad sanitaria.",
    },
    "codigo_aeronautico": {
        "url": "https://www.leychile.cl/Navegar?idNorma=6848",
        "nombre": "Código Aeronáutico",
        "descripcion": "Regula la actividad aeronáutica civil.",
    },
}

# --- DERECHO CIVIL Y FAMILIA ---
CIVIL_FAMILIA = {
    "ley_19947_matrimonio_civil": {
        "url": "https://www.leychile.cl/Navegar?idNorma=225128",
        "nombre": "Ley 19.947 - Matrimonio Civil",
        "descripcion": "Establece nueva ley de matrimonio civil, incluyendo divorcio.",
    },
    "ley_14908_pension_alimentos": {
        "url": "https://www.leychile.cl/Navegar?idNorma=172986",
        "nombre": "Ley 14.908 - Abandono de Familia y Pensiones",
        "descripcion": "Abandono de familia y pago de pensiones alimenticias.",
    },
    "ley_20066_violencia_intrafamiliar": {
        "url": "https://www.leychile.cl/Navegar?idNorma=242648",
        "nombre": "Ley 20.066 - Violencia Intrafamiliar",
        "descripcion": "Establece ley de violencia intrafamiliar.",
    },
    "ley_19620_adopcion": {
        "url": "https://www.leychile.cl/Navegar?idNorma=138817",
        "nombre": "Ley 19.620 - Adopción de Menores",
        "descripcion": "Dicta normas sobre adopción de menores.",
    },
    "ley_21400_matrimonio_igualitario": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1169553",
        "nombre": "Ley 21.400 - Matrimonio Igualitario",
        "descripcion": "Modifica diversos cuerpos legales para regular en igualdad de condiciones el matrimonio.",
    },
    "ley_19968_tribunales_familia": {
        "url": "https://www.leychile.cl/Navegar?idNorma=229557",
        "nombre": "Ley 19.968 - Tribunales de Familia",
        "descripcion": "Crea los tribunales de familia.",
    },
    "ley_20830_acuerdo_union_civil": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1075210",
        "nombre": "Ley 20.830 - Acuerdo de Unión Civil",
        "descripcion": "Crea el acuerdo de unión civil.",
    },
}

# --- DERECHO COMERCIAL Y EMPRESARIAL ---
COMERCIAL = {
    "ley_19496_consumidor": {
        "url": "https://www.leychile.cl/Navegar?idNorma=61438",
        "nombre": "Ley 19.496 - Protección del Consumidor",
        "descripcion": "Derechos del consumidor, publicidad, contratos de adhesión, garantías.",
    },
    "ley_20720_insolvencia": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1058072",
        "nombre": "Ley 20.720 - Reorganización y Liquidación",
        "descripcion": "Procedimientos concursales, quiebras, reorganización empresarial.",
    },
    "ley_18046_sociedades_anonimas": {
        "url": "https://www.leychile.cl/Navegar?idNorma=29473",
        "nombre": "Ley 18.046 - Sociedades Anónimas",
        "descripcion": "Regula la constitución y funcionamiento de sociedades anónimas.",
    },
    "ley_3918_sociedades_responsabilidad_limitada": {
        "url": "https://www.leychile.cl/Navegar?idNorma=24483",
        "nombre": "Ley 3.918 - Sociedades de Responsabilidad Limitada",
        "descripcion": "Regula las sociedades de responsabilidad limitada.",
    },
    "ley_20659_empresas_un_dia": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1048718",
        "nombre": "Ley 20.659 - Empresas en un Día",
        "descripcion": "Simplifica régimen de constitución, modificación y disolución de sociedades.",
    },
    "dfl_251_seguros_bolsas": {
        "url": "https://www.leychile.cl/Navegar?idNorma=5201",
        "nombre": "DFL 251 - Compañías de Seguros y Bolsas de Comercio",
        "descripcion": "Regula compañías de seguros, sociedades anónimas y bolsas de comercio.",
    },
    "ley_18045_mercado_valores": {
        "url": "https://www.leychile.cl/Navegar?idNorma=29472",
        "nombre": "Ley 18.045 - Mercado de Valores",
        "descripcion": "Regula la oferta pública de valores y sus mercados.",
    },
    "ley_20393_responsabilidad_penal_personas_juridicas": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1008668",
        "nombre": "Ley 20.393 - Responsabilidad Penal Personas Jurídicas",
        "descripcion": "Establece responsabilidad penal de las personas jurídicas.",
    },
    "ley_20169_competencia_desleal": {
        "url": "https://www.leychile.cl/Navegar?idNorma=258377",
        "nombre": "Ley 20.169 - Competencia Desleal",
        "descripcion": "Regula la competencia desleal.",
    },
    "dl_211_libre_competencia": {
        "url": "https://www.leychile.cl/Navegar?idNorma=5872",
        "nombre": "DL 211 - Libre Competencia",
        "descripcion": "Fija normas para la defensa de la libre competencia.",
    },
}

# --- DERECHO LABORAL Y PREVISIONAL ---
LABORAL = {
    "ley_16744_accidentes_trabajo": {
        "url": "https://www.leychile.cl/Navegar?idNorma=28650",
        "nombre": "Ley 16.744 - Accidentes del Trabajo",
        "descripcion": "Establece normas sobre accidentes del trabajo y enfermedades profesionales.",
    },
    "ley_21643_acoso_laboral": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1200096",
        "nombre": "Ley 21.643 - Ley Karin (Acoso Laboral)",
        "descripcion": "Modifica el Código del Trabajo en materia de prevención, investigación y sanción del acoso laboral, sexual o de violencia en el trabajo.",
    },
    "dl_3500_pensiones": {
        "url": "https://www.leychile.cl/Navegar?idNorma=7147",
        "nombre": "DL 3.500 - Sistema de Pensiones AFP",
        "descripcion": "Establece nuevo sistema de pensiones basado en capitalización individual.",
    },
    "ley_21327_modernizacion_dt": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1158029",
        "nombre": "Ley 21.327 - Modernización Dirección del Trabajo",
        "descripcion": "Moderniza la Dirección del Trabajo.",
    },
    "ley_19728_seguro_desempleo": {
        "url": "https://www.leychile.cl/Navegar?idNorma=185814",
        "nombre": "Ley 19.728 - Seguro de Desempleo",
        "descripcion": "Establece un seguro de desempleo.",
    },
    "ley_20545_postnatal_parental": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1030936",
        "nombre": "Ley 20.545 - Postnatal Parental",
        "descripcion": "Modifica las normas sobre protección a la maternidad e incorpora permiso postnatal parental.",
    },
}

# --- DERECHO ADMINISTRATIVO Y FUNCIONARIOS ---
ADMINISTRATIVO = {
    "ley_18834_estatuto_administrativo": {
        "url": "https://www.leychile.cl/Navegar?idNorma=30256",
        "nombre": "Ley 18.834 - Estatuto Administrativo",
        "descripcion": "Aprueba estatuto administrativo de funcionarios públicos.",
    },
    "ley_19880_procedimiento_administrativo": {
        "url": "https://www.leychile.cl/Navegar?idNorma=210676",
        "nombre": "Ley 19.880 - Procedimiento Administrativo",
        "descripcion": "Establece bases de los procedimientos administrativos.",
    },
    "ley_18695_municipalidades": {
        "url": "https://www.leychile.cl/Navegar?idNorma=251693",
        "nombre": "Ley 18.695 - Orgánica de Municipalidades",
        "descripcion": "Ley orgánica constitucional de municipalidades.",
    },
    "ley_20285_acceso_informacion": {
        "url": "https://www.leychile.cl/Navegar?idNorma=276363",
        "nombre": "Ley 20.285 - Transparencia y Acceso a la Información",
        "descripcion": "Sobre acceso a la información pública.",
    },
    "ley_18575_bases_administracion": {
        "url": "https://www.leychile.cl/Navegar?idNorma=191865",
        "nombre": "Ley 18.575 - Bases Generales Administración del Estado",
        "descripcion": "Ley orgánica constitucional de bases generales de la administración del Estado.",
    },
    "ley_19886_compras_publicas": {
        "url": "https://www.leychile.cl/Navegar?idNorma=213004",
        "nombre": "Ley 19.886 - Compras Públicas",
        "descripcion": "Ley de bases sobre contratos administrativos de suministro y prestación de servicios.",
    },
    "ley_20730_lobby": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1060115",
        "nombre": "Ley 20.730 - Ley del Lobby",
        "descripcion": "Regula el lobby y las gestiones que representen intereses particulares ante las autoridades.",
    },
}

# --- DERECHO PENAL Y PROCESAL PENAL ---
PENAL = {
    "ley_20000_drogas": {
        "url": "https://www.leychile.cl/Navegar?idNorma=235507",
        "nombre": "Ley 20.000 - Ley de Drogas",
        "descripcion": "Sustituye la ley N° 19.366, que sanciona el tráfico ilícito de estupefacientes.",
    },
    "ley_20084_responsabilidad_penal_adolescentes": {
        "url": "https://www.leychile.cl/Navegar?idNorma=244803",
        "nombre": "Ley 20.084 - Responsabilidad Penal Adolescentes",
        "descripcion": "Establece un sistema de responsabilidad de los adolescentes por infracciones a la ley penal.",
    },
    "ley_18216_medidas_alternativas": {
        "url": "https://www.leychile.cl/Navegar?idNorma=29636",
        "nombre": "Ley 18.216 - Penas Sustitutivas",
        "descripcion": "Establece penas que indica como sustitutivas a las penas privativas o restrictivas de libertad.",
    },
    "ley_19696_codigo_procesal_penal": {
        "url": "https://www.leychile.cl/Navegar?idNorma=176595",
        "nombre": "Ley 19.696 - Código Procesal Penal",
        "descripcion": "Establece Código Procesal Penal.",
    },
    "ley_21057_entrevistas_videograbadas": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1113932",
        "nombre": "Ley 21.057 - Entrevistas Videograbadas",
        "descripcion": "Regula entrevistas grabadas en video y otras medidas de resguardo a menores de edad víctimas de delitos sexuales.",
    },
}

# --- DERECHO TRIBUTARIO ---
TRIBUTARIO = {
    "ley_impuesto_renta": {
        "url": "https://www.leychile.cl/Navegar?idNorma=6368",
        "nombre": "Ley sobre Impuesto a la Renta",
        "descripcion": "Aprueba texto refundido de la ley sobre impuesto a la renta.",
    },
    "dl_825_iva": {
        "url": "https://www.leychile.cl/Navegar?idNorma=6370",
        "nombre": "DL 825 - Ley del IVA",
        "descripcion": "Ley sobre impuesto a las ventas y servicios (IVA).",
    },
    "ley_17235_impuesto_territorial": {
        "url": "https://www.leychile.cl/Navegar?idNorma=28872",
        "nombre": "Ley 17.235 - Impuesto Territorial",
        "descripcion": "Sobre impuesto territorial (contribuciones).",
    },
}

# --- PROPIEDAD INTELECTUAL ---
PROPIEDAD_INTELECTUAL = {
    "ley_17336_propiedad_intelectual": {
        "url": "https://www.leychile.cl/Navegar?idNorma=28933",
        "nombre": "Ley 17.336 - Propiedad Intelectual",
        "descripcion": "Sobre propiedad intelectual (derechos de autor).",
    },
    "ley_19039_propiedad_industrial": {
        "url": "https://www.leychile.cl/Navegar?idNorma=30406",
        "nombre": "Ley 19.039 - Propiedad Industrial",
        "descripcion": "Establece normas aplicables a los privilegios industriales y protección de los derechos de propiedad industrial.",
    },
}

# --- MEDIO AMBIENTE ---
MEDIO_AMBIENTE = {
    "ley_19300_bases_medio_ambiente": {
        "url": "https://www.leychile.cl/Navegar?idNorma=30667",
        "nombre": "Ley 19.300 - Bases Generales del Medio Ambiente",
        "descripcion": "Aprueba ley sobre bases generales del medio ambiente.",
    },
    "ley_20417_institucionalidad_ambiental": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1010459",
        "nombre": "Ley 20.417 - Ministerio del Medio Ambiente",
        "descripcion": "Crea el Ministerio, el Servicio de Evaluación Ambiental y la Superintendencia del Medio Ambiente.",
    },
}

# --- DATOS PERSONALES Y TECNOLOGÍA ---
DATOS_TECNOLOGIA = {
    "ley_19628_proteccion_datos": {
        "url": "https://www.leychile.cl/Navegar?idNorma=141599",
        "nombre": "Ley 19.628 - Protección de Datos Personales",
        "descripcion": "Sobre protección de la vida privada (datos personales).",
    },
    "ley_21459_delitos_informaticos": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1177975",
        "nombre": "Ley 21.459 - Delitos Informáticos",
        "descripcion": "Establece normas sobre delitos informáticos, deroga la ley N° 19.223.",
    },
    "ley_19799_firma_electronica": {
        "url": "https://www.leychile.cl/Navegar?idNorma=196640",
        "nombre": "Ley 19.799 - Firma Electrónica",
        "descripcion": "Sobre documentos electrónicos, firma electrónica y servicios de certificación.",
    },
    "ley_21180_transformacion_digital": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1138479",
        "nombre": "Ley 21.180 - Transformación Digital del Estado",
        "descripcion": "Sobre transformación digital del Estado.",
    },
}

# --- URBANISMO E INMOBILIARIO ---
URBANISMO = {
    "dfl_458_urbanismo": {
        "url": "https://www.leychile.cl/Navegar?idNorma=13560",
        "nombre": "DFL 458 - Ley General de Urbanismo y Construcciones",
        "descripcion": "Aprueba nueva ley general de urbanismo y construcciones.",
    },
    "ley_19537_copropiedad_inmobiliaria": {
        "url": "https://www.leychile.cl/Navegar?idNorma=81505",
        "nombre": "Ley 19.537 - Copropiedad Inmobiliaria",
        "descripcion": "Sobre copropiedad inmobiliaria.",
    },
    "dl_2695_regularizacion_propiedad": {
        "url": "https://www.leychile.cl/Navegar?idNorma=6982",
        "nombre": "DL 2.695 - Regularización de la Pequeña Propiedad Raíz",
        "descripcion": "Fija normas para regularizar la posesión de la pequeña propiedad raíz.",
    },
    "ley_19865_financiamiento_urbano": {
        "url": "https://www.leychile.cl/Navegar?idNorma=210992",
        "nombre": "Ley 19.865 - Financiamiento Urbano Compartido",
        "descripcion": "Sobre financiamiento urbano compartido.",
    },
}

# --- SALUD ---
SALUD = {
    "ley_20584_derechos_pacientes": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1039348",
        "nombre": "Ley 20.584 - Derechos de los Pacientes",
        "descripcion": "Regula los derechos y deberes que tienen las personas en relación con acciones vinculadas a su atención en salud.",
    },
    "ley_20850_ricarte_soto": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1078148",
        "nombre": "Ley 20.850 - Ley Ricarte Soto",
        "descripcion": "Crea un sistema de protección financiera para diagnósticos y tratamientos de alto costo.",
    },
    "ley_18933_isapres": {
        "url": "https://www.leychile.cl/Navegar?idNorma=30222",
        "nombre": "Ley 18.933 - Isapres",
        "descripcion": "Crea la Superintendencia de Instituciones de Salud Previsional.",
    },
}

# --- EDUCACIÓN ---
EDUCACION = {
    "ley_20370_general_educacion": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1006043",
        "nombre": "Ley 20.370 - Ley General de Educación",
        "descripcion": "Establece la ley general de educación.",
    },
    "ley_21091_educacion_superior": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1118991",
        "nombre": "Ley 21.091 - Educación Superior",
        "descripcion": "Sobre educación superior.",
    },
}

# --- OTRAS LEYES RELEVANTES ---
OTRAS = {
    "ley_18290_transito": {
        "url": "https://www.leychile.cl/Navegar?idNorma=29708",
        "nombre": "Ley 18.290 - Ley de Tránsito",
        "descripcion": "Ley de tránsito.",
    },
    "ley_20609_antidiscriminacion": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1042092",
        "nombre": "Ley 20.609 - Ley Zamudio (Antidiscriminación)",
        "descripcion": "Establece medidas contra la discriminación.",
    },
    "ley_21545_tea": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1177268",
        "nombre": "Ley 21.545 - Ley TEA",
        "descripcion": "Establece la promoción de la inclusión, la atención integral y la protección de los derechos de las personas con trastorno del espectro autista.",
    },
}

# --- COBRANZA Y TÍTULOS EJECUTIVOS ---
COBRANZA_TITULOS = {
    "ley_18092_letra_pagare": {
        "url": "https://www.leychile.cl/Navegar?idNorma=29517",
        "nombre": "Ley 18.092 - Letra de Cambio y Pagaré",
        "descripcion": "Dicta nuevas normas sobre letra de cambio y pagaré y deroga disposiciones del Código de Comercio.",
    },
    "ley_19983_factura_ejecutiva": {
        "url": "https://www.leychile.cl/Navegar?idNorma=233421",
        "nombre": "Ley 19.983 - Mérito Ejecutivo de la Factura",
        "descripcion": "Regula la transferencia y otorga mérito ejecutivo a copia de la factura.",
    },
    "ley_20727_factura_electronica": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1058909",
        "nombre": "Ley 20.727 - Factura Electrónica",
        "descripcion": "Introduce modificaciones a la legislación tributaria en materia de factura electrónica.",
    },
    "dfl_707_cheques": {
        "url": "https://www.leychile.cl/Navegar?idNorma=5594",
        "nombre": "DFL 707 - Cuentas Corrientes y Cheques",
        "descripcion": "Fija texto refundido de la ley sobre cuentas corrientes bancarias y cheques.",
    },
    "ley_18010_credito_dinero": {
        "url": "https://www.leychile.cl/Navegar?idNorma=29438",
        "nombre": "Ley 18.010 - Operaciones de Crédito de Dinero",
        "descripcion": "Establece normas para las operaciones de crédito y otras obligaciones de dinero (intereses, reajustes).",
    },
    "ley_17322_cobranza_previsional": {
        "url": "https://www.leychile.cl/Navegar?idNorma=28919",
        "nombre": "Ley 17.322 - Cobranza Judicial de Cotizaciones",
        "descripcion": "Normas para la cobranza judicial de cotizaciones, aportes y multas de las instituciones de seguridad social.",
    },
}

# --- PROCEDIMIENTOS ESPECIALES ---
PROCEDIMIENTOS = {
    "ley_19971_arbitraje_internacional": {
        "url": "https://www.leychile.cl/Navegar?idNorma=230697",
        "nombre": "Ley 19.971 - Arbitraje Comercial Internacional",
        "descripcion": "Sobre arbitraje comercial internacional.",
    },
    "ley_18287_policia_local": {
        "url": "https://www.leychile.cl/Navegar?idNorma=29705",
        "nombre": "Ley 18.287 - Procedimiento Juzgados de Policía Local",
        "descripcion": "Establece procedimiento ante los Juzgados de Policía Local.",
    },
}

# --- TIMBRES Y ESTAMPILLAS ---
TIMBRES = {
    "dl_3475_timbres": {
        "url": "https://www.leychile.cl/Navegar?idNorma=7137",
        "nombre": "DL 3.475 - Ley de Timbres y Estampillas",
        "descripcion": "Modifica la ley de timbres y estampillas (impuesto de timbres).",
    },
}

# --- CONSERVADORES Y REGISTROS ---
REGISTROS = {
    "reglamento_cbr": {
        "url": "https://www.leychile.cl/Navegar?idNorma=255400",
        "nombre": "Reglamento del Conservador de Bienes Raíces",
        "descripcion": "Reglamento del Registro Conservatorio de Bienes Raíces (1857).",
    },
}

# --- SOCIETARIO ADICIONAL ---
SOCIETARIO = {
    "ley_19857_eirl": {
        "url": "https://www.leychile.cl/Navegar?idNorma=207588",
        "nombre": "Ley 19.857 - EIRL",
        "descripcion": "Autoriza el establecimiento de empresas individuales de responsabilidad limitada.",
    },
    "ley_20382_gobiernos_corporativos": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1007297",
        "nombre": "Ley 20.382 - Gobiernos Corporativos",
        "descripcion": "Introduce perfeccionamientos a la normativa que regula los gobiernos corporativos de las empresas.",
    },
}

# --- GARANTÍAS Y PRENDAS ---
GARANTIAS = {
    "ley_20190_prenda_sin_desplazamiento": {
        "url": "https://www.leychile.cl/Navegar?idNorma=261427",
        "nombre": "Ley 20.190 - Prenda sin Desplazamiento (MK2)",
        "descripcion": "Introduce adecuaciones para el fomento de la industria de capital de riesgo y modernización del mercado de capitales. Incluye la Ley de Prenda sin Desplazamiento.",
    },
    "ley_4287_prenda_valores": {
        "url": "https://www.leychile.cl/Navegar?idNorma=24631",
        "nombre": "Ley 4.287 - Prenda de Valores Mobiliarios",
        "descripcion": "Ley sobre prenda de valores mobiliarios a favor de los bancos.",
    },
}

# --- ELECTORAL ---
ELECTORAL = {
    "dfl_2_votaciones": {
        "url": "https://www.leychile.cl/Navegar?idNorma=1108229",
        "nombre": "DFL 2 - Ley de Votaciones Populares (Ley 18.700)",
        "descripcion": "Fija el texto refundido de la Ley N° 18.700, orgánica constitucional sobre votaciones populares y escrutinios.",
    },
}


# ============================================================================
# DEFINICIONES DE BIBLIOTECAS
# ============================================================================

def _merge_dicts(*dicts) -> dict:
    """Combina múltiples diccionarios."""
    result = {}
    for d in dicts:
        result.update(d)
    return result


BIBLIOTECAS = {
    "basica": {
        "nombre": "Biblioteca Legal Básica",
        "descripcion": "Leyes fundamentales del derecho chileno",
        "leyes": {
            "codigo_civil": CODIGOS["codigo_civil"],
            "codigo_comercio": CODIGOS["codigo_comercio"],
            "ley_19496_consumidor": COMERCIAL["ley_19496_consumidor"],
            "ley_20720_insolvencia": COMERCIAL["ley_20720_insolvencia"],
        },
    },
    "comercial": {
        "nombre": "Biblioteca de Derecho Comercial",
        "descripcion": "Leyes relacionadas con el comercio y los negocios",
        "leyes": _merge_dicts(
            {"codigo_comercio": CODIGOS["codigo_comercio"]},
            COMERCIAL,
        ),
    },
    "civil": {
        "nombre": "Biblioteca de Derecho Civil",
        "descripcion": "Código Civil y leyes relacionadas",
        "leyes": _merge_dicts(
            {"codigo_civil": CODIGOS["codigo_civil"]},
            CIVIL_FAMILIA,
        ),
    },
    "laboral": {
        "nombre": "Biblioteca de Derecho Laboral",
        "descripcion": "Código del Trabajo y leyes laborales",
        "leyes": _merge_dicts(
            {"codigo_trabajo": CODIGOS["codigo_trabajo"]},
            LABORAL,
        ),
    },
    "penal": {
        "nombre": "Biblioteca de Derecho Penal",
        "descripcion": "Código Penal y leyes penales relacionadas",
        "leyes": _merge_dicts(
            {"codigo_penal": CODIGOS["codigo_penal"]},
            PENAL,
        ),
    },
    "tributario": {
        "nombre": "Biblioteca de Derecho Tributario",
        "descripcion": "Código Tributario y leyes impositivas",
        "leyes": _merge_dicts(
            {"codigo_tributario": CODIGOS["codigo_tributario"]},
            TRIBUTARIO,
        ),
    },
    "administrativo": {
        "nombre": "Biblioteca de Derecho Administrativo",
        "descripcion": "Leyes de administración del Estado",
        "leyes": ADMINISTRATIVO,
    },
    "codigos": {
        "nombre": "Códigos de la República",
        "descripcion": "Todos los códigos fundamentales de Chile",
        "leyes": CODIGOS,
    },
    "completa": {
        "nombre": "Biblioteca Legal Completa de Chile",
        "descripcion": "Colección completa de leyes chilenas más relevantes",
        "leyes": _merge_dicts(
            CODIGOS,
            CIVIL_FAMILIA,
            COMERCIAL,
            LABORAL,
            ADMINISTRATIVO,
            PENAL,
            TRIBUTARIO,
            PROPIEDAD_INTELECTUAL,
            MEDIO_AMBIENTE,
            DATOS_TECNOLOGIA,
            URBANISMO,
            SALUD,
            EDUCACION,
            OTRAS,
            COBRANZA_TITULOS,
            PROCEDIMIENTOS,
            TIMBRES,
            REGISTROS,
            SOCIETARIO,
            GARANTIAS,
            ELECTORAL,
        ),
    },
    "cobranza": {
        "nombre": "Biblioteca de Cobranza Judicial",
        "descripcion": "Leyes para cobranza de facturas, pagarés, cheques y títulos ejecutivos",
        "leyes": _merge_dicts(
            {"codigo_comercio": CODIGOS["codigo_comercio"]},
            {"codigo_proc_civil": CODIGOS["codigo_proc_civil"]},
            COBRANZA_TITULOS,
            PROCEDIMIENTOS,
            TIMBRES,
            GARANTIAS,
        ),
    },
}


def parse_args() -> argparse.Namespace:
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="generar_biblioteca_xml",
        description="🇨🇱 Genera una biblioteca de leyes chilenas en formato XML para agentes de IA",
        epilog="Ejemplo: python generar_biblioteca_xml.py --leyes basica -o ./biblioteca",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="./biblioteca_xml",
        help="Directorio de salida (default: ./biblioteca_xml)",
    )

    parser.add_argument(
        "-l",
        "--leyes",
        choices=list(BIBLIOTECAS.keys()),
        default="basica",
        help="Conjunto de leyes a generar (default: basica)",
    )

    parser.add_argument(
        "--url",
        help="URL específica de una ley para generar individualmente",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Modo verbose",
    )

    return parser.parse_args()


def generar_ley_individual(url: str, output_dir: str) -> None:
    """Genera XML para una ley individual."""
    generator = LawXMLGenerator()

    logger.info(f"Generando XML desde: {url}")
    xml_path = generator.generate_from_url(url, output_dir)
    logger.info(f"✅ Generado: {xml_path}")


def generar_biblioteca(biblioteca_key: str, output_dir: str) -> None:
    """Genera una biblioteca completa de leyes."""
    biblioteca_config = BIBLIOTECAS[biblioteca_key]

    print("\n" + "=" * 60)
    print(f"📚 {biblioteca_config['nombre']}")
    print(f"   {biblioteca_config['descripcion']}")
    print("=" * 60)

    generator = BibliotecaXMLGenerator()

    resultado = generator.generate(
        leyes=biblioteca_config["leyes"],
        output_dir=output_dir,
        nombre=biblioteca_config["nombre"],
    )

    # Mostrar resumen
    print("\n" + "-" * 60)
    print("📊 RESUMEN")
    print("-" * 60)
    print(f"   Directorio: {resultado['directorio']}")
    print(f"   Leyes procesadas: {len(resultado['leyes'])}")
    print(f"   ✅ Exitosas: {resultado['exitosas']}")
    print(f"   ❌ Fallidas: {resultado['fallidas']}")

    if resultado.get("indice"):
        print(f"   📑 Índice: {resultado['indice']}")

    print("\n📁 Archivos generados:")
    for ley in resultado["leyes"]:
        if ley["estado"] == "exitoso":
            print(f"   ✓ {ley['archivo']} - {ley['nombre']}")
        else:
            print(f"   ✗ {ley['nombre']} - Error: {ley.get('error', 'Desconocido')}")

    print("=" * 60 + "\n")


def main() -> int:
    """Función principal."""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print("\n🇨🇱 LeyChile XML Generator")
    print("   Generador de XML para agentes de IA\n")

    try:
        if args.url:
            # Generar ley individual
            generar_ley_individual(args.url, args.output)
        else:
            # Generar biblioteca
            generar_biblioteca(args.leyes, args.output)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️ Operación cancelada por el usuario")
        return 130

    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
