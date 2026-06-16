from difflib import SequenceMatcher

def analisar_escrita(palavra_esperada, escrita_aluno):
    palavra = palavra_esperada.strip().upper()
    escrita = escrita_aluno.strip().upper()

    if escrita == "":
        return "N1", "Não respondeu."

    if not any(letra.isalpha() for letra in escrita):
        return "N1", "Utilizou símbolos ou sinais gráficos."

    if escrita == palavra:
        return "N4", "Escreveu corretamente a palavra."

    similaridade = SequenceMatcher(None, palavra, escrita).ratio()

    letras_em_comum = set(palavra) & set(escrita)
    proporcao = len(letras_em_comum) / len(set(palavra))

    tamanho_minimo = len(palavra) * 0.70
    if similaridade >= 0.60 and len(escrita) >= tamanho_minimo:
        return "N3", "Palavra inteligível com omissões ou trocas."

    if proporcao >= 0.30:
        return "N2", "Representou parcialmente os sons da palavra."

    return "N1", "Pouca relação entre escrita e palavra esperada."


if __name__ == "__main__":
    palavra = input("Palavra esperada: ")
    escrita = input("Escrita do aluno: ")

    nivel, justificativa = analisar_escrita(palavra, escrita)

    print("\nRESULTADO")
    print("Nível:", nivel)
    print("Justificativa:", justificativa)
