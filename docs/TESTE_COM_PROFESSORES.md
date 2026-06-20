# Teste do MIM com Professores

## Objetivo do teste

Validar uma versão simples do MIM PWA com amigos professores, observando se o registro pedagógico é rápido, claro e útil no celular.

Esta versão não exige login. Os registros ficam salvos localmente em JSON no computador que estiver rodando o sistema.

## Como acessar

Na raiz do projeto, execute:

```bash
python3 mvp_web.py
```

Depois acesse no navegador:

```text
http://127.0.0.1:8000
```

Para testar no celular, o computador e o celular precisam estar na mesma rede.

Para expor o teste na rede local, execute:

```bash
python3 mvp_web.py --host 0.0.0.0
```

Depois, no celular, acesse o IP local do computador na porta 8000, por exemplo:

```text
http://192.168.0.10:8000
```

## Como registrar uma aula

1. Abra a tela inicial do MIM.
2. Toque em `Começar registro` ou na aba `Registrar`.
3. Preencha o campo principal `O que aconteceu?`.
4. Se fizer sentido, preencha turma, título, evidências observadas e feedback.
5. No campo final, responda: `O que você mudaria no MIM?`
6. Toque em `Salvar registro`.
7. Confira o registro em `Registros anteriores`.

O registro deve poder ser feito em menos de 1 minuto. Se algum campo complementar atrasar o uso, ele pode ficar em branco.

## Quais feedbacks observar

- O professor entendeu rapidamente para que serve o MIM?
- O registro em celular parece simples o bastante?
- O campo principal orienta bem o relato?
- Os campos opcionais ajudam ou atrapalham?
- O botão de exportar JSON é fácil de encontrar?
- A tela `Sobre o MIM` transmite confiança?
- O professor percebe que o MIM não substitui seu julgamento pedagógico?
- O que gerou dúvida, cansaço ou insegurança?

## Perguntas para professores avaliadores

1. Você conseguiria registrar uma aula em menos de 1 minuto?
2. O que você registraria no MIM depois de uma aula real?
3. Que campo você removeria?
4. Que campo você acrescentaria?
5. O texto inicial explica bem a proposta?
6. Você se sentiria confortável usando uma ferramenta assim sem login em um teste inicial?
7. Que tipo de devolutiva pedagógica você esperaria receber depois de vários registros?
8. O que você mudaria no MIM?
