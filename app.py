import streamlit as st
from datetime import datetime, date

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



def Percentual_de_Gordura(Idade, Sete_Dobras, Sexo):
    if Sexo == 'Masculino':
        Densidade_Corporal = 1.112 - 0.00043499 * Sete_Dobras + 0.00000055 * (Sete_Dobras**2) - 0.00028826 * Idade
        percentual = ((495/Densidade_Corporal) - 450)
        return round(percentual, 2)
    elif Sexo == 'Feminino':
        Densidade_Corporal = 1.097 - 0.00046971 * Sete_Dobras + 0.00000056 * (Sete_Dobras**2) - 0.00012828 * Idade
        percentual = ((4.95/Densidade_Corporal) - 450)
        return round(percentual, 2)


def Percentual_Residual(Percent_Gordura, Peso_total):
    Massa_Magra = Peso_total - (Peso_total*Percent_Gordura/100)
    return round(Massa_Magra, 2)


def Massa_Gorda(Peso_total, Massa_Magra ):
    Massa_Gorda = Peso_total - Massa_Magra
    return round(Massa_Gorda, 2)


# ------------------- SIDEBAR --------------------
pagina = st.sidebar.radio("Navegação", ["Cadastro", "Editar Cadastro", "Avaliações"])

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
        peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1)
        altura = st.number_input("Altura (m)", min_value=0.0, step=0.01)
        enviar = st.form_submit_button("Cadastrar")

        if enviar:
            idade = calcular_idade(data_nasc)
            st.session_state.alunos[nome] = {
                "Data de nascimento": data_nasc.strftime("%d/%m/%Y"),
                "Idade": idade,
                "Sexo": sexo,
                "Peso": peso,
                "Altura": altura
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
            novo_peso = st.number_input("Peso (kg)", value=aluno["Peso"], step=0.1)
            nova_altura = st.number_input("Altura (m)", value=aluno["Altura"], step=0.01)

            salvar = st.form_submit_button("Salvar alterações")
            if salvar:
                nova_idade = calcular_idade(nova_data)

                if novo_nome != selecionado:
                    del st.session_state.alunos[selecionado]
                    if selecionado in st.session_state.avaliacoes:
                        st.session_state.avaliacoes[novo_nome] = st.session_state.avaliacoes.pop(selecionado)

                st.session_state.alunos[novo_nome] = {
                    "Data de nascimento": nova_data.strftime("%d/%m/%Y"),
                    "Idade": nova_idade,
                    "Sexo": novo_sexo,
                    "Peso": novo_peso,
                    "Altura": nova_altura
                }

                st.success(f"Dados de {novo_nome} atualizados com sucesso!")
    else:
        st.info("Nenhum aluno cadastrado ainda.")

# ------------------- AVALIAÇÕES --------------------
elif pagina == "Avaliações":
    st.title("📊 Avaliações Físicas")
    nomes = list(st.session_state.alunos.keys())

    if nomes:
        selecionado = st.selectbox("Selecione um aluno", nomes)
        st.subheader(f"Avaliação de {selecionado}")
        
        with st.form("avaliacao_form"):
            data_aval = st.date_input("Data da avaliação", value=datetime.today())
            

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
                    "dobras": dobras,
                    "circunferencias": circ
                }
                st.session_state.avaliacoes.setdefault(selecionado, []).append(nova_aval)
                st.success("Avaliação registrada com sucesso!")

        # Mostrar avaliações passadas (se houver)
        if selecionado in st.session_state.avaliacoes:
            st.markdown("### 📂 Avaliações anteriores")
            for i, aval in enumerate(st.session_state.avaliacoes[selecionado][::-1], 1):
                st.markdown(f"**Avaliação {i} - {aval['data']}**")
                with st.expander("Ver detalhes"):
                    st.markdown("**Dobras:**")
                    for k, v in aval["dobras"].items():
                        st.write(f"{k}: {v} mm")
                    st.markdown("**Circunferências:**")
                    for k, v in aval["circunferencias"].items():
                        st.write(f"{k}: {v} cm")
    else:
        st.info("Cadastre pelo menos um aluno para começar.")
