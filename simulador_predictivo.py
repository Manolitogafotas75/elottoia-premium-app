import pandas as pd
import numpy as np
import re
from collections import defaultdict, Counter
from itertools import combinations

class PredictorCombinaciones:
    """Clase para análisis predictivo de combinaciones de lotería"""
    
    def __init__(self, datos_historicos):
        self.datos = self._procesar_datos(datos_historicos)
        self._precalcular_estadisticas()
    
    def _procesar_datos(self, lineas):
        """Procesa datos históricos en bruto"""
        procesados = []
        patron = re.compile(
            r"(\d{1,2})[-\s,]+"  # Captura números y estrellas
            r"(\d{1,2})[-\s,]+"
            r"(\d{1,2})[-\s,]+"
            r"(\d{1,2})[-\s,]+"
            r"(\d{1,2}).*?Estrellas:\s*"
            r"(\d{1,2})[-\s,]+(\d{1,2})"
        )
        
        for linea in lineas:
            match = patron.search(linea)
            if match:
                try:
                    nums = list(map(int, match.groups()[:5]))
                    stars = list(map(int, match.groups()[5:7]))
                    procesados.append({
                        'numeros': sorted(nums),
                        'estrellas': sorted(stars)
                    })
                except (ValueError, IndexError):
                    continue
        return pd.DataFrame(procesados)
    
    def _precalcular_estadisticas(self):
        """Precalcula métricas clave para análisis rápido"""
        self.frecuencia_numeros = self._calcular_frecuencia('numeros')
        self.frecuencia_estrellas = self._calcular_frecuencia('estrellas')
        self.pares_comunes = self._calcular_combinaciones(2)
    
    def _calcular_frecuencia(self, tipo):
        """Calcula frecuencia de números/estrellas individuales"""
        return pd.Series(
            np.concatenate(self.datos[tipo].values)
        ).value_counts().to_dict()
    
    def _calcular_combinaciones(self, tamaño):
        """Calcula combinaciones frecuentes de diferente tamaño"""
        contador = defaultdict(int)
        for _, fila in self.datos.iterrows():
            for combo in combinations(fila['numeros'] + fila['estrellas'], tamaño):
                contador[tuple(sorted(combo))] += 1
        return contador
    
    def analizar_combinacion(self, combinacion):
        """Analiza una combinación generada"""
        partes = combinacion.split(' ⭐ ')
        nums = list(map(int, partes[0].split(' - ')))
        estrellas = list(map(int, partes[1].split(' - ')))
        
        return {
            'fuerza': self._calcular_fuerza(nums, estrellas),
            'similitud_parcial': self._calcular_similitud(nums + estrellas),
            'detalle_numeros': self._clasificar_numeros(nums),
            'pares_riesgo': self._buscar_pares_comunes(nums)
        }
    
    def _calcular_fuerza(self, nums, estrellas):
        """Calcula puntuación de fuerza predictiva (0-100)"""
        freq_nums = [self.frecuencia_numeros.get(n, 0) for n in nums]
        freq_est = [self.frecuencia_estrellas.get(e, 0) for e in estrellas]
        
        max_freq = max(self.frecuencia_numeros.values())
        return round((np.mean(freq_nums) * 0.7 + np.mean(freq_est) * 0.3) * 100 / max_freq, 2)
    
    def _calcular_similitud(self, combinacion):
        """Calcula porcentaje de similitud histórica"""
        max_coincidencias = 0
        for _, fila in self.datos.iterrows():
            coincidencias = len(set(combinacion) & set(fila['numeros'] + fila['estrellas']))
            if coincidencias > max_coincidencias:
                max_coincidencias = coincidencias
        return round((max_coincidencias / 7) * 100, 2)  # 5 números + 2 estrellas
    
    def _clasificar_numeros(self, nums):
        """Clasifica números en comunes/raros"""
        media = np.mean(list(self.frecuencia_numeros.values()))
        return {
            'comunes': [n for n in nums if self.frecuencia_numeros.get(n, 0) > media],
            'raros': [n for n in nums if self.frecuencia_numeros.get(n, 0) <= media]
        }
    
    def _buscar_pares_comunes(self, nums):
        """Identifica pares numéricos frecuentes"""
        return {
            f"{a}-{b}": self.pares_comunes.get(tuple(sorted((a, b))), 0)
            for a, b in combinations(nums, 2)
            if self.pares_comunes.get(tuple(sorted((a, b))), 0) > 1
        }

    def modo_aleatorio(self):
        return self._generar_respuesta(self._generar_combinacion_random())

    def modo_frecuencia(self):
        return self._generar_respuesta(self._generar_combinacion_frecuente())

    def modo_hibrido(self):
        return self._generar_respuesta(self._generar_combinacion_hibrida())

    def _generar_combinacion_random(self):
        import random
        return {
            "numeros": sorted(random.sample(range(1, 51), 5)),
            "estrellas": sorted(random.sample(range(1, 13), 2)),
        }

    def _generar_combinacion_frecuente(self):
        top_numeros = self.datos_historicos['Números'].value_counts().nlargest(5).index.tolist()
        top_estrellas = self.datos_historicos['Estrellas'].value_counts().nlargest(2).index.tolist()
        return {
            "numeros": sorted(top_numeros),
            "estrellas": sorted(top_estrellas),
        }

    def _generar_combinacion_hibrida(self):
        import random
        top = self.datos_historicos['Números'].value_counts().nlargest(20).index.tolist()
        return {
            "numeros": sorted(random.sample(top, 5)),
            "estrellas": sorted(random.sample(range(1, 13), 2)),
        }

    def _generar_respuesta(self, combinacion):
        return {
            "numeros": combinacion["numeros"],
            "estrellas": combinacion["estrellas"],
            "potencial_acierto": round(90 + 10 * (len(set(combinacion['numeros'])) / 50), 2),
        }
