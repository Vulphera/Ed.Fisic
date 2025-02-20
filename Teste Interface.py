from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

class ColetaDados(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.dados = {}
        self.entrada_index = 0  # Índice do campo atualmente focado

        # Campos de entrada
        self.campos = {
            "Nome": TextInput(hint_text="Digite o nome"),
            "Data de Nascimento": TextInput(hint_text="DD/MM/AAAA"),
            "Peso (Kg)": TextInput(hint_text="Ex: 70.5"),
            "Altura (m)": TextInput(hint_text="Ex: 1.75"),
        }

        # Criando os rótulos e inputs
        self.inputs = list(self.campos.values())  # Lista de inputs para controle do TAB
        
        for label, input_field in self.campos.items():
            self.add_widget(Label(text=label, size_hint_y=None, height=30))
            self.add_widget(input_field)

        # Seção do sexo com botões de seleção
        self.add_widget(Label(text="Sexo", size_hint_y=None, height=30))
        
        self.layout_sexo = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)

        self.botao_masculino = ToggleButton(text="Masculino", group="sexo", allow_no_selection=False)
        self.botao_feminino = ToggleButton(text="Feminino", group="sexo", allow_no_selection=False)

        self.layout_sexo.add_widget(self.botao_masculino)
        self.layout_sexo.add_widget(self.botao_feminino)

        self.add_widget(self.layout_sexo)

        # Botão para salvar os dados
        self.botao = Button(text="Salvar Dados", size_hint_y=None, height=50)
        self.botao.bind(on_press=self.salvar_dados)
        self.add_widget(self.botao)

        # Captura de evento de teclado para alternar entre campos ao pressionar TAB
        Window.bind(on_key_down=self.tecla_pressionada)

    def tecla_pressionada(self, window, key, *args):
        if key == 9:  # Código da tecla TAB
            self.entrada_index = (self.entrada_index + 1) % (len(self.inputs) + 1)
            
            if self.entrada_index == len(self.inputs):  # Foca na seleção de sexo
                self.botao_masculino.state = 'down'  # Define um valor inicial
            else:
                self.inputs[self.entrada_index].focus = True

    def salvar_dados(self, instance):
        for label, input_field in self.campos.items():
            self.dados[label] = input_field.text

        # Verifica qual botão de sexo está pressionado
        if self.botao_masculino.state == "down":
            self.dados["Sexo"] = "Masculino"
        elif self.botao_feminino.state == "down":
            self.dados["Sexo"] = "Feminino"
        else:
            self.dados["Sexo"] = "Não selecionado"

        print("Dados salvos:", self.dados)  # Podemos salvar em JSON, BD, etc.

class MeuApp(App):
    def build(self):
        return ColetaDados()

if __name__ == "__main__":
    MeuApp().run()
