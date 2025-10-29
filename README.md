# Educ360_Dashboard_Clinica_Medico

# 🩺 Painel de Consultas Médicas

Este projeto é um **dashboard interativo** desenvolvido em **Python** com as bibliotecas **Streamlit**, **Plotly** e **Pandas**.  
O objetivo é monitorar **métricas de desempenho e faturamento** de consultas médicas por **unidade e especialidade**, oferecendo uma visão clara e dinâmica dos dados clínicos.

---

## 📊 Funcionalidades do Dashboard

✅ Filtro de período (data inicial e final)  
✅ Filtro por unidade médica  
✅ Gráfico de **barras** com total de consultas por unidade  
✅ Gráfico de **pizza** com distribuição por especialidade  
✅ Exibição de **indicadores resumidos** (total de consultas, valor total, ticket médio)  
✅ Layout limpo e responsivo, com gráficos centralizados lado a lado  

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta                    | Descrição |
|--------------------------------|--------------|
| **Python**                    | Linguagem base do projeto |
| **Streamlit**                | Criação do dashboard interativo |
| **Plotly Express**         | Visualização de dados interativas |
| **Pandas**                    | Manipulação e análise dos dados |
| **Visual Studio Code** | Ambiente de desenvolvimento |

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o repositório
```bash
git clonehttps://github.com/claudinez/Educ360_Dashboard_Clinica_Medico

```

### 2️⃣ Criar e ativar ambiente virtual
```bash
python -m venv .venv
# Ativar o ambiente:
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3️⃣ Instalar as dependências
```bash
pip install streamlit pandas plotly
```

### 4️⃣ Executar o painel
```bash
streamlit run Dashboard_Clinica.py
```

---

## 📂 Estrutura do Projeto

```
📁 Painel_Clinica
├── Dashboard_Clinica.py     # Código principal do dashboard
├── consultas.csv             # Base de dados com informações médicas
├── README.md                 # Documentação do projeto
└── imagens/                  # (Opcional) pasta com ícones e gráficos
```

---

## 💡 Possíveis Melhorias Futuras

- Adição de gráfico de **tendência mensal** (linha temporal)  
- Exportação dos dados filtrados em **Excel ou PDF**  
- Integração com base de dados SQL  
- Comparativo entre **ano atual e anterior**  

---

## 👨‍💻 Autor

**Desenvolvido por [Claudinez](https://github.com/claudinez)**  
💬 Analista de Sistemas | Python | Java | JavaScript | CSS | HTML  
📧 Contato: *andrade.claudinez@gmail.com*  

---

## 🧠 Licença

Este projeto é distribuído sob a licença **MIT**.  
Sinta-se à vontade para usar, modificar e compartilhar!
