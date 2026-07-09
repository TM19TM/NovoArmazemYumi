# app.py
import flet as ft
import pandas as pd
import os
from drive_service import fazer_upload_foto 

EXCEL_FILE = "armazem_yumi_v2.xlsx"

def inicializar_excel():
    if not os.path.exists(EXCEL_FILE):
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            df_produtos = pd.DataFrame(columns=["ID", "Nome do Personagem", "Anime", "Status", "Preço", "Link Foto Drive"])
            df_produtos.to_excel(writer, sheet_name="Produtos", index=False)
            
            df_insumos = pd.DataFrame(columns=["ID", "Item", "Categoria", "Qtd Atual", "Qtd Mínima"])
            df_insumos.to_excel(writer, sheet_name="Insumos", index=False)

inicializar_excel()

def main(page: ft.Page):
    page.title = "YumiStudioArt - Armazém"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    COR_PRINCIPAL = "#FF85A2"  
    COR_SECUNDARIA = "#FFB7B2" 
    COR_FUNDO = "#FFF5F5"      
    COR_TEXTO = "#2B2D42"      
    
    page.bgcolor = COR_FUNDO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    txt_personagem = ft.TextField(label="Nome do Personagem / Peça", border_radius=15, border_color=COR_PRINCIPAL)
    txt_anime = ft.TextField(label="Anime / Franquia", border_radius=15, border_color=COR_PRINCIPAL)
    txt_preco = ft.TextField(label="Preço de Venda (R$)", border_radius=15, border_color=COR_PRINCIPAL, keyboard_type=ft.KeyboardType.NUMBER)
    
    # Variável temporária para simular a foto selecionada no celular
    caminho_foto_selecionada = "foto_temporaria.jpg" 

    def salvar_no_excel(e):
        if not txt_personagem.value or not txt_preco.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha os campos obrigatórios!"))
            page.snack_bar.open = True
            page.update()
            return
        
        df = pd.read_excel(EXCEL_FILE, sheet_name="Produtos")
        novo_id = f"PROD-{len(df) + 1:03d}"
        nome_arquivo_drive = f"{novo_id}_{txt_personagem.value}.jpg"
        
        # 1º PASSO: Envia a foto para o Drive antes de salvar no Excel
        link_da_foto = "Sem Foto"
        if os.path.exists(caminho_foto_selecionada):
            page.snack_bar = ft.SnackBar(ft.Text("Enviando foto para o Google Drive..."))
            page.snack_bar.open = True
            page.update()
            
            link_da_foto = fazer_upload_foto(caminho_foto_selecionada, nome_arquivo_drive)
        
        # 2º PASSO: Insere a linha no Excel incluindo o link retornado pelo Drive
        nova_linha = {
            "ID": novo_id,
            "Nome do Personagem": txt_personagem.value,
            "Anime": txt_anime.value,
            "Status": "Pronta Entrega",
            "Preço": float(txt_preco.value),
            "Link Foto Drive": link_da_foto if link_da_foto else "Erro no Upload"
        }
        
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name="Produtos", index=False)
            
        page.snack_bar = ft.SnackBar(ft.Text(f"✨ {txt_personagem.value} cadastrado com sucesso!"))
        page.snack_bar.open = True
        
        txt_personagem.value = ""
        txt_anime.value = ""
        txt_preco.value = ""
        page.update()

    btn_salvar = ft.ElevatedButton(
        text="Cadastrar Escultura 🎨",
        style=ft.ButtonStyle(
            color="white", 
            bgcolor=COR_PRINCIPAL, 
            shape=ft.RoundedRectangleBorder(radius=15), 
            padding=18
        ),
        on_click=salvar_no_excel
    )

    header = ft.Container(content=ft.Text("YumiStudioArt", size=28, weight=ft.FontWeight.BOLD, color=COR_TEXTO), margin=ft.margin.only(top=20, bottom=20))

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
            padding=20, bgcolor="white", border_radius=25, border=ft.border.all(2, COR_SECUNDARIA),
            shadow=ft.BoxShadow(blur_radius=10, color="#E0E0E0", offset=ft.Offset(0, 5))
        )
    )

ft.app(target=main)