from fpdf import FPDF
import os

def create_generic_manual():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Content simulating a generic technical manual, in Portuguese
    content = """
    MANUAL TÉCNICO - PRODUTO X-1000

    1. INTRODUÇÃO
    O X-1000 é um dispositivo de alta performance projetado para operações críticas. Este manual cobre a instalação, configuração e resolução de problemas comuns.

    2. ESPECIFICAÇÕES TÉCNICAS
    - Processador: Quad-Core 3.5 GHz
    - Memória: 32GB DDR5
    - Armazenamento: 2TB NVMe SSD
    - Temperatura da operação: 0C a 75C

    3. RESOLUÇÃO DE PROBLEMAS (TROUBLESHOOTING)
    Erro 101: O sistema não liga.
    Solução: Verifique a conexão do cabo de força na porta traseira (Porta A). Certifique-se de que a voltagem está correta (110V/220V).

    Erro 202: Superaquecimento.
    Solução: Verifique se as saídas de ar estão obstruídas. O X-1000 possui sensores térmicos que desligam o aparelho automaticamente se atingir 85C.

    4. MANUTENÇÃO PREVENTIVA
    Limpe os filtros de poeira a cada 3 meses. Não utilize produtos abrasivos. Atualize o firmware apenas através do poortal oficial de suporte.
    """

    # Adding text (treating basic latin characters)
    pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))

    # Making sure the directory exists
    output_dir = "backend/data/manuals"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "manual_generico.pdf")
    pdf.output(output_path)
    print(f"Test PDF generated successfully at: {output_path}")

if __name__ == "__main__":
    create_generic_manual()
