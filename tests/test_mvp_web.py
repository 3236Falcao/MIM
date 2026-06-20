import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import mvp_web


class TestMVPWeb(unittest.TestCase):
    def test_criar_registro_mvp_exige_apenas_observacao(self):
        registro = mvp_web.criar_registro_mvp(
            {"observacao": "A turma participou melhor depois da leitura em duplas."},
            data_hora=datetime(2026, 6, 19, 10, 30, 0),
        )

        self.assertEqual(registro["categoria"], "mvp_educativo")
        self.assertEqual(registro["titulo"], "Registro pedagógico")
        self.assertEqual(registro["perfil"], "Não informado")
        self.assertEqual(registro["observacao"], "A turma participou melhor depois da leitura em duplas.")
        self.assertEqual(registro["data"], "2026-06-19")
        self.assertEqual(registro["hora"], "10:30:00")

    def test_criar_registro_mvp_inclui_feedback_e_evidencias(self):
        registro = mvp_web.criar_registro_mvp(
            {
                "titulo": "Leitura em duplas",
                "observacao": "Alunos leram e comentaram o texto.",
                "evidencias": "Mais alunos participaram da conversa.",
                "feedback": "Eu mudaria a ordem dos campos.",
                "perfil": "Professor",
                "turma": "8A",
            },
            data_hora=datetime(2026, 6, 19, 11, 0, 0),
        )

        self.assertEqual(registro["titulo"], "Leitura em duplas")
        self.assertEqual(registro["evidencias"], "Mais alunos participaram da conversa.")
        self.assertEqual(registro["feedback_professor"], "Eu mudaria a ordem dos campos.")
        self.assertEqual(registro["perfil"], "Professor")
        self.assertEqual(registro["turma"], "8A")

    def test_criar_registro_mvp_rejeita_observacao_vazia(self):
        with self.assertRaises(ValueError):
            mvp_web.criar_registro_mvp({"titulo": "Sem observação", "observacao": "   "})

    def test_adicionar_registro_mvp_salva_json_local(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "registros.json"

            registro, registros = mvp_web.adicionar_registro_mvp(
                {"observacao": "Registro de teste."},
                caminho=caminho,
                data_hora=datetime(2026, 6, 19, 12, 0, 0),
            )

            self.assertEqual(len(registros), 1)
            self.assertEqual(registro["observacao"], "Registro de teste.")
            dados = json.loads(caminho.read_text(encoding="utf-8"))
            self.assertEqual(dados[0]["categoria"], "mvp_educativo")


if __name__ == "__main__":
    unittest.main()
