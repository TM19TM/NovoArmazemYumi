import flet as ft
import pandas as pd
import os

# Configuração inicial do arquivo Excel (Banco de Dados)
EXCEL_FILE = "armazem_yumi_v2.xlsx"

def inicializar_excel():
    if not os.path.exists(EXCEL_FILE):
        # Cria as abas iniciais se o arquivo não existir
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            df_produtos = pd.DataFrame(columns=["ID", "Nome do Personagem", "Anime", "Status", "Preço", "Link Foto Drive"])
            df_produtos.to_excel(writer, sheet_name="Produtos", index=False)
            
            df_insumos = pd.DataFrame(columns=["ID", "Item", "Categoria", "Qtd Atual", "Qtd Mínima"])
            df_insumos.to_excel(writer, sheet_name="Insumos", index=False)

# Inicializa o banco de dados local em Excel
inicializar_excel()

def main(page: ft.Page):
    page.title = "YumiStudioArt - Armazém"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Customização da Paleta de Cores (Baseada na identidade visual lúdica/artesanal)
    # Substitua as hexadecimais abaixo pelas cores exatas da sua logo!
    COR_PRINCIPAL = "#FF85A2"  # Um rosa/pastel vibrante estilo cartoon
    COR_SECUNDARIA = "#FFB7B2" # Tom pastel complementar
    COR_FUNDO = "#FFF5F5"      # Fundo suave
    COR_TEXTO = "#2B2D42"      # Texto escuro para boa leitura
    
    page.bgcolor = COR_FUNDO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # Campos de Entrada (Estilo Cartoon: Bordas bem arredondadas e cores vivas)
    txt_personagem = ft.TextField(
        label="Nome do Personagem / Peça", 
        border_radius=15, 
        border_color=COR_PRINCIPAL,
        label_style=ft.TextStyle(color=COR_TEXTO, weight=ft.FontWeight.BOLD)
    )
    txt_anime = ft.TextField(
        label="Anime / Franquia", 
        border_radius=15, 
        border_color=COR_PRINCIPAL
    )
    txt_preco = ft.TextField(
        label="Preço de Venda (R$)", 
        border_radius=15, 
        border_color=COR_PRINCIPAL,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    # Função para salvar os dados capturados na interface direto no Excel
    def salvar_no_excel(e):
        if not txt_personagem.value or not txt_preco.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha os campos obrigatórios!"))
            page.snack_bar.open = True
            page.update()
            return
        
        # Carrega o Excel existente
        df = pd.read_excel(EXCEL_FILE, sheet_name="Produtos")
        
        # Cria a nova linha
        novo_id = f"PROD-{len(df) + 1:03d}"
        nova_linha = {
            "ID": novo_id,
            "Nome do Personagem": txt_personagem.value,
            "Anime": txt_anime.value,
            "Status": "Pronta Entrega",
            "Preço": float(txt_preco.value),
            "Link Foto Drive": "Pendente Integração API" # Próximo passo
        }
        
        # Adiciona e salva de volta na aba correspondente
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name="Produtos", index=False)
            
        # Feedback visual estilo pop-up rápido
        page.snack_bar = ft.SnackBar(ft.Text(f" {txt_personagem.value} salvo com sucesso no Excel!"))
        page.snack_bar.open = True
        
        # Limpa os campos
        txt_personagem.value = ""
        txt_anime.value = ""
        txt_preco.value = ""
        page.update()

    # Botão com visual marcante "Cartoon" (Gordinho e arredondado)
    btn_salvar = ft.ElevatedButton(
        text="Cadastrar Escultura ",
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=COR_PRINCIPAL,
            shape=ft.RoundedRectangleBorder(radius=15),
            padding=18
        ),
        on_click=salvar_no_excel
    )

    # Top Bar / Logo Area
    header = ft.Container(
        content=ft.Text("YumiStudioArt", size=28, weight=ft.FontWeight.BOLD, color=COR_TEXTO),
        margin=ft.margin.only(top=20, bottom=20)
    )

    # Adicionando os componentes na tela simétrica para Celular
    page.add(
        header,
        ft.Container(
            content=ft.Column([
                ft.Text("Novo Item no Estoque", size=18, weight=ft.FontWeight.BOLD, color=COR_TEXTO),
                txt_personagem,
                txt_anime,
                txt_preco,
                ft.Row([btn_salvar], alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=20),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=25,
            border=ft.border.all(2, COR_SECUNDARIA),
            shadow=ft.BoxShadow(blur_radius=10, color="#E0E0E0", offset=ft.Offset(0, 5))
        )
    )

ft.app(target=main)