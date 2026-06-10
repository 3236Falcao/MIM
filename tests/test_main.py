import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import main


class TestMIM(unittest.TestCase):
    def test_adicionar_registro_salva_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "registros.json"
            data_hora = datetime(2026, 6, 5, 8, 30, 0)

            registro = main.adicionar_registro(
                "manhã",
                "Acordei bem.",
                caminho,
                data_hora,
                tipo_de_dia="docente",
                estado_fisico="descansado",
                estado_mental="focado",
                estado_emocional="calmo",
                prioridades=["Aula", "Planejar semana", "Descansar"],
                foco_unico="Finalizar plano de aula.",
                lembrar_30_dias="Revisar se a rotina nova funcionou.",
            )

            self.assertEqual(registro["periodo"], "manhã")
            self.assertEqual(registro["texto"], "Acordei bem.")
            self.assertEqual(registro["data"], "2026-06-05")
            self.assertEqual(registro["tipo_de_dia"], "docente")
            self.assertEqual(registro["estado"]["fisico"], "descansado")
            self.assertEqual(registro["estado"]["mental"], "focado")
            self.assertEqual(registro["estado"]["emocional"], "calmo")
            self.assertEqual(registro["prioridades"], ["Aula", "Planejar semana", "Descansar"])
            self.assertEqual(registro["foco_unico"], "Finalizar plano de aula.")
            self.assertEqual(registro["lembrar_30_dias"], "Revisar se a rotina nova funcionou.")

            dados = json.loads(caminho.read_text(encoding="utf-8"))
            self.assertEqual(len(dados), 1)
            self.assertEqual(dados[0]["hora"], "08:30:00")

    def test_formatar_registros_vazio(self):
        self.assertEqual(main.formatar_registros([]), "Nenhum registro encontrado.")

    def test_criar_registro_rejeita_texto_vazio(self):
        with self.assertRaises(ValueError):
            main.criar_registro("noite", "   ")

    def test_criar_registro_rejeita_tipo_de_dia_invalido(self):
        with self.assertRaises(ValueError):
            main.criar_registro("manhã", "Bom dia.", tipo_de_dia="invalido")

    def test_criar_registro_aceita_tipo_de_dia_hibrido(self):
        registro = main.criar_registro(
            "manhã",
            "Dia com várias frentes.",
            tipo_de_dia="híbrido",
        )

        self.assertEqual(registro["tipo_de_dia"], "híbrido")

    def test_criar_registro_noite_inclui_decisao_aprendizado_e_conselho(self):
        registro = main.criar_registro(
            "noite",
            "Fechei o dia.",
            data_hora=datetime(2026, 6, 5, 21, 0, 0),
            decisao_importante="Adiar uma entrega para preservar qualidade.",
            aprendizado_principal="Pausas curtas evitaram retrabalho.",
            conselho_para_amanha="Começar pela tarefa mais difícil.",
        )

        self.assertEqual(
            registro["decisao_importante"],
            "Adiar uma entrega para preservar qualidade.",
        )
        self.assertEqual(registro["aprendizado_principal"], "Pausas curtas evitaram retrabalho.")
        self.assertEqual(registro["conselho_para_amanha"], "Começar pela tarefa mais difícil.")

    def test_gerar_relatorio_diario_filtra_por_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_dados = Path(temp_dir) / "registros.json"
            caminho_relatorio = Path(temp_dir) / "relatorio.txt"
            registros = [
                {
                    "periodo": "manhã",
                    "texto": "Planejei o dia.",
                    "data": "2026-06-05",
                    "hora": "07:15:00",
                    "tipo_de_dia": "planejamento",
                    "estado": {
                        "fisico": "cansado",
                        "mental": "organizado",
                        "emocional": "estável",
                    },
                    "prioridades": ["Preparar aula", "Resolver pendências", "Dormir cedo"],
                    "foco_unico": "Preparar aula inaugural.",
                    "lembrar_30_dias": "Conferir se o planejamento foi realista.",
                },
                {
                    "periodo": "noite",
                    "texto": "Revisei o dia.",
                    "data": "2026-06-05",
                    "hora": "22:00:00",
                    "decisao_importante": "Não aceitar uma reunião extra.",
                    "aprendizado_principal": "Limitar contexto melhorou o foco.",
                    "conselho_para_amanha": "Proteger o primeiro bloco da manhã.",
                },
                {
                    "periodo": "noite",
                    "texto": "Registro de outro dia.",
                    "data": "2026-06-04",
                    "hora": "22:30:00",
                },
            ]
            main.salvar_registros(registros, caminho_dados)

            relatorio = main.gerar_relatorio_diario(
                caminho_dados,
                caminho_relatorio,
                data="2026-06-05",
            )

            self.assertIn("Relatorio Diario - MIM v0.4", relatorio)
            self.assertIn("Planejei o dia.", relatorio)
            self.assertIn("Tipo de dia: planejamento", relatorio)
            self.assertIn("Estado: físico: cansado; mental: organizado; emocional: estável", relatorio)
            self.assertIn("Prioridades: Preparar aula | Resolver pendências | Dormir cedo", relatorio)
            self.assertIn("Foco único: Preparar aula inaugural.", relatorio)
            self.assertIn("Lembrar daqui a 30 dias: Conferir se o planejamento foi realista.", relatorio)
            self.assertIn("Decisão mais importante: Não aceitar uma reunião extra.", relatorio)
            self.assertIn("Aprendizado principal: Limitar contexto melhorou o foco.", relatorio)
            self.assertIn("Conselho para amanhã: Proteger o primeiro bloco da manhã.", relatorio)
            self.assertNotIn("Registro de outro dia.", relatorio)
            self.assertEqual(caminho_relatorio.read_text(encoding="utf-8"), relatorio)

    def test_validar_sistema_valido(self):
        self.assertEqual(main.validar_sistema("trabalho"), "TRABALHO")

    def test_validar_sistema_invalido(self):
        with self.assertRaises(ValueError):
            main.validar_sistema("FINANCAS")

    def test_validar_tipo_de_registro_valido(self):
        self.assertEqual(main.validar_tipo_de_registro("ideia"), "IDEIA")

    def test_validar_tipo_de_registro_invalido(self):
        with self.assertRaises(ValueError):
            main.validar_tipo_de_registro("MEMORIA")

    def test_criar_experiencia_de_aula(self):
        experiencia = main.criar_experiencia(
            sistema="ESTUDOS",
            tipo_registro="AULA",
            titulo="Aula sobre crônica",
            descricao="Turma analisou crônicas curtas.",
            impacto="Boa participação.",
            aprendizado="Exemplos concretos ajudaram.",
            memoria_futura="Retomar produção textual.",
            data_hora=datetime(2026, 6, 5, 14, 0, 0),
            disciplina="Português",
            tema="Crônica",
            objetivo="Identificar marcas do gênero.",
            evidencias="Alunos compararam textos.",
            descobertas="A turma reconhece humor com facilidade.",
            hipotese_pedagogica="Leitura guiada melhora repertório.",
            intervencao_futura="Propor escrita em dupla.",
        )

        self.assertEqual(experiencia["categoria"], "experiencia")
        self.assertEqual(experiencia["sistema"], "ESTUDOS")
        self.assertEqual(experiencia["tipo_registro"], "AULA")
        self.assertEqual(experiencia["aula"]["disciplina"], "Português")
        self.assertEqual(experiencia["aula"]["hipotese_pedagogica"], "Leitura guiada melhora repertório.")

    def test_consultar_por_sistema(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "registros.json"
            registros = [
                {
                    "categoria": "experiencia",
                    "sistema": "TRABALHO",
                    "tipo_registro": "EVENTO",
                    "titulo": "Reunião",
                    "descricao": "Alinhamento semanal.",
                    "impacto": "Clareza de prioridades.",
                    "aprendizado": "Documentar antes ajuda.",
                    "memoria_futura": "Revisar acordos.",
                    "data": "2026-06-05",
                    "hora": "09:00:00",
                },
                {
                    "categoria": "experiencia",
                    "sistema": "FAMILIA",
                    "tipo_registro": "REFLEXAO",
                    "titulo": "Rotina",
                    "descricao": "Organização da noite.",
                    "impacto": "Menos pressa.",
                    "aprendizado": "Preparar itens antes.",
                    "memoria_futura": "Manter rotina simples.",
                    "data": "2026-06-05",
                    "hora": "20:00:00",
                },
            ]
            main.salvar_registros(registros, caminho)

            resultado = main.consultar_por_sistema("trabalho", caminho)

            self.assertEqual(len(resultado), 1)
            self.assertEqual(resultado[0]["titulo"], "Reunião")

    def test_registro_rapido_ideia(self):
        registro = main.criar_registro_rapido(
            "IDEIA: O MIM deve organizar sistemas, não tarefas.",
            data_hora=datetime(2026, 6, 5, 10, 0, 0),
        )

        self.assertEqual(registro["origem"], "inbox_rapida")
        self.assertEqual(registro["sistema"], "PROJETOS")
        self.assertEqual(registro["tipo_registro"], "IDEIA")
        self.assertEqual(registro["descricao"], "O MIM deve organizar sistemas, não tarefas.")
        self.assertTrue(registro["processado"])

    def test_registro_rapido_familia(self):
        registro = main.criar_registro_rapido("FAMILIA: Samuel já está melhor.")

        self.assertEqual(registro["sistema"], "FAMILIA")
        self.assertEqual(registro["tipo_registro"], "EVENTO")
        self.assertEqual(registro["titulo"], "Samuel já está melhor.")

    def test_registro_rapido_aula(self):
        registro = main.criar_registro_rapido("AULA: A turma respondeu melhor ao trabalho em duplas.")

        self.assertEqual(registro["sistema"], "TRABALHO")
        self.assertEqual(registro["tipo_registro"], "AULA")
        self.assertNotIn("aula", registro)

    def test_registro_rapido_sem_dois_pontos(self):
        registro = main.criar_registro_rapido("TRABALHO Preciso revisar o planejamento semanal.")

        self.assertEqual(registro["sistema"], "TRABALHO")
        self.assertEqual(registro["tipo_registro"], "EVENTO")
        self.assertEqual(registro["descricao"], "Preciso revisar o planejamento semanal.")

    def test_modelo_estruturado_completo(self):
        mensagem = """
[SISTEMA]: PROJETOS
[TIPO]: IDEIA
[TÍTULO]: Organização por sistemas
[DATA]: 2026-06-05
[DESCRIÇÃO]: O MIM deve organizar sistemas.
[IMPACTO]: Clareza.
[APRENDIZADO]: Sistemas são mais estáveis que tarefas.
[MEMÓRIA FUTURA]: Revisar arquitetura.
"""

        registro = main.criar_registro_estruturado(mensagem)

        self.assertEqual(registro["origem"], "inbox_estruturada")
        self.assertEqual(registro["sistema"], "PROJETOS")
        self.assertEqual(registro["tipo_registro"], "IDEIA")
        self.assertEqual(registro["data"], "2026-06-05")
        self.assertTrue(registro["processado"])

    def test_modelo_estruturado_incompleto_rejeitado(self):
        mensagem = """
[SISTEMA]: PROJETOS
[TIPO]: IDEIA
[TÍTULO]: Organização por sistemas
"""

        with self.assertRaises(ValueError) as contexto:
            main.criar_registro_estruturado(mensagem)

        self.assertIn("MEMORIA FUTURA", str(contexto.exception))
        self.assertIn("DESCRICAO ou O QUE ACONTECEU", str(contexto.exception))

    def test_modelo_aula_completo(self):
        mensagem = """
[SISTEMA]: TRABALHO
[TIPO]: AULA
[TÍTULO]: Trabalho em duplas
[DATA]: 2026-06-05
[MEMÓRIA FUTURA]: Repetir formato com ajustes.
[DISCIPLINA]: Português
[TURMA]: 8A
[TEMA]: Crônica
[OBJETIVO]: Produzir uma crônica curta.
[O QUE ACONTECEU]: A turma trabalhou melhor em pares.
[EVIDÊNCIAS]: Mais alunos entregaram rascunhos.
[DESCOBERTAS]: Pares reduziram bloqueios.
[HIPÓTESE PEDAGÓGICA]: Colaboração diminui insegurança.
[INTERVENÇÃO FUTURA]: Preparar duplas previamente.
"""

        registro = main.criar_registro_estruturado(mensagem)

        self.assertEqual(registro["tipo_registro"], "AULA")
        self.assertEqual(registro["descricao"], "A turma trabalhou melhor em pares.")
        self.assertEqual(registro["aula"]["turma"], "8A")
        self.assertEqual(registro["aula"]["o_que_aconteceu"], "A turma trabalhou melhor em pares.")
        self.assertEqual(registro["aula"]["intervencao_futura"], "Preparar duplas previamente.")

    def test_modelo_aula_incompleto_rejeitado(self):
        mensagem = """
[SISTEMA]: TRABALHO
[TIPO]: AULA
[TÍTULO]: Trabalho em duplas
[MEMÓRIA FUTURA]: Repetir formato.
[O QUE ACONTECEU]: A turma trabalhou melhor em pares.
[DISCIPLINA]: Português
[TEMA]: Crônica
"""

        with self.assertRaises(ValueError) as contexto:
            main.criar_registro_estruturado(mensagem)

        self.assertIn("TURMA", str(contexto.exception))
        self.assertIn("EVIDENCIAS", str(contexto.exception))
        self.assertIn("INTERVENCAO FUTURA", str(contexto.exception))

    def test_limpeza_da_inbox_apos_processamento(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_inbox = Path(temp_dir) / "inbox.txt"
            caminho_dados = Path(temp_dir) / "registros.json"
            caminho_inbox.write_text("IDEIA: Registrar pela inbox é mais rápido.\n", encoding="utf-8")

            resultado = main.processar_inbox(
                caminho_inbox,
                caminho_dados,
                data_hora=datetime(2026, 6, 5, 11, 0, 0),
            )

            self.assertEqual(len(resultado["salvos"]), 1)
            self.assertEqual(resultado["erros"], [])
            self.assertEqual(caminho_inbox.read_text(encoding="utf-8"), "")
            dados = json.loads(caminho_dados.read_text(encoding="utf-8"))
            self.assertEqual(dados[0]["origem"], "inbox_rapida")

    def test_relatorio_inclui_registros_de_inbox_e_campos_de_aula(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_dados = Path(temp_dir) / "registros.json"
            caminho_relatorio = Path(temp_dir) / "relatorio.txt"
            registros = [
                main.criar_registro_rapido(
                    "IDEIA: Registrar pela inbox é mais rápido.",
                    data_hora=datetime(2026, 6, 5, 9, 0, 0),
                ),
                main.criar_registro_estruturado(
                    """
[SISTEMA]: TRABALHO
[TIPO]: AULA
[TÍTULO]: Trabalho em duplas
[DATA]: 2026-06-05
[MEMÓRIA FUTURA]: Repetir formato.
[DISCIPLINA]: Português
[TURMA]: 8A
[TEMA]: Crônica
[OBJETIVO]: Produzir uma crônica curta.
[O QUE ACONTECEU]: A turma trabalhou melhor em pares.
[EVIDÊNCIAS]: Mais alunos entregaram rascunhos.
[DESCOBERTAS]: Pares reduziram bloqueios.
[HIPÓTESE PEDAGÓGICA]: Colaboração diminui insegurança.
[INTERVENÇÃO FUTURA]: Preparar duplas previamente.
"""
                ),
            ]
            main.salvar_registros(registros, caminho_dados)

            relatorio = main.gerar_relatorio_diario(
                caminho_dados,
                caminho_relatorio,
                data="2026-06-05",
            )

            self.assertIn("Origem: inbox_rapida", relatorio)
            self.assertIn("Origem: inbox_estruturada", relatorio)
            self.assertIn("Turma: 8A", relatorio)
            self.assertIn("O que aconteceu: A turma trabalhou melhor em pares.", relatorio)
            self.assertIn("Hipótese pedagógica: Colaboração diminui insegurança.", relatorio)

    def test_sintese_eco_do_dia_lista_observacoes_aprendizados_e_memorias(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_dados = Path(temp_dir) / "registros.json"
            registros = [
                {
                    "categoria": "experiencia",
                    "sistema": "TRABALHO",
                    "tipo_registro": "AULA",
                    "titulo": "Trabalho em duplas",
                    "descricao": "A turma trabalhou melhor em pares.",
                    "impacto": "Mais participação.",
                    "aprendizado": "Duplas reduzem bloqueios.",
                    "memoria_futura": "Preparar duplas previamente.",
                    "data": "2026-06-05",
                    "hora": "09:00:00",
                },
                {
                    "categoria": "experiencia",
                    "sistema": "FAMILIA",
                    "tipo_registro": "EVENTO",
                    "titulo": "Rotina da noite",
                    "descricao": "A noite fluiu melhor.",
                    "impacto": "Menos pressa.",
                    "aprendizado": "Preparar itens antes ajuda.",
                    "memoria_futura": "Manter rotina simples.",
                    "data": "2026-06-05",
                    "hora": "20:00:00",
                },
                {
                    "periodo": "noite",
                    "texto": "Registro comum do dia.",
                    "data": "2026-06-05",
                    "hora": "21:00:00",
                },
                {
                    "categoria": "experiencia",
                    "sistema": "PROJETOS",
                    "tipo_registro": "IDEIA",
                    "titulo": "Outro dia",
                    "descricao": "Fora da data filtrada.",
                    "impacto": "",
                    "aprendizado": "Não deve aparecer.",
                    "memoria_futura": "Não deve aparecer.",
                    "data": "2026-06-04",
                    "hora": "10:00:00",
                },
            ]
            main.salvar_registros(registros, caminho_dados)

            sintese = main.gerar_sintese_eco_do_dia(caminho_dados, data="2026-06-05")

            self.assertIn("Síntese ECO do dia", sintese)
            self.assertIn("OBSERVAÇÕES", sintese)
            self.assertIn("Quantidade de experiências registradas: 2", sintese)
            self.assertIn("Sistemas envolvidos: FAMILIA, TRABALHO", sintese)
            self.assertIn("APRENDIZADOS", sintese)
            self.assertIn("Duplas reduzem bloqueios.", sintese)
            self.assertIn("Preparar itens antes ajuda.", sintese)
            self.assertIn("MEMÓRIAS FUTURAS", sintese)
            self.assertIn("Preparar duplas previamente.", sintese)
            self.assertIn("Manter rotina simples.", sintese)
            self.assertNotIn("Não deve aparecer.", sintese)

    def test_sintese_eco_do_dia_informa_quando_nao_ha_registros_no_dia(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_dados = Path(temp_dir) / "registros.json"
            registros = [
                {
                    "categoria": "experiencia",
                    "sistema": "PROJETOS",
                    "tipo_registro": "IDEIA",
                    "titulo": "Outro dia",
                    "descricao": "Registro antigo.",
                    "impacto": "",
                    "aprendizado": "Fora da data.",
                    "memoria_futura": "Fora da data.",
                    "data": "2026-06-04",
                    "hora": "10:00:00",
                },
            ]
            main.salvar_registros(registros, caminho_dados)

            sintese = main.gerar_sintese_eco_do_dia(caminho_dados, data="2026-06-05")

            self.assertEqual(sintese, "Nenhum registro encontrado para esta data: 2026-06-05.")

    def test_sintese_eco_do_dia_ignora_aprendizados_e_memorias_vazios(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho_dados = Path(temp_dir) / "registros.json"
            registros = [
                {
                    "categoria": "experiencia",
                    "sistema": "PROJETOS",
                    "tipo_registro": "IDEIA",
                    "titulo": "Registro rápido",
                    "descricao": "Ideia capturada rapidamente.",
                    "impacto": "",
                    "aprendizado": "",
                    "memoria_futura": "   ",
                    "data": "2026-06-05",
                    "hora": "10:00:00",
                },
            ]
            main.salvar_registros(registros, caminho_dados)

            sintese = main.gerar_sintese_eco_do_dia(caminho_dados, data="2026-06-05")

            self.assertIn("Quantidade de experiências registradas: 1", sintese)
            self.assertIn("Sistemas envolvidos: PROJETOS", sintese)
            self.assertIn("- Nenhum aprendizado registrado.", sintese)
            self.assertIn("- Nenhuma memória futura registrada.", sintese)


if __name__ == "__main__":
    unittest.main()
