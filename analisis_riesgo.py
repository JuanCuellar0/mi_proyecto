"""Módulo de análisis de riesgo de deserción - Refactorizado con POO"""
import csv
from database import Database, DatabaseConfig
from services import CaracterizacionRepository, RiskAnalysisRepository


class RiskAnalysisExporter:
    """Exportador de resultados de análisis de riesgo"""
    
    def __init__(self, risk_analysis_repo: RiskAnalysisRepository):
        self.risk_analysis_repo = risk_analysis_repo
    
    def export_to_csv(self, filename: str = 'reportes/riesgo_desercion.csv') -> None:
        """Exporta los resultados de análisis a un archivo CSV"""
        results = self.risk_analysis_repo.analyze_all()
        
        if not results:
            print("No hay registros para exportar")
            return
        
        # Obtener headers del primer resultado
        headers = results[0].keys()
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(results)
            print(f"Archivo exportado exitosamente: {filename}")
        except IOError as e:
            print(f"Error al escribir archivo: {e}")
    
    def print_summary(self) -> None:
        """Imprime un resumen de los resultados"""
        results = self.risk_analysis_repo.analyze_all()
        
        if not results:
            print("No hay datos para analizar")
            return
        
        # Contar por nivel de riesgo
        levels = {'Alto': 0, 'Medio': 0, 'Bajo': 0}
        for result in results:
            nivel = result.get('nivel', 'Desconocido')
            if nivel in levels:
                levels[nivel] += 1
        
        total = len(results)
        print("\n" + "="*50)
        print("RESUMEN DE ANÁLISIS DE RIESGO DE DESERCIÓN")
        print("="*50)
        print(f"Total de registros: {total}")
        print(f"Riesgo Alto: {levels['Alto']} ({levels['Alto']/total*100:.1f}%)")
        print(f"Riesgo Medio: {levels['Medio']} ({levels['Medio']/total*100:.1f}%)")
        print(f"Riesgo Bajo: {levels['Bajo']} ({levels['Bajo']/total*100:.1f}%)")
        print("="*50 + "\n")


def main():
    """Función principal para ejecutar el análisis"""
    # Inicializar BD
    db_config = DatabaseConfig(
        host="127.0.0.1",
        user="root",
        password="",
        database="mi_proyecto",
        charset="utf8mb4"
    )
    
    db = Database(db_config)
    caracterizacion_repo = CaracterizacionRepository(db)
    risk_analysis_repo = RiskAnalysisRepository(caracterizacion_repo)
    
    # Exportar resultados
    exporter = RiskAnalysisExporter(risk_analysis_repo)
    exporter.print_summary()
    exporter.export_to_csv()


if __name__ == '__main__':
    main()
            "score": score,
            "nivel": level,
            "razones": "; ".join(reasons),
        })

    os.makedirs("reportes", exist_ok=True)
    out_path = os.path.join("reportes", "riesgo_desercion.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id","fecha","nombre","estrato","acceso",
                "sisben_sn","grupo_sisben","vulnerabilidad_social","score","nivel","razones"
            ]
        )
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    altos = [r for r in results if r["nivel"] == "Alto"]
    print(f"Registros analizados: {len(results)}")
    print(f"Riesgo Alto: {len(altos)} — reporte: {out_path}")
    for r in sorted(altos, key=lambda x: x["score"], reverse=True)[:10]:
        print(f"- ID {r['id']} | {r.get('nombre') or 'Sin nombre'} | Score {r['score']} | {r['razones']}")

if __name__ == "__main__":
    main()