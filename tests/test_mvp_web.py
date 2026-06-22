import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import mvp_web


class TestMVPWeb(unittest.TestCase):
    def test_salvar_registro_essencial(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "registros.json"

            registro, registros = mvp_web.adicionar_registro_mim(
                {
                    "modo": "observacao_essencial",
                    "foco": "Leitura",
                    "observacao": "A turma participou melhor depois da leitura em duplas.",
                },
                caminho=caminho,
                data_hora=datetime(2026, 6, 19, 10, 30, 0),
            )

            self.assertEqual(len(registros), 1)
            self.assertEqual(registro["modo"], "observacao_essencial")
            self.assertEqual(registro["foco"], "Leitura")
            self.assertEqual(registro["observacao"], "A turma participou melhor depois da leitura em duplas.")
            self.assertEqual(registro["data"], "2026-06-19")
            self.assertEqual(registro["hora"], "10:30:00")

            dados = json.loads(caminho.read_text(encoding="utf-8"))
            self.assertEqual(dados[0]["modo"], "observacao_essencial")

    def test_salvar_registro_investigativo(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "registros.json"

            registro, registros = mvp_web.adicionar_registro_mim(
                {
                    "modo": "observacao_investigativa",
                    "observacoes": [
                        {"hora": "08:10:00", "texto": "João leu o primeiro trecho com apoio."},
                        {"hora": "09:15:00", "texto": "O Grupo B formulou uma hipótese própria."},
                    ],
                },
                caminho=caminho,
                data_hora=datetime(2026, 6, 19, 12, 0, 0),
            )

            self.assertEqual(len(registros), 1)
            self.assertEqual(registro["modo"], "observacao_investigativa")
            self.assertEqual(registro["quantidade_observacoes"], 2)
            self.assertEqual(registro["data"], "2026-06-19")
            self.assertEqual(registro["hora_inicio"], "08:10:00")
            self.assertEqual(registro["hora_finalizacao"], "12:00:00")
            self.assertEqual(registro["sintese"], "Hoje foram registradas 2 observações.")
            self.assertEqual(registro["observacoes"][1]["texto"], "O Grupo B formulou uma hipótese própria.")

    def test_listar_registros(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "registros.json"
            registros = [
                {
                    "modo": "observacao_essencial",
                    "foco": "Escrita",
                    "observacao": "A turma revisou os próprios textos.",
                    "data": "2026-06-19",
                    "hora": "10:30:00",
                }
            ]
            mvp_web.salvar_registros(registros, caminho)

            self.assertEqual(mvp_web.listar_registros(caminho), registros)

    def test_exportar_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "registros.json"
            mvp_web.salvar_registros(
                [
                    {
                        "modo": "observacao_essencial",
                        "foco": "Participação",
                        "observacao": "Mais estudantes fizeram perguntas.",
                        "data": "2026-06-19",
                        "hora": "11:00:00",
                    }
                ],
                caminho,
            )

            exportado = mvp_web.exportar_registros_json(caminho)

            dados = json.loads(exportado)
            self.assertEqual(dados[0]["modo"], "observacao_essencial")
            self.assertIn('"foco": "Participação"', exportado)

    def test_limpar_registros(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "registros.json"
            mvp_web.salvar_registros(
                [
                    {
                        "modo": "observacao_essencial",
                        "foco": "Comportamento",
                        "observacao": "A turma retomou os combinados.",
                        "data": "2026-06-19",
                        "hora": "11:30:00",
                    }
                ],
                caminho,
            )

            registros = mvp_web.limpar_registros(caminho)

            self.assertEqual(registros, [])
            self.assertEqual(json.loads(caminho.read_text(encoding="utf-8")), [])

    def test_criar_registro_essencial_rejeita_observacao_vazia(self):
        with self.assertRaises(ValueError):
            mvp_web.criar_registro_essencial(
                {"modo": "observacao_essencial", "foco": "Leitura", "observacao": "   "}
            )

    def test_criar_registro_investigativo_rejeita_lista_vazia(self):
        with self.assertRaises(ValueError):
            mvp_web.criar_registro_investigativo({"modo": "observacao_investigativa", "observacoes": []})

    def test_criar_registro_essencial_rejeita_foco_invalido(self):
        with self.assertRaises(ValueError):
            mvp_web.criar_registro_essencial(
                {"modo": "observacao_essencial", "foco": "Matemática", "observacao": "Registro válido."}
            )

    def test_criar_registro_mim_rejeita_modo_invalido(self):
        with self.assertRaises(ValueError):
            mvp_web.criar_registro_mim({"modo": "outro"})

    def test_criar_registro_essencial_direto(self):
        registro = mvp_web.criar_registro_essencial(
            {
                "modo": "observacao_essencial",
                "foco": "Grupo A",
                "observacao": "O grupo concluiu a leitura sem mediação direta.",
            },
            data_hora=datetime(2026, 6, 19, 10, 30, 0),
        )

        self.assertEqual(registro["modo"], "observacao_essencial")
        self.assertEqual(registro["foco"], "Grupo A")
        self.assertEqual(registro["observacao"], "O grupo concluiu a leitura sem mediação direta.")
        self.assertEqual(registro["data"], "2026-06-19")
        self.assertEqual(registro["hora"], "10:30:00")


if __name__ == "__main__":
    unittest.main()
