import streamlit as st
from datetime import datetime, date
import pandas as pd
import plotly.graph_objects as go

# Inicialização
if 'alunos' not in st.session_state:
    st.session_state['alunos'] = {}
if 'avaliacoes' not in st.session_state:
    st.session_state['avaliacoes'] = {}  # Dict: {nome_aluno: [{data:..., dobras:{...}, circ:{...}}]}

def ponto_virgula(mensagem = ''):
    while True:
        entrada = str(input(mensagem).replace(',', '.')).strip()
        if entrada.isalpha():
            print(f'\033[0;31m"{entrada}" não é um valor inválido, tente novamente\033[m')
        elif entrada == '':
            print(f'\033[0;31mPor favor, digite um valor válido\033[m')
        else:
            num = float(entrada)
            return num
        
def calcular_idade(data_nasc):
    hoje = datetime.today()
    idade = hoje.year - data_nasc.year
    if (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day):
        idade -= 1
    return idade

def percent_residual(peso_total, sexo):
    if sexo == "Masculino":
        perpercentual_de_massa_residual = 0.24
    elif sexo =="Feminino":
        perpercentual_de_massa_residual = 0.2

    massa_residual = peso_total * perpercentual_de_massa_residual
    return massa_residual

def Percentual_de_Gordura(Idade, Sete_Dobras, Sexo):
    if Sexo == 'Masculino':
        Densidade_Corporal = 1.112 - 0.00043499 * Sete_Dobras + 0.00000055 * (Sete_Dobras**2) - 0.00028826 * Idade
        percentual = ((495/Densidade_Corporal) - 450)
        return round(percentual, 2)
    elif Sexo == 'Feminino':
        Densidade_Corporal = 1.097 - 0.00046971 * Sete_Dobras + 0.00000056 * (Sete_Dobras**2) - 0.00012828 * Idade
        percentual = ((4.95/Densidade_Corporal) - 450)
        return round(percentual, 2)

def calcular_massa_magra(Percent_Gordura, Peso_total):
    Massa_Magra = Peso_total - (Peso_total*(Percent_Gordura/100))
    return round(Massa_Magra, 2)

def calcular_massa_gorda(Peso_total, Massa_Magra ):
    Massa_Gorda = Peso_total - Massa_Magra
    return round(Massa_Gorda, 2)

def plot_composicao_corporal(idade, sexo, peso_total, dobras, key="grafico"):
    soma_dobras = sum(dobras.values())
    percent_gordura = Percentual_de_Gordura(idade, soma_dobras, sexo)
    massa_magra = calcular_massa_magra(percent_gordura, peso_total)
    massa_gorda = calcular_massa_gorda(peso_total, massa_magra)
    residual = percent_residual(peso_total, sexo)

    nomes_massas = ['Massa Magra', 'Massa Gorda', 'Residual']
    massas = [massa_magra, massa_gorda, residual]
    cores = ["#b41515", "#dbd70c", "#0059FF"]

    fig = go.Figure(data=[go.Pie(labels=nomes_massas, values=massas, hole=.6, marker=dict(colors=cores))])

    fig.update_layout(
        title="Composição Corporal",
        annotations=[
            dict(
                text=f"{peso_total} kg",
                x=0.5, y=0.5,
                font_size=20,
                showarrow=False
            ),
            dict(
                text=f"{massa_magra} kg Magra",
                x=0.02, y=0.5,
                xanchor='right',
                font_size=14,
                showarrow=False
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True, key=key)

def plot_evolucao_completa(avaliacoes, medidas_selecionadas, selecionado):
    fig = go.Figure()
    datas = [datetime.strptime(aval['data'], "%d/%m/%Y") for aval in avaliacoes]

    for medida in medidas_selecionadas:
        valores = []
        unidade = ""

        # Peso
        if medida == "Peso":
            valores = [aval['peso'] for aval in avaliacoes]
            unidade = "kg"

        # Altura
        elif medida == "Altura":
            valores = [aval['altura'] for aval in avaliacoes]
            unidade = "m"

        # Dobras
        elif medida in avaliacoes[0]['dobras']:
            valores = [aval['dobras'][medida] for aval in avaliacoes]
            unidade = "mm"

        # Circunferências
        elif medida in avaliacoes[0]['circunferencias']:
            valores = [aval['circunferencias'][medida] for aval in avaliacoes]
            unidade = "cm"

        # Adiciona linha ao gráfico se encontrou valores
        if valores:
            fig.add_trace(go.Scatter(x=datas, y=valores, mode='lines+markers', name=f"{medida} ({unidade})"))

    fig.update_layout(title=f"Evolução das Medidas de {selecionado}",
                      xaxis_title="Data", yaxis_title="Valor",
                      hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

# ------------------- SIDEBAR --------------------
pagina = st.sidebar.radio("Navegação", ["Cadastro", "Editar Cadastro", "Avaliações", "Prescrição de Treinos", ])

# ------------------- CADASTRO --------------------
if pagina == "Cadastro":
    st.title("📋 Cadastro de Alunos")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome").title()
        data_nasc = st.date_input(
            "Data de nascimento",
            value=datetime(2000, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY"
)
        sexo = st.radio("Sexo", ["Masculino", "Feminino"])

        doenca_cardiaca = st.radio("Doença Cardíaca?", ["Não", "Sim"])
        pressao = st.radio("Pressão alta ou baixa?", ["Normal", "Alta", "Baixa"])        
        experiencia = st.radio("Sedentário ou Experiente em modalidades", ["Sedentário", "Pratica Atividades Físicas"])
        colesterol = st.radio("Colesterol Alto ou Baixo?", ["Nenhum", "Colesterol Alto", "Colesterol Baixo"])
        diabete = st.radio("Diabético?", ["Não Diabético", "Diabético"])

        fuma = st.radio("Fumante?", ["Não fumante", "Fumante"])
        alcool = st.radio("Consumo de álcool:", ["Não consome álcool", "Casualmente", "Frequentemente"])
        sono = st.radio("Qualidade do sono", ["Bom", "Regular", "Ruim"])

        alimentacao = st.radio("Restrição alimentar ou plano nutricional?", ["Não", "Sim"])
        tipo_alimentacao = st.text_input("Qual tipo de restrição ou plano nutricional?").strip()

        lesao = st.radio("Lesão em articulação ou ligamento?", ["Não", "Sim"])
        tipo_lesao = st.text_input("Qual tipo de lesão?").strip()


        enviar = st.form_submit_button("Cadastrar")

        if enviar:
            idade = calcular_idade(data_nasc)
            st.session_state.alunos[nome] = {
                "Data de nascimento": data_nasc.strftime("%d/%m/%Y"),
                "Idade": idade,
                "Sexo": sexo,
                "Doença Cardíaca": doenca_cardiaca,
                "Pressão": pressao,
                "Experiência": experiencia,
                "Colesterol": colesterol,
                "Diabético": diabete,

                "Fumante": fuma,
                "Bebe": alcool,
                "Sono": sono,

                "Alimentação": alimentacao,
                "Tipo de Alimentação": tipo_alimentacao,

                "Lesão": lesao,
                "Tipo de Lesão": tipo_lesao,
                
            }

            st.success(f"{nome} cadastrado com sucesso!")

# ------------------- EDITAR --------------------
elif pagina == "Editar Cadastro":
    st.title("✏️ Editar Cadastro de Alunos")
    nomes = list(st.session_state.alunos.keys())

    if nomes:
        selecionado = st.selectbox("Selecione um aluno", nomes)
        aluno = st.session_state.alunos[selecionado]

        with st.form("editar_form"):
            novo_nome = st.text_input("Nome", value=selecionado).title()
            nova_data = st.date_input("Data de nascimento", datetime.strptime(aluno["Data de nascimento"], "%d/%m/%Y"))
            novo_sexo = st.radio("Sexo", ["Masculino", "Feminino"], index=["Masculino", "Feminino"].index(aluno["Sexo"]))

            col_editar, col_excluir = st.columns(2)
            with col_editar:
                salvar = st.form_submit_button("💾 Salvar")
            with col_excluir:
                excluir = st.form_submit_button("❌ Excluir")

            if salvar:
                nova_idade = calcular_idade(nova_data)
                if novo_nome != selecionado:
                    # Atualiza nome do aluno e mantém as avaliações
                    st.session_state.alunos[novo_nome] = st.session_state.alunos.pop(selecionado)
                    if selecionado in st.session_state.avaliacoes:
                        st.session_state.avaliacoes[novo_nome] = st.session_state.avaliacoes.pop(selecionado)

                # Atualiza dados
                st.session_state.alunos[novo_nome] = {
                    "Data de nascimento": nova_data.strftime("%d/%m/%Y"),
                    "Idade": nova_idade,
                    "Sexo": novo_sexo,
                }

                st.success(f"Dados de {novo_nome} atualizados com sucesso!")

            if excluir:
                confirma = st.text_input("Digite o nome do aluno para confirmar exclusão", key="confirma_excluir")
                if confirma == selecionado:
                    del st.session_state.alunos[selecionado]
                    if selecionado in st.session_state.avaliacoes:
                        del st.session_state.avaliacoes[selecionado]

                    st.success("Cadastro excluído com sucesso!")
                    st.stop()
                elif confirma == "":
                    st.warning("Por favor, digite o nome do aluno para confirmar a exclusão.")
                else:
                    st.warning("Nome digitado incorretamente para exclusão. Tente novamente.")

    else:
        st.info("Nenhum aluno cadastrado.")


# ------------------- AVALIAÇÕES --------------------
elif pagina == "Avaliações":
    st.title("📊 Avaliações Físicas")
    nomes = list(st.session_state.alunos.keys())

    if nomes:
        selecionado = st.selectbox("Selecione um aluno", nomes)
        st.subheader(f"Avaliação de {selecionado}")
        with st.expander("📋 Avaliação Física"):
            with st.form("avaliacao_form"):
                data_aval = st.date_input("Data da avaliação", value=datetime.today())
                
                
                peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1)

                altura = st.number_input("Altura (m)", min_value=0.0, step=0.01)


                st.markdown("#### 📏 Dobras Cutâneas (mm)")
                dobras = {
                    "Peitoral": st.number_input("Peitoral", min_value=0.0, step=0.1),
                    "Tríceps": st.number_input("Tríceps", min_value=0.0, step=0.1),
                    "Subescapular": st.number_input("Subescapular", min_value=0.0, step=0.1),
                    "Axilar_Media":  st.number_input("Axilar_Media", min_value=0.0, step=0.1),
                    "Abdominal": st.number_input("Abdominal", min_value=0.0, step=0.1),
                    "Supra-ilíaca": st.number_input("Supra-ilíaca", min_value=0.0, step=0.1),
                    "Coxa": st.number_input("Coxa", min_value=0.0, step=0.1)
                }


                st.markdown("#### 📏 Circunferências (cm)")
                circ = {
                    "Ombro": st.number_input("Ombro", min_value=0.0, step=0.1),
                    "Torax": st.number_input("Torax", min_value=0.0, step=0.1),
                    "Cintura": st.number_input("Cintura", min_value=0.0, step=0.1),
                    "Abdomen": st.number_input("Abdomen", min_value=0.0, step=0.1),
                    "Quadril": st.number_input("Quadril", min_value=0.0, step=0.1),
                    "Braco_Direito": st.number_input("Braco_Direito", min_value=0.0, step=0.1),
                    "Braco_Esquerdo": st.number_input("Braco_Esquerdo", min_value=0.0, step=0.1),
                    "Antebraco_Direito": st.number_input("Antebraco_Direito", min_value=0.0, step=0.1),
                    "Antebraco_Esquerdo": st.number_input("Antebraco_Esquerdo", min_value=0.0, step=0.1),
                    "Coxa_Direita": st.number_input("Coxa_Direita", min_value=0.0, step=0.1),
                    "Coxa_Esquerda": st.number_input("Coxa_Esquerda", min_value=0.0, step=0.1),
                    "Panturrilha_Direita": st.number_input("Panturrilha_Direita", min_value=0.0, step=0.1),
                    "Panturrilha_Esqueda": st.number_input("Panturrilha_Esqueda", min_value=0.0, step=0.1),
                }

                enviar = st.form_submit_button("Salvar Avaliação")
                if enviar:
                    nova_aval = {
                        "data": data_aval.strftime("%d/%m/%Y"),
                        "peso": peso,
                        "altura": altura,
                        "dobras": dobras,
                        "circunferencias": circ
                    }
                    st.session_state.avaliacoes.setdefault(selecionado, []).append(nova_aval)
                    st.session_state.avaliacoes[selecionado].sort(key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y",))
                    st.success("Avaliação registrada com sucesso!")

    # --------------avaliações anteriores (se houver)
        if selecionado in st.session_state.avaliacoes:
            st.markdown("### 📂 Avaliações anteriores")

            avaliacoes = st.session_state.avaliacoes[selecionado]
            total = len(avaliacoes)
            
            for i, aval in enumerate(st.session_state.avaliacoes[selecionado][::-1], 1):
                numero_invertido = total - i +1
                with st.expander(f"**Avaliação {numero_invertido} - {aval['data']}**"):
                    tab0 ,tab1, tab2, tab3 = st.tabs(["Dobras", "Circunferências", "Peso e Altura", "Editar"])

                    with tab0:
                        col1, col2 = st.columns(2)
                        with col1:
                            for k, v in aval["dobras"].items():
                                st.write(f"{k}: {v} mm")
                        with col2:
                            # --------------Gráfico--------------
                            st.markdown("### 📈 Composição Corporal")

                            idade = calcular_idade(datetime.strptime(st.session_state.alunos[selecionado]["Data de nascimento"], "%d/%m/%Y"))
                            sexo = st.session_state.alunos[selecionado]["Sexo"]
                            peso_total = aval["peso"]
                            soma_dobras = sum(aval["dobras"].values())
                            
                            plot_composicao_corporal(idade, sexo, peso_total, aval["dobras"], key=f"grafico_em_dobras_{i}")

                    with tab1:
                        col1, col2 = st.columns(2)
                        with col1:
                            for k, v in aval["circunferencias"].items():
                                st.write(f"{k}: {v} cm")
                        with col2:
                            # --------------Gráfico--------------
                            st.markdown("### 📈 Composição Corporal")

                            idade = calcular_idade(datetime.strptime(st.session_state.alunos[selecionado]["Data de nascimento"], "%d/%m/%Y"))
                            sexo = st.session_state.alunos[selecionado]["Sexo"]
                            peso_total = aval["peso"]
                            soma_dobras = sum(aval["dobras"].values())
                            
                            plot_composicao_corporal(idade, sexo, peso_total, aval["dobras"], key=f"grafico_em_circunferencia_{i}")                            

                    with tab2:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### Informações iniciais")
                            
                            st.write(f"Peso: {aval['peso']}Kg")
                            st.write(f"Altura: {aval['altura']}m")

                    with tab3:
                        st.markdown("### ✏️ Editar Avaliação")

                        with st.form(f"editar_form_{i}"):
                            # Campos de edição com valores atuais
                            novo_peso = st.number_input("Peso (kg)", value=aval['peso'], min_value=0.0, step=0.1, key=f"peso_{i}")
                            nova_altura = st.number_input("Altura (m)", value=aval['altura'], min_value=0.0, step=0.01, key=f"altura_{i}")

                            st.markdown("#### 📏 Dobras Cutâneas (mm)")
                            novas_dobras = {}
                            for k, v in aval["dobras"].items():
                                novas_dobras[k] = st.number_input(f"{k}", value=v, min_value=0.0, step=0.1, key=f"dobras_{k}_{i}")

                            st.markdown("#### 📏 Circunferências (cm)")
                            novas_circ = {}
                            for k, v in aval["circunferencias"].items():
                                novas_circ[k] = st.number_input(f"{k}", value=v, min_value=0.0, step=0.1, key=f"circ_{k}_{i}")

                            col_editar, col_excluir = st.columns(2)
                            with col_editar:
                                salvar_editar = st.form_submit_button("💾 Salvar")
                            with col_excluir:
                                excluir = st.form_submit_button("❌ Excluir")

                            if salvar_editar:
                                # Atualiza avaliação existente
                                aval['peso'] = novo_peso
                                aval['altura'] = nova_altura
                                aval['dobras'] = novas_dobras
                                aval['circunferencias'] = novas_circ
                                st.success("Avaliação atualizada com sucesso!")

                            if excluir:
                                # Exclui avaliação do aluno
                                st.session_state.avaliacoes[selecionado].remove(aval)
                                st.success("Avaliação excluída com sucesso!\nClique em Salvar para sair desta tela")
                                st.stop()

            st.markdown("### 📈 Evolução do aluno")

            avaliacoes = st.session_state.avaliacoes[selecionado]
            avaliacoes = sorted(avaliacoes, key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))

            medidas_disponiveis = ["Peso", "Altura"] + list(avaliacoes[0]["dobras"].keys()) + list(avaliacoes[0]["circunferencias"].keys())
            medidas_selecionadas = st.multiselect("Selecione as medidas para mostrar no gráfico", medidas_disponiveis, default=["Peso"])

            plot_evolucao_completa(avaliacoes, medidas_selecionadas, selecionado)

    else:
        st.info("Nenhum aluno cadastrado.")

# --------------------PRESCRIÇÂO DE TREINOS --------------------------

elif pagina == "Prescrição de Treinos":
    nomes = list(st.session_state.alunos.keys())

    if nomes:
        selecionado = st.selectbox("Selecione um aluno", nomes)

        st.title("💪 Prescrição de treinos")

#--------------------Dados do Aluno------------------------
        st.markdown("### 📋 Dados do Aluno")
        dados_aluno = st.session_state.alunos[selecionado]

        idade = dados_aluno.get("Idade", "Não informado")
        sexo = dados_aluno.get("Sexo", "Não informado")
        st.write(f"**Idade:** {idade} anos")
        st.write(f"**Sexo:** {sexo}")


        st.markdown("### 🗓 Duração de treino")
        data_inicio = st.date_input(
            "Data de Inicio",
            value=date.today(),
            min_value=date(2025, 1, 1),
            max_value=date(2100, 1, 1),
            format="DD/MM/YYYY"
    )
        data_fim = st.date_input(
            "Data de Término",
            value=date.today(),
            min_value=date(2025, 1, 1),
            max_value=date(2100, 1, 1),
            format="DD/MM/YYYY"
    )
        st.markdown("### Cadastro de treino")


        #-------------------------- Tabela de Treinos -----------------------------------

        def cadastro_treino(c):

            col0, col1, col2, col3, col4 = st.columns(5)


            with col0:
                st.markdown("Tipo de treino")
            with col1:
                st.selectbox(
                    f"Exercício {c}",
                    ["Leg press", "Agachamento livre", "Extensora", "Flexora"],
                    key=f"treino_selectbox_{c}"
                )

            with col2:
                st.number_input("Séries", min_value=0, step=1, key=f"series_{c}")

            with col3:
                st.number_input("Repetição", min_value=0, step=1, key=f"repeticao_{c}")

            with col4:
                st.number_input("Descanso", min_value=0, max_value=5, step=1, key=f"descanso_{c}")

            st.text_input("Observações", key=f"descricao_{c}")

        # Número de treinos
        numero_de_treinos = st.number_input("Qual o número de treinos?", min_value=0, step=1, format="%d")
        numero_de_treinos = int(numero_de_treinos)

        for c in range(1, numero_de_treinos + 1):
            cadastro_treino(c)


#elif pagina == "Idiomas"