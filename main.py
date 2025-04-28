from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, DictProperty
from datetime import datetime, timedelta
import pandas as pd
import os

# Estrutura das atividades
# Estrutura das atividades
atividades = {
    "1": "PROJETO BÁSICO",
    "2": {
        "title": "ASSINATURA DE CONTRATOS",
        "children": {
            "2.1": "Contrato de Compartilhamento de Instalação CCI",
            "2.2": "Contrato de Conexão de Transmissão CCT",
        },
    },
    "3": "FUNDIÁRIO",
    "4": "LICENCIAMENTO AMBIENTAL",
    "5": "PROJETO EXECUTIVO",
    "6": {
        "title": "AQUISIÇÃO DE EQUIPAMENTOS E MATERIAIS",
        "children": {
            "6.1": "Estruturas",
            "6.2": "Cabos e Condutores",
            "6.3": {
                "title": "Equipamentos Principais (TR e CR)",
                "children": {
                    "6.3.1": "Autotransformador",
                    "6.3.2": "Transformador",
                    "6.3.3": "Compensador Estático/Síncrono",
                    "6.3.4": "Reator",
                    "6.3.5": "Capacitor",
                }
            },
            "6.4": {
                "title": "Demais Equipamentos",
                "children": {
                    "6.4.1": "Disjuntor",
                    "6.4.2": "Chave Seccionadora",
                    "6.4.3": "TC",
                    "6.4.4": "TP",
                    "6.4.5": "Para-raios",
                    "6.4.6": "Isolador",
                    "6.4.7": "Bobinas de Bloqueio",
                }
            },
            "6.5": "Serviço Auxiliar",
            "6.6": "Materiais de SPCST",
            "6.7": "Aterramento",
            "6.8": "Barramento",
            "6.9": "Iluminação e Tomadas",
            "6.10": "Ferragens",
            "6.11": "Equipamentos CFTV",
        }
    },
    "7": {
        "title": "SERVIÇOS PRELIMINARES",
        "children": {
            "7.1": "Canteiro de Obras",
            "7.2": "Limpeza dos Acessos",
        }
    },
    "8": {
        "title": "OBRAS CIVIS",
        "children": {
            "8.1": "Terraplenagem",
            "8.2": "Base e Fundações",
            "8.3": "Canaleta e Eletrodutos",
            "8.4": "Drenagem",
            "8.5": "Serviços de Malha de Terra",
            "8.6": "Edificações",
            "8.7": "Urbanização",
        }
    },
    "9": {
        "title": "MONTAGEM",
        "children": {
            "9.1": "Estruturas",
            "9.2": "Cabos e Condutores",
            "9.3": {
                "title": "Equipamentos Principais (TR e CR)",
                "children": {
                    "9.3.1": "Autotransformador",
                    "9.3.2": "Transformador",
                    "9.3.3": "Compensador Estático/Síncrono",
                    "9.3.4": "Reator",
                    "9.3.5": "Capacitor",
                }
            },
            "9.4": {
                "title": "Demais Equipamentos",
                "children": {
                    "9.4.1": "Disjuntor",
                    "9.4.2": "Chave Seccionadora",
                    "9.4.3": "TC",
                    "9.4.4": "TP",
                    "9.4.5": "Para-raios",
                    "9.4.6": "Isolador",
                    "9.4.7": "Bobinas de Bloqueio",
                }
            },
            "9.5": "Serviço Auxiliar",
            "9.6": "SPCST",
            "9.7": "Aterramento",
            "9.8": "Barramento",
            "9.9": "Iluminação e Tomadas",
            "9.10": "Equipamentos CFTV",
        }
    },
    "10": {
        "title": "COMISSIONAMENTO",
        "children": {
            "10.1": "Linhas",
            "10.2": "Subestações",
            "10.3": "Autotransformador",
            "10.4": "Transformador",
            "10.5": "Compensador Estático/Síncrono",
            "10.6": "Reator",
            "10.7": "Capacitor",
            "10.8": "Disjuntor",
            "10.9": "Chave Seccionadora",
            "10.10": "TC",
            "10.11": "TP",
            "10.12": "Para-raios",
            "10.13": "Isolador",
            "10.14": "Bobinas de Bloqueio",
            "10.15": "Serviço Auxiliar",
            "10.16": "SPCST",
        }
    },
    "11": "DESMONTAGEM",
    "12": "GERENCIAMENTO PRÉ/PÓS-MOBILIZAÇÃO",
    "13": "ENERGIZAÇÃO",
    "14": "OUTROS"
}


class CheckBoxTreeNode(TreeViewNode, BoxLayout):
    def __init__(self, key="", text="", is_parent=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 30

        self.checkbox = CheckBox(size_hint_x=None, width=30)
        self.label = Label(text=text, halign='left', size_hint_x=0.9)

        self.add_widget(self.checkbox)
        self.add_widget(self.label)

        self.key = key
        self.text = text
        self.is_parent = is_parent

        if is_parent:
            self.checkbox.color = (0, 0, 1, 1)  # Blue for parent nodes


class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        # Adicionando logo (verifique se o caminho da imagem está correto)
        try:
            self.logo = Image(source='img/Eletrobras.png',
                              size_hint=(1, 0.4),
                              keep_ratio=True,
                              allow_stretch=True)
            self.layout.add_widget(self.logo)
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            self.layout.add_widget(
                Label(text="ELETROBRAS", font_size=24, bold=True))

        # Layout para os botões
        botoes_layout = BoxLayout(
            size_hint_y=0.2, spacing=20, padding=(20, 0, 20, 0))

        # Botão Voltar (desabilitado pois é a primeira tela)
        self.botao_voltar = Button(
            text="Voltar",
            # Mais claro para indicar desabilitado
            background_color=(0.8, 0.3, 0.3, 0.5),
            disabled=True
        )

        # Botão Extrair
        self.botao_extrair = Button(
            text="[b]EXTRAIR[/b]",
            size_hint=(0.7, 1),
            font_size='24sp',
            markup=True,
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            background_down='atlas://data/images/defaulttheme/button_pressed'
        )
        self.botao_extrair.bind(on_press=self.ir_para_selecao)

        botoes_layout.add_widget(self.botao_voltar)
        botoes_layout.add_widget(self.botao_extrair)

        self.layout.add_widget(Label(size_hint_y=0.2))  # Espaçamento
        self.layout.add_widget(botoes_layout)

        self.add_widget(self.layout)

    def ir_para_selecao(self, instance):
        self.manager.current = 'selecao_atividades'


class TelaSelecaoAtividades(Screen):
    selected = DictProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # ScrollView para a lista de atividades
        self.scroll = ScrollView()
        self.tree = TreeView(hide_root=True, size_hint_y=None)
        self.tree.bind(minimum_height=self.tree.setter('height'))

        # Adicionando as atividades à árvore
        self.adicionar_atividades(self.tree, atividades)

        self.scroll.add_widget(self.tree)
        self.layout.add_widget(self.scroll)

        # Barra de botões
        botoes = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        botoes.add_widget(Button(
            text="Voltar",
            background_color=(0.8, 0.3, 0.3, 1),
            on_press=lambda x: setattr(self.manager, 'current', 'inicio')
        ))
        botoes.add_widget(Button(
            text="Avançar",
            background_color=(0.2, 0.6, 1, 1),
            on_press=self.avancar
        ))
        self.layout.add_widget(botoes)

        self.add_widget(self.layout)

    def adicionar_atividades(self, tree, dados, parent_node=None):
        for key, value in dados.items():
            if isinstance(value, str):  # Atividade simples
                node = CheckBoxTreeNode(key=key, text=f"{key} - {value}")
                tree.add_node(node, parent_node)
                self.selected[key] = (node.checkbox, value)
            elif isinstance(value, dict):  # Atividade com subatividades
                title = value.get("title", key)
                parent = CheckBoxTreeNode(
                    key=key, text=f"{key} - {title}", is_parent=True)
                tree.add_node(parent, parent_node)
                if "children" in value:
                    self.adicionar_atividades(tree, value["children"], parent)

    def avancar(self, instance):
        # Verifica se pelo menos uma atividade foi selecionada
        selected_activities = {}
        for key, (checkbox, nome) in self.selected.items():
            if checkbox.active:
                selected_activities[key] = nome

        if not selected_activities:
            return  # Poderia adicionar um aviso aqui

        # Passa para a próxima tela
        periodo_screen = self.manager.get_screen('periodo')
        periodo_screen.selected_activities = selected_activities
        self.manager.current = 'periodo'


class TelaPeriodo(Screen):
    selected_activities = ObjectProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Entradas para as datas
        self.input_inicio = TextInput(
            hint_text="Data Início (YYYY-MM-DD)",
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )
        self.input_fim = TextInput(
            hint_text="Data Fim (YYYY-MM-DD)",
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )

        self.layout.add_widget(
            Label(text="Data Início:", size_hint_y=None, height=30))
        self.layout.add_widget(self.input_inicio)
        self.layout.add_widget(
            Label(text="Data Fim:", size_hint_y=None, height=30))
        self.layout.add_widget(self.input_fim)

        # Barra de botões
        botoes = BoxLayout(size_hint_y=None, height=60, spacing=10, padding=10)
        botoes.add_widget(Button(
            text="Voltar",
            background_color=(0.8, 0.3, 0.3, 1),
            on_press=lambda x: setattr(
                self.manager, 'current', 'selecao_atividades')
        ))
        self.btn_gerar = Button(
            text="Gerar Planilha",
            background_color=(0.2, 0.6, 1, 1),
            on_press=self.gerar_planilha
        )
        botoes.add_widget(self.btn_gerar)
        self.layout.add_widget(botoes)

        self.label_resultado = Label(text="", size_hint_y=None, height=40)
        self.layout.add_widget(self.label_resultado)

        self.add_widget(self.layout)

    def gerar_planilha(self, instance):
        try:
            data_inicio = datetime.strptime(self.input_inicio.text, "%Y-%m-%d")
            data_fim = datetime.strptime(self.input_fim.text, "%Y-%m-%d")

            if data_fim < data_inicio:
                raise ValueError("Data fim deve ser posterior à data início")

            # Gerando lista de meses entre a data de início e fim
            meses = []
            atual = data_inicio.replace(day=1)
            while atual <= data_fim:
                meses.append(atual.strftime("%b/%y"))
                if atual.month == 12:
                    atual = atual.replace(year=atual.year + 1, month=1)
                else:
                    atual = atual.replace(month=atual.month + 1)

            # Criando DataFrame para a planilha
            data = []
            for key, nome in self.selected_activities.items():
                linha = {"Atividade": f"{key} - {nome}", "Valor": ""}
                for m in meses:
                    linha[m] = ""
                data.append(linha)

            filename = f"relatorio_atividades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)

            self.label_resultado.text = f"✅ Planilha gerada: {filename}"
            self.btn_gerar.disabled = True
            self.btn_gerar.text = "Gerado!"
            self.btn_gerar.background_color = (0, 0.7, 0, 1)

        except ValueError as ve:
            self.label_resultado.text = f"Erro: {ve}"
        except Exception as e:
            self.label_resultado.text = f"Erro inesperado: {str(e)}"


class GeradorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name='inicio'))
        sm.add_widget(TelaSelecaoAtividades(name='selecao_atividades'))
        sm.add_widget(TelaPeriodo(name='periodo'))
        return sm


if __name__ == '__main__':
    GeradorApp().run()
