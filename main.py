import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "registros.json"
REPORT_FILE = BASE_DIR / "reports" / "relatorio_diario.txt"
INBOX_FILE = BASE_DIR / "inbox" / "inbox.txt"
TIPOS_DE_DIA = ("docente", "doméstico", "criativo", "planejamento", "recuperação", "híbrido")
SISTEMAS = ("TRABALHO", "FAMILIA", "ESPIRITUALIDADE", "ESCRITA", "ESTUDOS", "PROJETOS", "SAUDE")
TIPOS_DE_REGISTRO = ("EVENTO", "REFLEXAO", "PLANEJAMENTO", "AULA", "IDEIA")
MAPEAMENTO_RAPIDO = {
    "IDEIA": ("PROJETOS", "IDEIA"),
    "AULA": ("TRABALHO", "AULA"),
    "TRABALHO": ("TRABALHO", "EVENTO"),
    "FAMILIA": ("FAMILIA", "EVENTO"),
    "FAMÍLIA": ("FAMILIA", "EVENTO"),
    "ESCRITA": ("ESCRITA", "IDEIA"),
    "SAUDE": ("SAUDE", "EVENTO"),
    "SAÚDE": ("SAUDE", "EVENTO"),
    "FE": ("ESPIRITUALIDADE", "REFLEXAO"),
    "FÉ": ("ESPIRITUALIDADE", "REFLEXAO"),
    "ESTUDOS": ("ESTUDOS", "REFLEXAO"),
    "MIM": ("PROJETOS", "IDEIA"),
}


def carregar_registros(caminho=DATA_FILE):
    caminho = Path(caminho)
    if not caminho.exists():
        return []

    with caminho.open("r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()
        if not conteudo:
            return []
        return json.loads(conteudo)


def salvar_registros(registros, caminho=DATA_FILE):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(registros, arquivo, ensure_ascii=False, indent=2)


def criar_registro(
    periodo,
    texto,
    data_hora=None,
    tipo_de_dia=None,
    estado_fisico=None,
    estado_mental=None,
    estado_emocional=None,
    prioridades=None,
    foco_unico=None,
    decisao_importante=None,
    aprendizado_principal=None,
    lembrar_30_dias=None,
    conselho_para_amanha=None,
):
    if periodo not in ("manhã", "noite"):
        raise ValueError("Periodo deve ser 'manhã' ou 'noite'.")

    texto = texto.strip()
    if not texto:
        raise ValueError("O texto do registro não pode estar vazio.")

    if tipo_de_dia is not None and tipo_de_dia not in TIPOS_DE_DIA:
        tipos = ", ".join(TIPOS_DE_DIA)
        raise ValueError(f"Tipo de dia inválido. Use: {tipos}.")

    if data_hora is None:
        data_hora = datetime.now()

    registro = {
        "periodo": periodo,
        "texto": texto,
        "data": data_hora.strftime("%Y-%m-%d"),
        "hora": data_hora.strftime("%H:%M:%S"),
    }

    if tipo_de_dia:
        registro["tipo_de_dia"] = tipo_de_dia

    estado = {}
    if estado_fisico:
        estado["fisico"] = estado_fisico.strip()
    if estado_mental:
        estado["mental"] = estado_mental.strip()
    if estado_emocional:
        estado["emocional"] = estado_emocional.strip()
    if estado:
        registro["estado"] = estado

    if prioridades:
        prioridades_limpas = [prioridade.strip() for prioridade in prioridades if prioridade.strip()]
        if prioridades_limpas:
            registro["prioridades"] = prioridades_limpas[:3]

    if foco_unico:
        registro["foco_unico"] = foco_unico.strip()
    if decisao_importante:
        registro["decisao_importante"] = decisao_importante.strip()
    if aprendizado_principal:
        registro["aprendizado_principal"] = aprendizado_principal.strip()
    if lembrar_30_dias:
        registro["lembrar_30_dias"] = lembrar_30_dias.strip()
    if conselho_para_amanha:
        registro["conselho_para_amanha"] = conselho_para_amanha.strip()

    return registro


def adicionar_registro(periodo, texto, caminho=DATA_FILE, data_hora=None, **campos):
    registros = carregar_registros(caminho)
    registro = criar_registro(periodo, texto, data_hora, **campos)
    registros.append(registro)
    salvar_registros(registros, caminho)
    return registro


def normalizar_opcao(valor):
    return valor.strip().upper()


def validar_sistema(sistema):
    sistema = normalizar_opcao(sistema)
    if sistema not in SISTEMAS:
        sistemas = ", ".join(SISTEMAS)
        raise ValueError(f"Sistema inválido. Use: {sistemas}.")
    return sistema


def validar_tipo_de_registro(tipo_registro):
    tipo_registro = normalizar_opcao(tipo_registro)
    if tipo_registro not in TIPOS_DE_REGISTRO:
        tipos = ", ".join(TIPOS_DE_REGISTRO)
        raise ValueError(f"Tipo de registro inválido. Use: {tipos}.")
    return tipo_registro


def criar_experiencia(
    sistema,
    tipo_registro,
    titulo,
    descricao,
    impacto,
    aprendizado,
    memoria_futura,
    data_hora=None,
    disciplina=None,
    tema=None,
    objetivo=None,
    evidencias=None,
    descobertas=None,
    hipotese_pedagogica=None,
    intervencao_futura=None,
    origem=None,
    processado=None,
    turma=None,
    o_que_aconteceu=None,
):
    sistema = validar_sistema(sistema)
    tipo_registro = validar_tipo_de_registro(tipo_registro)

    titulo = titulo.strip()
    descricao = descricao.strip()
    if not titulo:
        raise ValueError("O título não pode estar vazio.")
    if not descricao:
        raise ValueError("A descrição não pode estar vazia.")

    if data_hora is None:
        data_hora = datetime.now()

    experiencia = {
        "categoria": "experiencia",
        "sistema": sistema,
        "tipo_registro": tipo_registro,
        "titulo": titulo,
        "descricao": descricao,
        "impacto": impacto.strip(),
        "aprendizado": aprendizado.strip(),
        "memoria_futura": memoria_futura.strip(),
        "data": data_hora.strftime("%Y-%m-%d"),
        "hora": data_hora.strftime("%H:%M:%S"),
    }

    if origem:
        experiencia["origem"] = origem
    if processado is not None:
        experiencia["processado"] = processado

    campos_aula = (
        disciplina,
        turma,
        tema,
        objetivo,
        o_que_aconteceu,
        evidencias,
        descobertas,
        hipotese_pedagogica,
        intervencao_futura,
    )
    if tipo_registro == "AULA" and any(campo is not None for campo in campos_aula):
        experiencia["aula"] = {
            "disciplina": (disciplina or "").strip(),
            "turma": (turma or "").strip(),
            "tema": (tema or "").strip(),
            "objetivo": (objetivo or "").strip(),
            "o_que_aconteceu": (o_que_aconteceu or "").strip(),
            "evidencias": (evidencias or "").strip(),
            "descobertas": (descobertas or "").strip(),
            "hipotese_pedagogica": (hipotese_pedagogica or "").strip(),
            "intervencao_futura": (intervencao_futura or "").strip(),
        }

    return experiencia


def adicionar_experiencia(caminho=DATA_FILE, data_hora=None, **campos):
    registros = carregar_registros(caminho)
    experiencia = criar_experiencia(data_hora=data_hora, **campos)
    registros.append(experiencia)
    salvar_registros(registros, caminho)
    return experiencia


def consultar_por_sistema(sistema, caminho=DATA_FILE):
    sistema = validar_sistema(sistema)
    registros = carregar_registros(caminho)
    return [registro for registro in registros if registro.get("sistema") == sistema]


def gerar_titulo(descricao):
    primeira_frase = re.split(r"(?<=[.!?])\s+", descricao.strip(), maxsplit=1)[0]
    titulo = primeira_frase[:60].strip()
    return titulo or "Registro rápido"


def separar_palavra_chave(mensagem):
    mensagem = mensagem.strip()
    if ":" in mensagem:
        palavra_chave, descricao = mensagem.split(":", 1)
    else:
        partes = mensagem.split(maxsplit=1)
        palavra_chave = partes[0] if partes else ""
        descricao = partes[1] if len(partes) > 1 else ""
    return normalizar_opcao(palavra_chave), descricao.strip()


def criar_registro_rapido(mensagem, data_hora=None):
    palavra_chave, descricao = separar_palavra_chave(mensagem)
    if palavra_chave not in MAPEAMENTO_RAPIDO:
        chaves = ", ".join(MAPEAMENTO_RAPIDO)
        raise ValueError(f"Palavra-chave inválida. Use: {chaves}.")
    if not descricao:
        raise ValueError("A descrição do registro rápido não pode estar vazia.")

    sistema, tipo_registro = MAPEAMENTO_RAPIDO[palavra_chave]
    return criar_experiencia(
        sistema=sistema,
        tipo_registro=tipo_registro,
        titulo=gerar_titulo(descricao),
        descricao=descricao,
        impacto="",
        aprendizado="",
        memoria_futura="",
        data_hora=data_hora,
        origem="inbox_rapida",
        processado=True,
    )


def possui_campos_estruturados(mensagem):
    return bool(re.search(r"^\[[^\]]+\]:", mensagem, flags=re.MULTILINE))


def normalizar_nome_campo(campo):
    sem_acentos = unicodedata.normalize("NFD", campo)
    sem_acentos = "".join(caractere for caractere in sem_acentos if unicodedata.category(caractere) != "Mn")
    return normalizar_opcao(sem_acentos)


def extrair_campos_estruturados(mensagem):
    padrao = re.compile(r"^\[([^\]]+)\]:\s*(.*)$", flags=re.MULTILINE)
    matches = list(padrao.finditer(mensagem))
    campos = {}

    for indice, match in enumerate(matches):
        nome = normalizar_nome_campo(match.group(1))
        inicio = match.end(2)
        fim = matches[indice + 1].start() if indice + 1 < len(matches) else len(mensagem)
        primeira_linha = match.group(2).strip()
        restante = mensagem[inicio:fim].strip()
        valor = primeira_linha
        if restante:
            valor = f"{valor}\n{restante}".strip() if valor else restante
        campos[nome] = valor.strip()

    return campos


def campos_faltantes_estruturado(campos):
    faltantes = []
    for campo in ("SISTEMA", "TIPO", "TITULO", "MEMORIA FUTURA"):
        if not campos.get(campo):
            faltantes.append(campo)

    tipo = normalizar_opcao(campos.get("TIPO", ""))
    if not campos.get("DESCRICAO") and not campos.get("O QUE ACONTECEU"):
        faltantes.append("DESCRICAO ou O QUE ACONTECEU")

    if tipo == "AULA":
        for campo in ("DISCIPLINA", "TURMA", "TEMA", "EVIDENCIAS", "INTERVENCAO FUTURA"):
            if not campos.get(campo):
                faltantes.append(campo)

    return faltantes


def criar_registro_estruturado(mensagem, data_hora=None):
    campos = extrair_campos_estruturados(mensagem)
    faltantes = campos_faltantes_estruturado(campos)
    if faltantes:
        raise ValueError("Campos faltantes: " + ", ".join(faltantes))

    data_registro = data_hora
    if campos.get("DATA"):
        data_registro = datetime.strptime(campos["DATA"], "%Y-%m-%d")

    descricao = campos.get("DESCRICAO") or campos.get("O QUE ACONTECEU", "")
    return criar_experiencia(
        sistema=campos["SISTEMA"],
        tipo_registro=campos["TIPO"],
        titulo=campos["TITULO"],
        descricao=descricao,
        impacto=campos.get("IMPACTO", ""),
        aprendizado=campos.get("APRENDIZADO", ""),
        memoria_futura=campos["MEMORIA FUTURA"],
        data_hora=data_registro,
        origem="inbox_estruturada",
        processado=True,
        disciplina=campos.get("DISCIPLINA"),
        turma=campos.get("TURMA"),
        tema=campos.get("TEMA"),
        objetivo=campos.get("OBJETIVO"),
        o_que_aconteceu=campos.get("O QUE ACONTECEU"),
        evidencias=campos.get("EVIDENCIAS"),
        descobertas=campos.get("DESCOBERTAS"),
        hipotese_pedagogica=campos.get("HIPOTESE PEDAGOGICA"),
        intervencao_futura=campos.get("INTERVENCAO FUTURA"),
    )


def processar_mensagem_inbox(mensagem, data_hora=None):
    if possui_campos_estruturados(mensagem):
        return criar_registro_estruturado(mensagem, data_hora)
    return criar_registro_rapido(mensagem, data_hora)


def processar_inbox(caminho_inbox=INBOX_FILE, caminho_dados=DATA_FILE, data_hora=None):
    caminho_inbox = Path(caminho_inbox)
    conteudo = caminho_inbox.read_text(encoding="utf-8").strip() if caminho_inbox.exists() else ""
    if not conteudo:
        return {"salvos": [], "erros": []}

    mensagens = [conteudo] if possui_campos_estruturados(conteudo) else conteudo.splitlines()
    registros = carregar_registros(caminho_dados)
    salvos = []
    erros = []

    for mensagem in mensagens:
        mensagem = mensagem.strip()
        if not mensagem:
            continue
        try:
            registro = processar_mensagem_inbox(mensagem, data_hora)
        except ValueError as erro:
            erros.append(str(erro))
            continue
        salvos.append(registro)

    if salvos and not erros:
        registros.extend(salvos)
        salvar_registros(registros, caminho_dados)
        caminho_inbox.write_text("", encoding="utf-8")

    return {"salvos": salvos, "erros": erros}


def formatar_detalhes_registro(registro):
    detalhes = []

    if registro.get("tipo_de_dia"):
        detalhes.append(f"Tipo de dia: {registro['tipo_de_dia']}")

    estado = registro.get("estado", {})
    if estado:
        partes_estado = []
        if estado.get("fisico"):
            partes_estado.append(f"físico: {estado['fisico']}")
        if estado.get("mental"):
            partes_estado.append(f"mental: {estado['mental']}")
        if estado.get("emocional"):
            partes_estado.append(f"emocional: {estado['emocional']}")
        detalhes.append("Estado: " + "; ".join(partes_estado))

    prioridades = registro.get("prioridades", [])
    if prioridades:
        detalhes.append("Prioridades: " + " | ".join(prioridades))

    if registro.get("foco_unico"):
        detalhes.append(f"Foco único: {registro['foco_unico']}")
    if registro.get("decisao_importante"):
        detalhes.append(f"Decisão mais importante: {registro['decisao_importante']}")
    if registro.get("aprendizado_principal"):
        detalhes.append(f"Aprendizado principal: {registro['aprendizado_principal']}")
    if registro.get("lembrar_30_dias"):
        detalhes.append(f"Lembrar daqui a 30 dias: {registro['lembrar_30_dias']}")
    if registro.get("lembrar_por_mim"):
        detalhes.append(f"O que lembrar: {registro['lembrar_por_mim']}")
    if registro.get("conselho_para_amanha"):
        detalhes.append(f"Conselho para amanhã: {registro['conselho_para_amanha']}")

    return detalhes


def formatar_experiencia(registro):
    origem = registro.get("origem", "registro_manual")
    linhas = [
        f"Experiência [{registro['sistema']} / {registro['tipo_registro']}]: {registro['titulo']}",
        f"   - Origem: {origem}",
        f"   - Descrição: {registro['descricao']}",
    ]

    if registro.get("impacto"):
        linhas.append(f"   - Impacto: {registro['impacto']}")
    if registro.get("aprendizado"):
        linhas.append(f"   - Aprendizado: {registro['aprendizado']}")
    if registro.get("memoria_futura"):
        linhas.append(f"   - Memória futura: {registro['memoria_futura']}")

    aula = registro.get("aula")
    if aula:
        linhas.append(f"   - Disciplina: {aula.get('disciplina', '')}")
        linhas.append(f"   - Turma: {aula.get('turma', '')}")
        linhas.append(f"   - Tema: {aula.get('tema', '')}")
        linhas.append(f"   - Objetivo: {aula.get('objetivo', '')}")
        linhas.append(f"   - O que aconteceu: {aula.get('o_que_aconteceu', '')}")
        linhas.append(f"   - Evidências: {aula.get('evidencias', '')}")
        linhas.append(f"   - Descobertas: {aula.get('descobertas', '')}")
        linhas.append(f"   - Hipótese pedagógica: {aula.get('hipotese_pedagogica', '')}")
        linhas.append(f"   - Intervenção futura: {aula.get('intervencao_futura', '')}")

    return linhas


def formatar_registros(registros):
    if not registros:
        return "Nenhum registro encontrado."

    linhas = []
    for indice, registro in enumerate(registros, start=1):
        prefixo = f"{indice}. [{registro['data']} {registro['hora']}] "
        if registro.get("categoria") == "experiencia":
            experiencia = formatar_experiencia(registro)
            linhas.append(prefixo + experiencia[0])
            linhas.extend(experiencia[1:])
        else:
            linhas.append(prefixo + f"{registro['periodo'].capitalize()}: {registro['texto']}")
            for detalhe in formatar_detalhes_registro(registro):
                linhas.append(f"   - {detalhe}")
    return "\n".join(linhas)


def gerar_relatorio_diario(caminho_dados=DATA_FILE, caminho_relatorio=REPORT_FILE, data=None):
    registros = carregar_registros(caminho_dados)

    if data is None:
        data = datetime.now().strftime("%Y-%m-%d")

    registros_do_dia = [registro for registro in registros if registro["data"] == data]

    linhas = [
        "Relatorio Diario - MIM v0.4",
        f"Data: {data}",
        "",
    ]

    if registros_do_dia:
        linhas.append(formatar_registros(registros_do_dia))
    else:
        linhas.append("Nenhum registro encontrado para esta data.")

    relatorio = "\n".join(linhas) + "\n"
    caminho_relatorio = Path(caminho_relatorio)
    caminho_relatorio.parent.mkdir(parents=True, exist_ok=True)
    caminho_relatorio.write_text(relatorio, encoding="utf-8")
    return relatorio


def gerar_sintese_eco_do_dia(caminho_dados=DATA_FILE, data=None):
    registros = carregar_registros(caminho_dados)

    if data is None:
        data = datetime.now().strftime("%Y-%m-%d")

    registros_do_dia = [registro for registro in registros if registro["data"] == data]
    if not registros_do_dia:
        return f"Nenhum registro encontrado para esta data: {data}."

    experiencias = [
        registro
        for registro in registros_do_dia
        if registro.get("categoria") == "experiencia"
    ]
    sistemas = sorted({registro["sistema"] for registro in experiencias if registro.get("sistema")})
    aprendizados = [registro["aprendizado"].strip() for registro in experiencias if registro.get("aprendizado", "").strip()]
    memorias_futuras = [
        registro["memoria_futura"].strip()
        for registro in experiencias
        if registro.get("memoria_futura", "").strip()
    ]

    linhas = [
        "Síntese ECO do dia",
        f"Data: {data}",
        "",
        "OBSERVAÇÕES",
        f"- Quantidade de experiências registradas: {len(experiencias)}",
        "- Sistemas envolvidos: " + (", ".join(sistemas) if sistemas else "nenhum"),
        "",
        "APRENDIZADOS",
    ]

    if aprendizados:
        linhas.extend(f"- {aprendizado}" for aprendizado in aprendizados)
    else:
        linhas.append("- Nenhum aprendizado registrado.")

    linhas.extend(["", "MEMÓRIAS FUTURAS"])
    if memorias_futuras:
        linhas.extend(f"- {memoria}" for memoria in memorias_futuras)
    else:
        linhas.append("- Nenhuma memória futura registrada.")

    return "\n".join(linhas)


def escolher_tipo_de_dia():
    print("Tipos de dia:")
    for indice, tipo in enumerate(TIPOS_DE_DIA, start=1):
        print(f"{indice}. {tipo}")

    escolha = input("Escolha o tipo de dia: ").strip()
    if escolha.isdigit():
        indice = int(escolha) - 1
        if 0 <= indice < len(TIPOS_DE_DIA):
            return TIPOS_DE_DIA[indice]

    if escolha in TIPOS_DE_DIA:
        return escolha

    raise ValueError("Tipo de dia inválido.")


def coletar_prioridades():
    prioridades = []
    for indice in range(1, 4):
        prioridades.append(input(f"Prioridade {indice} do dia: "))
    return prioridades


def escolher_item(nome, opcoes):
    print(f"{nome}:")
    for indice, opcao in enumerate(opcoes, start=1):
        print(f"{indice}. {opcao}")

    escolha = input(f"Escolha {nome.lower()}: ").strip()
    if escolha.isdigit():
        indice = int(escolha) - 1
        if 0 <= indice < len(opcoes):
            return opcoes[indice]

    escolha = normalizar_opcao(escolha)
    if escolha in opcoes:
        return escolha

    raise ValueError(f"{nome} inválido.")


def registrar_periodo(periodo):
    texto = input(f"O que deseja registrar para a {periodo}? ")
    campos = {}

    if periodo == "manhã":
        try:
            campos["tipo_de_dia"] = escolher_tipo_de_dia()
        except ValueError as erro:
            print(f"Erro: {erro}")
            return

        campos["estado_fisico"] = input("Estado físico: ")
        campos["estado_mental"] = input("Estado mental: ")
        campos["estado_emocional"] = input("Estado emocional: ")
        campos["prioridades"] = coletar_prioridades()
        campos["foco_unico"] = input("Foco único: ")
        campos["lembrar_30_dias"] = input("O que o MIM deve lembrar daqui a 30 dias? ")
    else:
        campos["decisao_importante"] = input("Qual foi a decisão mais importante do dia? ")
        campos["aprendizado_principal"] = input("Aprendizado principal: ")
        campos["conselho_para_amanha"] = input("Que conselho o MIM daria para amanhã? ")

    try:
        registro = adicionar_registro(periodo, texto, **campos)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return

    print(f"Registro salvo: {registro['periodo']} em {registro['data']} às {registro['hora']}")


def registrar_experiencia_interativa():
    try:
        sistema = escolher_item("Sistema", SISTEMAS)
        tipo_registro = escolher_item("Tipo de registro", TIPOS_DE_REGISTRO)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return

    campos = {
        "sistema": sistema,
        "tipo_registro": tipo_registro,
        "titulo": input("Título: "),
        "descricao": input("Descrição: "),
        "impacto": input("Impacto: "),
        "aprendizado": input("Aprendizado: "),
        "memoria_futura": input("Memória futura: "),
    }

    if tipo_registro == "AULA":
        campos["disciplina"] = input("Disciplina: ")
        campos["tema"] = input("Tema: ")
        campos["objetivo"] = input("Objetivo: ")
        campos["evidencias"] = input("Evidências: ")
        campos["descobertas"] = input("Descobertas: ")
        campos["hipotese_pedagogica"] = input("Hipótese pedagógica: ")
        campos["intervencao_futura"] = input("Intervenção futura: ")

    try:
        experiencia = adicionar_experiencia(**campos)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return

    print(f"Experiência salva: {experiencia['sistema']} / {experiencia['tipo_registro']}")


def consultar_sistema_interativo():
    try:
        sistema = escolher_item("Sistema", SISTEMAS)
        registros = consultar_por_sistema(sistema)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return

    print(formatar_registros(registros))


def processar_inbox_interativo():
    resultado = processar_inbox()
    for erro in resultado["erros"]:
        print(f"Erro: {erro}")
    print(f"Registros salvos: {len(resultado['salvos'])}")


def ver_registros():
    registros = carregar_registros()
    print(formatar_registros(registros))


def mostrar_sintese_eco_do_dia():
    print(gerar_sintese_eco_do_dia())


def mostrar_menu():
    print("\nMIM v0.4 - Diario inteligente local")
    print("1. Registrar manhã")
    print("2. Registrar noite")
    print("3. Ver registros")
    print("4. Gerar relatório diário")
    print("5. Registrar experiência")
    print("6. Consultar sistema")
    print("7. Processar inbox")
    print("8. Sair")
    print("9. Síntese ECO do dia")


def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            registrar_periodo("manhã")
        elif opcao == "2":
            registrar_periodo("noite")
        elif opcao == "3":
            ver_registros()
        elif opcao == "4":
            relatorio = gerar_relatorio_diario()
            print(relatorio)
            print(f"Relatório salvo em: {REPORT_FILE}")
        elif opcao == "5":
            registrar_experiencia_interativa()
        elif opcao == "6":
            consultar_sistema_interativo()
        elif opcao == "7":
            processar_inbox_interativo()
        elif opcao == "8":
            print("Saindo...")
            break
        elif opcao == "9":
            mostrar_sintese_eco_do_dia()
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
